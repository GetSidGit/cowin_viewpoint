# cowin viewpoint

<h2 align="center"> Automated COWIN Slots Notifier on Email & Whatsapp </h1>

This is an automation to find detect free slots on COWIN and notify users through Whatsapp Message and Mail Alerts

</div>

* Automated booking on slot availability is not yet added, but this can trigger alerts within around 2 seconds when an open slot is detected based on search critieria

* User should trigger this code from his computer and let it run as long as watchout for slots is required.

* Supports Twilio

* Automated utilities are built for easy setup and quick start

* Python version greater than 3.8 is a minimum requirement

* Setup scripts will invoke pip wheel to download depedencies, if intended to download packages in anyother way - please make sure that all the packages in package_details.txt are installed

* To use this, either git clone or download the code manually using the download button

* No direct support to windows, but can be run through ubuntu shell (More on this below)




### Quick & Easy steps 

1. Verify if installed python version is 3.8+. If required, please use - https://python.org to download the latest version

2. use git clone or download the code manually using the download button

3. cd to the project location - ``` cd /code/path ```

4. run ``` pip install -r package_details.txt  ``` - you can copy and paste this command 

5. To verify if the installtion has completed succesfully: <br>
    If you dont know or dont have any python virtual environments, <br>
      run : ``` ksh setup_check.sh ``` <br>
    If you have a Virtual Environment and intentd to use it for this, same as above but pass venv actiave 
      run : ``` ksh setup_check.sh <venv actiave location> ``` <br>
      
6. Input to the slot search is controlled by "cowin_user_config.json", just keyin values (self explanatory). Make sure you are in project folder (step 1)<br>
    ``` vi cowin_user_config.json ```
    edit details, review and save with ":wq!" <br>
    
    Before proceeding, take a quick look at - A detailed guide on filling user config sheet : **[cowin_user_config.json](#simple-user-config-guide)**<br>

 ----  SETUP Completed ----
 
 Now that setup is completed, you are good to start, its extreemly simple ! Make sure you are in project directory (Step 1 above)
 
 Before proceeding, take a quick look at - **[execution shortcuts](#execution-shortcuts)**<br>
 
  If you dont know or dont have any python virtual environments, <br>
    run : ``` ksh cowin_crawler_wrapper.ksh ```
  If you have a Virtual Environment and intentd to use it for this, same as above but pass venv actiave 
      run : ``` ksh setup_check.sh <venv actiave location> ``` <br>
 
 
 ## Simple user config guide
 
 * State : Mandatry entry ! - Enter the state name in double quotes <br>
        Example : "Telangana"
 * Districts : Mandatry entry ! - Enter one or more districts, each in double quotes seperated by comma <br>
        Example 1 : ["Hyderabad"] <br>
        Example 2 : ["Hyderabad", "Rangareddy"]
* Pincodes : Mandatry entry ! - Enter "all" if you want to search on all pincodes for the districts above in the state mentioned above. You can also add multiple pincodes in double quotes seperated by commas just like how you did for "Districts" <br>
        Example 1 : ["all"] <br>
        Example 2 : ["500001"]  <br> 
        Example 3 : ["500001", "500002"] <br>
 * Dosage : Mandatry entry ! - The dosage which you are looking for. This is a number and cannot be less than 1 and greater than 2
         Example 1 : [1]
         Example 2 : [2]
         Example 3 : [1, 2]
 * 18_plus : Mandatory entry ! - set "True" if you want to search for 18 plus, "False" if you want to search for 45 plus
         Example 1 : "True"
         Example 2 : "False"
 * Mobile_Numbers : Optional - Enter mobile numbers to alert with country code, in double quotes, comma seperated - just like above <br>
         Example 1 : ["+919999999999"] <br>
         Example 2 : ["+919999999999", "+919111111111"]  <br>
 * Gmail_Addresses : Optional - Only Gmail address is suported, please add GMAIL addresses to trigger alerts - just like above <br>
          Example 1 : ["my_mail_id@gmail.com"] <br>
          Example 2 : ["my_mail_id@gmail.com", "my_another_mail_id@gmail.com"] <br> 
 * source_gmail_address|source_gmail_password|gmail_smtp_port :  Optional - To be filled only if "Gmail_Addresses" values are set. This string will be used to trigger GMAIL alerts. <br>
         This is a combination of : user gmail address, user gmail password, gmail smtp port <br>
         If you are not sure of smtp port number : Example "465"  <br>
         alternatively You can also type any character for smtp port number to make code pick default 465 : Example : "I dont know" <br>
         Example 1 : "my_gmail_id@gmail.com|my_gmail_password|465" <br>
         Example 2 : "my_gmail_id@gmail.com|my_gmail_password|i dont know" <br>
* twilio_account_sid|auth_token|source_number_with_countrycode :  Optional - Use this option to configure you twilio account to send whatsapp messages. This will let you get super fast message alerts. Setup is super fast - I Highly recommend using this. Refer **[twilio setup](#twilio-setup)**  to find out how you can use it 
         you can get below details from you twilio console
         This is a combination of : twilio account sid, twilio account auth token, assigned twilio number <br>
         Example 1 : "my_twilio_account_sid|my_twilio_account_auth_code|my_assigned_twilio_number" <br>
 * Drive_path_for_heartbeat :  Optional - path to your google drive or icloud sync folder on desktop to create and refresh a zero byte heartbeat file - so that user can check process alive status from phone through "folders" app on iphone or "drive" app on android. I highly recomment using this as you will know if the process you triggered is running or not. If you see the trigger file from phone with timestamp of 20 - 25 minutes below you current time (provided you have propert internet connection) - indicates that your process triggered on your laptop might have aborted !
        Example : "/google_drive/or/icloude/folder_location/"

