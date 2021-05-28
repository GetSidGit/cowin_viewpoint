import urllib.request, json, ssl, sys, time, datetime, pywhatkit, pathlib


def trigger_message_alert(user_number, alert_message, time_delay):
    sys.stdout = open(log_path + "cowin_crawler.log", 'a')
    print("Triggering Message alert to : ", user_number)
    trigger_time = datetime.datetime.now() + datetime.timedelta(0, time_delay)
    try:
        pywhatkit.sendwhatmsg(user_number, alert_message, trigger_time.hour, trigger_time.minute)
        print("Alert sent successfully with below message : ")
        print(alert_message)
    except:
        print("Unexpected Error encountered : Verify if make sure, time delay is above 60 seconds")
    sys.stdout.close()

def print_message(session_dict, pincode, date, dosage, above_18, mobile_numbers):
    if above_18:
        age_string = "18 plus"
    else:
        age_string = "45 plus"

    message = "Open Slot detected for " + age_string + " on " + str(date) + \
              " in pincode : " + str(pincode) + " For Dosage : " + str(dosage) + "\n" + \
              "Available Dose Capacity :" + str(session_dict["available_capacity_dose" + str(dosage)]) + "\n" + \
              "Location :" + str(session_dict["name"]) + "\n" + \
              "Address :" + str(session_dict["address"]) + "\n" + \
              "Vaccine Name :" + str(session_dict["vaccine"]) + "\n" + \
              "Slot :" + str(session_dict["slots"]) + "\n" + \
              "Price : " + str(session_dict["fee"]) + " INR" + "\n" + \
              "        --- @getsidgit "
    for number in mobile_numbers:
        trigger_message_alert(number, message, 80)


def hit_handler(pincode, search_date, dosage_count, exemption_dict, session_entry, above_18, mobile_numbers):
    if pincode + search_date + str(session_entry["center_id"]) not in exemption_dict.keys():
        print_message(session_entry, pincode, search_date, dosage_count, above_18, mobile_numbers)
        exemption_dict[pincode + search_date + str(session_entry["center_id"])] = "Place Holder"
    else:
        sys.stdout = open(log_path + "cowin_crawler.log", 'a')
        print(pincode + "|" + search_date + "|" + str(session_entry["center_id"]) + " : Alert already sent")
        sys.stdout.close()

def cowin_search(endpoint_base, location_pincode, search_date, above_18, dosages, sleep, mobile_numbers,
                 exemption_dict):

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    atleast_one_slot_found = 0

    for date in search_date:
        atleast_one_slot_found = 0
        for pin in location_pincode:
            for dosage in dosages:
                endpoint = endpoint_base + "pincode=" + pin + "&date=" + date

                request = urllib.request.Request(endpoint)
                request.add_header('User-Agent',
                                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36')

                response = urllib.request.urlopen(request, context=ssl_context)
                response_code = response.getcode()

                if response_code != 200:
                    sys.stdout = open(log_path + "cowin_crawler.log", 'a')
                    print("Error when fetching data, Error code : ", str(response_code))
                    sys.stdout.close()
                else:
                    vaccine_center_data = json.loads(response.read().decode('utf-8'))
                    for session_entry in vaccine_center_data['sessions']:
                        if above_18 and session_entry['min_age_limit'] == 18:
                            if session_entry["available_capacity_dose" + str(dosage)] != 0:
                                hit_handler(pin, date, dosage, exemption_dict, session_entry, above_18, mobile_numbers)

                        elif above_18 is not True:
                            if session_entry["available_capacity_dose" + str(dosage)] != 0:
                                hit_handler(pin, date, dosage, exemption_dict, session_entry, above_18, mobile_numbers)

                time.sleep(sleep)

            # if atleast_one_slot_found == 1:
            # break

        # if atleast_one_slot_found == 0:
        #    print("No Slots found for : ", date, " In Pincodes : ", location_pincode, "For dosages : ", dosages)
        # else:
        #    break


# Read config
log_path = "/Users/sid/log_dump/cowin/"

path = "/users/sid/PycharmProjects/cowin/"
with open(path + "cowin_user_config.json") as config_data:
    user_config = json.load(config_data)

endpoint_base = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?"
location_pincode = user_config["Pincodes"]
days = user_config['Days']
above_18 = bool(user_config["18_plus"] == "True")
dosages = user_config['Dosage']
alert_mobiles = user_config['Mobile_Numbers']

exemption_dict = {}
attempt_counter = 0
sys.stdout = open(log_path + "cowin_crawler.log", 'a')
for dosage in dosages:
    if dosage not in [1, 2]:
        print("Invalid dosage identified, Triggering Force Abort !")
        sys.exit(1)

base_date = datetime.date.today()
dates_list = []
for day in range(days):
    new_date = base_date + datetime.timedelta(days=day)
    dates_list.append(str(new_date.strftime("%d-%m-%Y")))

message = ""

reference_time = datetime.datetime.now() + datetime.timedelta(0, 900)
pathlib.Path('/Users/sid/Desktop/Desktop/cowin_alive.log').touch()
sys.stdout.close()
while True:
    sys.stdout = open(log_path + "cowin_crawler.log", 'a')
    current_time = datetime.datetime.now()
    if current_time > reference_time:
        print("I'm Alive at : ", current_time)
        pathlib.Path('/Users/sid/Desktop/Desktop/cowin_alive.log').touch()
        reference_time = datetime.datetime.now() + datetime.timedelta(0, 900)

    attempt_counter = attempt_counter + 1
    print("Fresh search Attempt count : ", str(attempt_counter))
    sys.stdout.close()
    cowin_search(endpoint_base, location_pincode, dates_list, above_18, dosages, 4, alert_mobiles, exemption_dict)
    # break
