import urllib.request, json, ssl, sys, time, datetime


def print_message(session_dict, pincode, date):
    print("Open Slot detected for : ", date, "in pincode : ", pincode)
    print("Location :", session_dict["name"])
    print("Address :", session_dict["address"])
    print("Vaccine Name :", session_dict["vaccine"])
    print("Slot :", session_dict["slots"])
    print("Price : ", session_dict["fee"], " INR")

def cowin_search(endpoint_base, location_pincode, search_date, above_18, dosages, sleep):

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
                request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36')

                response = urllib.request.urlopen(request, context=ssl_context)
                response_code = response.getcode()

                if response_code != 200:
                    print("Error when fetching data, Error code : ", str(response_code))
                else:
                    vaccine_center_data = json.loads(response.read().decode('utf-8'))
                    for session_entry in vaccine_center_data['sessions']:
                        if above_18 and session_entry['min_age_limit'] == 18:
                            if session_entry["available_capacity_dose" + str(dosage)] != 0:
                                print_message(session_entry, pin, date)
                                atleast_one_slot_found = 1
                                return atleast_one_slot_found
                                break
                        elif above_18 is not True:
                            if session_entry["available_capacity_dose" + str(dosage)] != 0:
                                print_message(session_entry, pin, date)
                                atleast_one_slot_found = 1
                                return atleast_one_slot_found
                                break
                time.sleep(5)

            if atleast_one_slot_found == 1:
                break

        if atleast_one_slot_found == 0:
            print("No Slots found for : ", date, " In Pincodes : ", location_pincode, "For dosages : ", dosages)
        else:
            break
    return atleast_one_slot_found

# Read config

with open("cowin_user_config.json") as config_data:
    user_config = json.load(config_data)

endpoint_base = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?"
location_pincode = user_config["Pincodes"]
days = user_config['Days']
above_18 = bool(user_config["18_plus"] == "True")
dosages = user_config['Dosage']
alert_mobiles = user_config['Mobile_Numbers']


for dosage in dosages:
    if dosage not in [1, 2]:
        print("Invalid dosage identified, Triggering Force Abort !")
        sys.exit(1)

base_date = datetime.date.today()
dates_list = []
for day in range(days):
    new_date = base_date + datetime.timedelta(days=day)
    dates_list.append(str(new_date.strftime("%d-%m-%Y")))

while True:
    is_slot_found = cowin_search(endpoint_base, location_pincode, dates_list, above_18, dosages, 5)
    if is_slot_found == 1:
        print("Slot found ! Out of while now !")
        break


