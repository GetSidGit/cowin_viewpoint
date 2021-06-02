import pathlib
import ssl
import os
from cowin import *

# Set base paths
log_path = os.path.expanduser('~/log_dump/cowin/')
path = os.path.dirname(os.path.realpath(__file__)) + "/"

# Read config file
with open(path + "cowin_user_config.json") as config_data:
    user_config = json.load(config_data)
# Set default ssl context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Pickup values from user config file
state_for_search = user_config["State"]
districts_list = user_config["Districts"]
location_pincode = user_config["Pincodes"]
days = user_config['Days']
above_18 = bool(user_config["18_plus"] == "True")
dosages = user_config['Dosage']
alert_mobiles = user_config['Mobile_Numbers']
drive_location = user_config['Drive_path_for_heartbeat']
twilio_string = user_config['twilio_account_sid|auth_token|source_number_with_countrycode']
gmail_connection_string = user_config['source_gmail_address|source_gmail_password|gmail_smtp_port']
mail_list = None

if len(str(gmail_connection_string).split("|")) == 3:
    mail_list = user_config["Gmail_Addresses"]
    mail_list.append(gmail_connection_string)
else:
    write_runtime_message(log_path, "Gmail string is not set correctly, assuming GMAIL component is not required !")

# set endpoints - For faster search, we no more hit findbypin endpoint but rely on district level info
district_endpoint_base_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?"
states_url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
districts_base_url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/"

# Refresh district_reference.json file
refresh_codes(state_for_search, states_url, districts_base_url, ssl_context, path, log_path)

# Initiate exemption placeholder to limit researching the combination and initiate attempts count for logging
exemption_dict = {}
attempt_counter = 0

# Validated dosages info keyed by user in user config file - Trigger force abort incase of invali entry
for dosage in dosages:
    if dosage not in [1, 2]:
        write_runtime_message(log_path, "Invalid dosage identified, Triggering Force Abort !")
        sys.exit(1)

# Generate dates for the specified range (API for one week is not working as expected so manually checking for each day
base_date = datetime.date.today()
dates_list = []

"""
for day in range(days):
    new_date = base_date + datetime.timedelta(days=day)
    dates_list.append(str(new_date.strftime("%d-%m-%Y")))
"""
dates_list.append(base_date.strftime("%d-%m-%Y"))

drive_path_present = False
if drive_location is not None and drive_location != "":
    drive_path_present = True

# Initialize message
message = ""

# Initialize variable to publish alive beat for every 15 minutes
reference_time = datetime.datetime.now() + datetime.timedelta(0, 900)
if drive_path_present:
    pathlib.Path(drive_location + '/cowin_alive.log').touch()

# Load district lookup
file = open(path + "districts_reference.json", "r")
district_details = json.load(file)
file.close()

# Initiate the main execution - No point of return from now !
while True:
    current_time = datetime.datetime.now()
    if current_time > reference_time:
        write_runtime_message(log_path, "I'm Alive at : " + str(current_time))
        if drive_path_present:
            pathlib.Path(drive_location + '/cowin_alive.log').touch()
        reference_time = datetime.datetime.now() + datetime.timedelta(0, 900)

    attempt_counter = attempt_counter + 1
    write_runtime_message(log_path, "Fresh search Attempt count : " + str(attempt_counter))
    cowin_search(district_endpoint_base_url, districts_list, location_pincode, dates_list, above_18, dosages, 4,
                 alert_mobiles, district_details['districts'], exemption_dict, ssl_context, log_path, twilio_string,
                 mail_list)
    # break
