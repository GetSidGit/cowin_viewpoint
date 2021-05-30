import datetime
import json
import pywhatkit
import sys
import time
import urllib.request

def write_runtime_message(log_file_path, text):
    with open(log_file_path + "cowin_crawler.log", 'a') as data:
        data.write(text + "\n")


def trigger_message_alert(user_number, alert_message, time_delay, cowin_log_path):
    write_runtime_message(cowin_log_path, "Triggering Message alert to : " + user_number)
    trigger_time = datetime.datetime.now() + datetime.timedelta(0, time_delay)
    pywhatkit.sendwhatmsg(user_number, alert_message, trigger_time.hour, trigger_time.minute)
    write_runtime_message(cowin_log_path, "Alert sent successfully with below message : ")
    write_runtime_message(cowin_log_path, alert_message)


def print_message(session_dict, pincode, date, hit_dosage, hit_above_18, mobile_numbers, cowin_log_path):
    if hit_above_18:
        age_string = "18 plus"
    else:
        age_string = "45 plus"

    alert_message = "Open Slot detected for " + age_string + " on " + str(date) + \
                    " in pincode : " + str(pincode) + " For Dosage : " + str(hit_dosage) + "\n" + \
                    "Available Dose Capacity :" + str(session_dict["available_capacity_dose" + str(hit_dosage)]) + "\n"\
                    + "Location :" + str(session_dict["name"]) + "\n" + \
                    "Address :" + str(session_dict["address"]) + "\n" + \
                    "Vaccine Name :" + str(session_dict["vaccine"]) + "\n" + \
                    "Slot :" + str(session_dict["slots"]) + "\n" + \
                    "Price : " + str(session_dict["fee"]) + " INR" + "\n" + \
                    "        --- @getsidgit "
    for number in mobile_numbers:
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
        if state["state_name"] == main_state and state_id is None:
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


def hit_handler(pincode, search_date, dosage_count, hits_dict, session_entry, user_above_18, mobile_numbers,
                cowin_log_path):
    if pincode + search_date + str(session_entry["center_id"]) not in hits_dict.keys():
        print_message(session_entry, pincode, search_date, dosage_count, user_above_18, mobile_numbers, cowin_log_path)
        hits_dict[pincode + search_date + str(session_entry["center_id"])] = "Place Holder"


def initiate_hit_handler(district_session_entry, search_dosage, search_pincodes, pin_flag, search_date, hit_dict,
                         search_18_flag, search_alert_numbers, cowin_log_path):
    if district_session_entry["available_capacity_dose" + str(search_dosage)] != 0:
        if pin_flag == 1:
            hit_handler(str(district_session_entry["pincode"]), search_date, search_dosage, hit_dict,
                        district_session_entry,
                        search_18_flag, search_alert_numbers, cowin_log_path)
        if str(district_session_entry["pincode"]) in search_pincodes:
            hit_handler(str(district_session_entry["pincode"]), search_date, search_dosage, hit_dict,
                        district_session_entry,
                        search_18_flag, search_alert_numbers, cowin_log_path)


def cowin_search(endpoint_base, districts, user_pincodes, search_date, above_18_flag, user_dosages, sleep,
                 user_mobile_numbers, district_lookup, attempt_reference_dict, request_ssl_context, cowin_log_path):
    # Check if user intend to search in all pincodes of the entered districts
    all_pincodes_flag = 0
    if len(user_pincodes) == 1 and str.lower(user_pincodes[0]) == "all":
        all_pincodes_flag = 1
    for date in search_date:
        for district in districts:
            district_found = 0
            district_id = -1
            for district_dict in district_lookup:
                if district_dict["district_name"] == district and district_found == 0:
                    district_id = district_dict["district_id"]
                    district_found = 1
            if district_found == 0:
                write_runtime_message(cowin_log_path,
                                      "District : " + district + " Not found ! Triggering Force Abort !")
                sys.exit()
            # for dosage_value in user_dosages:
            district_endpoint = endpoint_base + "district_id=" + str(district_id) + "&date=" + date
            vaccine_center_data = place_request(district_endpoint, request_ssl_context, cowin_log_path)

            for session_entry in vaccine_center_data['sessions']:
                for user_dose in user_dosages:
                    if above_18_flag and session_entry['min_age_limit'] == 18:
                        initiate_hit_handler(session_entry, user_dose, user_pincodes, all_pincodes_flag, date,
                                             attempt_reference_dict, above_18_flag, user_mobile_numbers, cowin_log_path)
                    elif above_18_flag is not True:
                        initiate_hit_handler(session_entry, user_dose, user_pincodes, all_pincodes_flag, date,
                                             attempt_reference_dict, above_18_flag, user_mobile_numbers, cowin_log_path)

        time.sleep(sleep)
