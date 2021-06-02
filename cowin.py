import datetime
import json
import pywhatkit
import sys
import time
import urllib.request
from twilio.rest import Client
import smtplib


def write_runtime_message(log_file_path, text):
    with open(log_file_path + "cowin_crawler.log", 'a') as data:
        data.write(text + "\n")


def trigger_message_alert_with_twilio(user_number, alert_message, user_twilio_string, cowin_log_path):
    account_sid = str(user_twilio_string).split("|")[0]
    auth_token = str(user_twilio_string).split("|")[1]
    client = Client(account_sid, auth_token)
    from_whatsapp_number = 'whatsapp:' + str(user_twilio_string).split("|")[2]
    to_whatsapp_number = 'whatsapp:' + user_number
    message = client.messages.create(
        from_=from_whatsapp_number,
        body=alert_message,
        to=to_whatsapp_number
    )
    write_runtime_message(cowin_log_path, "Twilio Message SID : " + str(message.sid))


def trigger_message_alert(user_number, alert_message, time_delay, cowin_log_path):
    write_runtime_message(cowin_log_path, "Triggering Message alert to : " + user_number)
    trigger_time = datetime.datetime.now() + datetime.timedelta(0, time_delay)
    pywhatkit.sendwhatmsg(user_number, alert_message, trigger_time.hour, trigger_time.minute)
    write_runtime_message(cowin_log_path, "Alert sent successfully with below message : ")
    write_runtime_message(cowin_log_path, alert_message)


def trigger_gmail_alert(gmail_list, alert_message, cowin_log_path):
    gmail_string = gmail_list[len(gmail_list) - 1]
    mail_subject = alert_message.split(" For Dosage :")[0]
    source_gmail_id = gmail_string.split("|")[0]
    source_gmail_pwd = gmail_string.split("|")[1]
    try:
        source_gmail_smtp_port = gmail_string.split("|")[2]
    except ValueError:
        print("SMTP port must be an integer ! trying with default port 465")
        source_gmail_smtp_port = 465
    try:
        gmail_handler = smtplib.SMTP_SSL("smtp.gmail.com", source_gmail_smtp_port)
        gmail_handler.login(source_gmail_id, source_gmail_pwd)
    except:
        print("GMAIL Login Failed !")
        sys.exit()

    for mail_id in gmail_list[:-1]:
        mail_data = "\r\n".join([
            "From: " + source_gmail_id,
            "To: " + mail_id,
            "Subject: " + mail_subject,
            "", alert_message])
        try:
            gmail_handler.sendmail(source_gmail_id, mail_id, mail_data)
        except:
            print("Send Mail failed ! ")
            sys.exit()
        write_runtime_message(cowin_log_path, "Mail sent to : " + mail_id)

    gmail_handler.quit()


def print_message(session_dict, pincode, date, hit_dosage, hit_above_18, mobile_numbers, cowin_log_path,
                  user_twilio_string, gmail_list):
    if hit_above_18:
        age_string = "18 plus"
    else:
        age_string = "45 plus"

    alert_message = "Open Slot detected for " + age_string + " on " + str(date) + \
                    " in pincode : " + str(pincode) + " For Dosage : " + str(hit_dosage) + "\n" + \
                    "Available Dose Capacity :" + str(session_dict["available_capacity_dose"]) + "\n" \
                    + "Location :" + str(session_dict["name"]) + "\n" + \
                    "Address :" + str(session_dict["address"]) + "\n" + \
                    "Vaccine Name :" + str(session_dict["vaccine"]) + "\n" + \
                    "Slot :" + str(session_dict["slots"]) + "\n" + \
                    "Price : " + str(session_dict["fee"]) + " INR" + "\n" + \
                    "        --- @GetSidGit "

    if gmail_list is not None:
        trigger_gmail_alert(gmail_list, alert_message, cowin_log_path)

    for number in mobile_numbers:
        if user_twilio_string is not None and user_twilio_string != '':
            trigger_message_alert_with_twilio(number, alert_message, user_twilio_string, cowin_log_path)
            time.sleep(1)
        else:
            trigger_message_alert(number, alert_message, 80, cowin_log_path)


def place_request(endpoint, set_ssl_context, cowin_log_path):
    request = urllib.request.Request(endpoint)
    request.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/90.0.4430.93 Safari/537.36')

    response = urllib.request.urlopen(request, context=set_ssl_context)
    response_code = response.getcode()

    if response_code != 200:
        write_runtime_message(cowin_log_path, "Error when fetching data, Error code : " + str(response_code))
        sys.exit()
    return json.loads(response.read().decode('utf-8'))


def refresh_codes(main_state, state_endpoint, district_endpoint_base, set_ssl_context, base_dir, cowin_log_path):
    get_states = place_request(state_endpoint, set_ssl_context, cowin_log_path)

    state_id = None
    for state in get_states["states"]:
        if state["state_name"].lower() == main_state.lower() and state_id is None:
            # write_runtime_message(log_path,"State ID identified for : " + main_state)
            state_id = state["state_id"]

    if state_id is not None:
        districts_url = district_endpoint_base + str(state_id)
    else:
        # write_runtime_message(log_path, "State not found ! " + main_state)
        sys.exit()

    districts_reference = place_request(districts_url, set_ssl_context, cowin_log_path)

    with open(base_dir + "districts_reference.json", "w") as output_file:
        json.dump(districts_reference, output_file)


def hit_handler(pincode, search_date, dosage_count, hits_dict, bunch_of_hits, user_above_18, mobile_numbers,
                cowin_log_path, user_twilio_string, gmail_list):
    for session_entry in bunch_of_hits:
        if pincode + search_date + str(session_entry["center_id"]) + str(session_entry["vaccine"]) not in \
                hits_dict.keys():
            print_message(session_entry, pincode, search_date, dosage_count, user_above_18, mobile_numbers,
                          cowin_log_path, user_twilio_string, gmail_list)
            hits_dict[pincode + search_date + str(session_entry["center_id"]) + str(session_entry["vaccine"])] \
                = "Place Holder "

def get_vaccine_slot_details(source_district_session_entry, source_individual_session, source_search_dosage):

    vaccine_lookup = source_district_session_entry['vaccine_fees']
    details_dict = {
        "center_id": source_district_session_entry['center_id'],
        "date": source_individual_session['date'],
        "available_capacity_dose": source_individual_session["available_capacity_dose" + str(source_search_dosage)],
        "name": source_district_session_entry['name'],
        "address": source_district_session_entry['address'],
        "vaccine": source_individual_session['vaccine'],
        "slots": str(source_individual_session['slots']),
    }
    vaccine_price_found = False
    for entry in vaccine_lookup:
        if not vaccine_price_found and entry["vaccine"] == source_individual_session['vaccine']:
            vaccine_price_found = True
            details_dict["fee"] = entry["fee"]
    if not vaccine_price_found:
        details_dict["fee"] = "Price Not found"

    return details_dict


def initiate_hit_handler(district_session_entry, search_dosage, search_pincodes, pin_flag, search_date, hit_dict,
                         search_18_flag, search_alert_numbers, cowin_log_path, user_twilio_string, gmail_list):
    bunch_of_hits = []
    hit_found = False
    for individual_session in district_session_entry['sessions']:
        if search_18_flag and individual_session['min_age_limit'] == 18 and \
                individual_session["available_capacity_dose" + str(search_dosage)] > 2:
            hit_found = True
            slot_details = get_vaccine_slot_details(district_session_entry, individual_session, search_dosage)
            bunch_of_hits.append(slot_details)
            search_date = individual_session['date']
        elif search_18_flag is not True and individual_session["available_capacity_dose" + str(search_dosage)] > 2:
            hit_found = True
            slot_details = get_vaccine_slot_details(district_session_entry, individual_session, search_dosage)
            bunch_of_hits.append(slot_details)
            search_date = individual_session['date']

    if hit_found:
        if pin_flag == 1:
            hit_handler(str(district_session_entry["pincode"]), search_date, search_dosage, hit_dict,
                        bunch_of_hits,
                        search_18_flag, search_alert_numbers, cowin_log_path, user_twilio_string, gmail_list)
        if str(district_session_entry["pincode"]) in search_pincodes:
            hit_handler(str(district_session_entry["pincode"]), search_date, search_dosage, hit_dict,
                        bunch_of_hits,
                        search_18_flag, search_alert_numbers, cowin_log_path, user_twilio_string, gmail_list)


def cowin_search(endpoint_base, districts, user_pincodes, search_date, above_18_flag, user_dosages, sleep,
                 user_mobile_numbers, district_lookup, attempt_reference_dict, request_ssl_context, cowin_log_path,
                 user_twilio_string, gmail_list):
    # Check if user intend to search in all pincodes of the entered districts
    all_pincodes_flag = 0
    if len(user_pincodes) == 1 and str.lower(user_pincodes[0]) == "all":
        all_pincodes_flag = 1
    for date in search_date:
        for district in districts:
            district_found = 0
            district_id = -1
            for district_dict in district_lookup:
                if district_dict["district_name"].lower() == district.lower() and district_found == 0:
                    district_id = district_dict["district_id"]
                    district_found = 1
            if district_found == 0:
                write_runtime_message(cowin_log_path,
                                      "District : " + district + " Not found ! Triggering Force Abort !")
                sys.exit()
            # for dosage_value in user_dosages:
            district_endpoint = endpoint_base + "district_id=" + str(district_id) + "&date=" + date
            vaccine_center_data = place_request(district_endpoint, request_ssl_context, cowin_log_path)

            for session_entry in vaccine_center_data['centers']:
                for user_dose in user_dosages:
                    # if above_18_flag and session_entry['min_age_limit'] == 18:
                    initiate_hit_handler(session_entry, user_dose, user_pincodes, all_pincodes_flag, date,
                                         attempt_reference_dict, above_18_flag, user_mobile_numbers, cowin_log_path,
                                         user_twilio_string, gmail_list)
                    # elif above_18_flag is not True: initiate_hit_handler(session_entry, user_dose, user_pincodes,
                    # all_pincodes_flag, date, attempt_reference_dict, above_18_flag, user_mobile_numbers,
                    # cowin_log_path, user_twilio_string, gmail_list)

        time.sleep(sleep)
