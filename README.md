# cowin viewpoint

<h2 align="center"> Automated COWIN Slots Notifier on Email & Whatsapp </h1>

This is an automation to find detect free slots on COWIN and notify users through Whatsapp Message and Mail Alerts

</div>

* Automated booking on slot availability is not yet added, but this can trigger alerts within around 2 seconds when an open slot is detected based on search critieria

* User should trigger this code from his computer and let it run as long as watchout for slots is required.

* Supports Twilio

* Creates HeartBeat file for run monitor from Android or Iphone by pointing to the sync folder

* Automated utilities are built for easy setup and quick start

* Python version greater than 3.8 is a minimum requirement

* Setup scripts will invoke pip wheel to download depedencies, if intended to download packages in anyother way - please make sure that all the packages in package_details.txt are installed

* To use this, either git clone or download the code manually using the download button

* support to windows, Mac and Linux (watchout for special instructions for windows)


### Quick & Easy steps 

            **** FOR WINDOWS USERS ONLY - Below is a super simple option :
            * Download official Ubuntu shell from windows app store : https://www.microsoft.com/store/productId/9NBLGGH4MSV6
            * control panel -> progreams -> "tuen windows features on and off" -> check "Windows subsystem for Linux"
            * Restart - you are good to go, continue from step 1
   Windows users, please refer this : **Refer : [Shortcuts and Logs](#shortcuts-and-logs)** to find out how to naviage through filesystem through ubuntu shell <br>
1. Verify if installed python version is 3.8+. If required, please use - https://python.org to download the latest version

2. use git clone or download the code manually using the download button

3. cd to the project location - ``` cd /code/path ```

4. run ``` pip install -r package_details.txt  ``` - you can copy and paste this command 

5. To verify if the installtion has completed succesfully: <br>
    If you dont know or dont have any python virtual environments, <br>
      run : ``` ksh setup_check.sh ``` <br>
    If you have a Virtual Environment and intentd to use it for this, same as above but pass venv actiave 
      run : ``` ksh setup_check.sh <venv actiave location> ``` <br>
6. Open Browser (Chrome/Safari), Login to https://web.whatsapp.com/ and link to your whatsapp account and close the browser (**Only if you wish to get default whatsapp alerts - Not Email only or whatsapp alert with twilio**)
      
7. Input to the slot search is controlled by "cowin_user_config.json", just keyin values (self explanatory). Make sure you are in project folder (step 1)<br>
    ``` vi cowin_user_config.json ```
    edit details, review and save with ":wq!" <br>
    
**Before proceeding, take a quick look at - A detailed guide on filling user config sheet : **[cowin_user_config.json](#simple-user-config-guide)**<br>**

 ----  SETUP Completed ----
 
 **Before proceeding, take a quick look at - **[execution shortcuts](#execution-shortcuts)**<br>**

Quick note on Alert priority :
1. If Email and Phone numbers are entered : Email alerts trigger first followed by Whatsapp Alerts
2. If None of Email and Phone numbers are entered : alerts are captured in logs for manual inspection
3. If Both Phone Number and Twilio connection details are entered : Twilio bot alerts will be triggered
4. Email alerts are triggered only if GMAIl connection string is added, else Email alerts are skipped
5. Alerts are restricted to one alert per center for a vaccine in a day to avoid spamming
 
 Now that setup is completed, you are good to start, its extreemly simple ! Make sure you are in project directory (Step 1 above)
 
 ## Invoke the main wrapper 
 
  If you dont know or dont have any python **virtual environments**, <br>
    **run :** ``` ksh cowin_crawler_wrapper.ksh ```  <br>
  If you have a **Virtual Environment** and intentd to use it for this, same as above but pass venv actiave <br>
    **run :** ``` ksh setup_check.sh <venv actiave location> ``` <br>
 
 **If you wish to stop the process**, you can either kill manually or use the utility. **Refer : [Shortcuts and Logs](#shortcuts-and-logs)**
 
 As an alternate (Not recommended), you can always invoke script directly with your python intepreter in the code folder - please note that, log cleanup will not be done:
 ``` python3 cowin_slot_search.py ```
 
 ## Simple user config guide
 
 * **State : Mandatry entry !** - Enter the state name in double quotes <br>
        Example : "Telangana"
 * **Districts : Mandatry entry !** - Enter one or more districts, each in double quotes seperated by comma <br>
        Example 1 : ["Hyderabad"] <br>
        Example 2 : ["Hyderabad", "Rangareddy"]
* **Pincodes : Mandatry entry !** - Enter "all" if you want to search on all pincodes for the districts above in the state mentioned above. You can also add multiple pincodes in double quotes seperated by commas just like how you did for "Districts" <br>
        Example 1 : ["all"] <br>
        Example 2 : ["500001"]  <br> 
        Example 3 : ["500001", "500002"] <br>
 * **Dosage : Mandatry entry !** - The dosage which you are looking for. This is a number and cannot be less than 1 and greater than 2
         Example 1 : [1]
         Example 2 : [2]
         Example 3 : [1, 2]
 * **18_plus : Mandatory entry !** - set "True" if you want to search for 18 plus, "False" if you want to search for 45 plus
         Example 1 : "True"
         Example 2 : "False"
 * **Mobile_Numbers : Optional** - Enter mobile numbers to alert with country code, in double quotes, comma seperated - just like above <br>
         Example 1 : ["+919999999999"] <br>
         Example 2 : ["+919999999999", "+919111111111"]  <br>
 * **Gmail_Addresses : Optional** - Any mail address is supported but the user triggering must have a GMAIL account, , please add Email addresses to trigger alerts<br>
          Example 1 : ["my_mail_id@gmail.com"] <br>
          Example 2 : ["my_mail_id@yahoo.com", "my_another_mail_id@hotmail.com"] <br> 
 * **source_gmail_address|source_gmail_password|gmail_smtp_port :  Optional  But Mandatory if Email Alerts are choosen (Gmail_Addresses)** - To be filled only if "Gmail_Addresses" values are set. This string will be used to trigger GMAIL alerts. <br>
         This is a combination of : user gmail address, user gmail password, gmail smtp port <br>
         If you are not sure of smtp port number : Example "465"  <br>
         alternatively You can also type any character for smtp port number to make code pick default 465 : Example : "I dont know" <br>
         Example 1 : "my_gmail_id@gmail.com|my_gmail_password|465" <br>
         Example 2 : "my_gmail_id@gmail.com|my_gmail_password|i dont know" <br>
* **twilio_account_sid|auth_token|source_number_with_countrycode :  Optional** - Use this option to configure you twilio account to send whatsapp messages. This will let you get super fast message alerts. Setup is super fast - **I Highly recommend using this for faster alerts**. <br>
         Refer **[Quick and Simple twilio setup](#twilio-setup)**  to find out how you can use it <br>
         you can get below details from you twilio console <br>
         This is a combination of : twilio account sid, twilio account auth token, assigned twilio number <br>
         Example 1 : "my_twilio_account_sid|my_twilio_account_auth_code|my_assigned_twilio_number" <br>
 * **Drive_path_for_heartbeat :  Optional** - path to your google drive or icloud sync folder on desktop to create and refresh a zero byte heartbeat file - so that user can check process alive status from phone through "folders" app on iphone or "drive" app on android. <br>
            **I highly recommend using this** as you will know if the process you triggered is running or not. If you see the trigger file from phone with timestamp of 20 - 25 minutes below you current time (provided you have propert internet connection) - indicates that your process triggered on your laptop might have aborted !
        Example : "/google_drive/or/icloude/folder_location/"

 ## Twilio Setup
 
 1. Signup for free Twilio trial account - you will get free credits of around 16 dollars - this credit is more than enough <br>
 2. Open whatsapp sandbox : **[Twilio whatsapp sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Flearn%3Fx-target-region%3Dus1)** <br>
 3. From you wahtsapp - send "join sing-run" to the number listed in the above URL. Done ! <br>
 4. your console home will have details on Account SID and Auth Key : **[Twilio console](https://console.twilio.com/?frameUrl=/console)**, keep a note of these two <br>
 5. use the twilio account SID, auth key and assigned phone number with country key aquired in the above steps and pass to "twilio_account_sid|auth_token|source_number_with_countrycode" in the cowin_user_config.json as listed in **[cowin_user_config.json](#simple-user-config-guide)**<br>
 6. Check twilio specific content in **[Basic Debugging](basic-debugging)** before wrapping up Twilio Setup.

## Shortcuts and Logs

1. **If you wish to stop the running process**, you can simply run : ``` ksh kill_cowin_crawler.sh ``` from the folder where the clone/code is residing <br>
2. I recommend to run main wrapper as mentioned **[Invoing Main Wrapper](#invoke-the-main-wrapper)** with nohup such that the process is not depedent on your teminal session <br>
3. you can create an alias for this nohup in .profile or .bash_profile and use shortcut to run <br>
4. Default log path is : ~/  , so setting an alias for log will also help <br>
5. When you run ubuntu shell for the first time, you will be prompted to set username and password, **please remember them to login again**
6. Windows Ubuntu subsytem : you can navigae to windows folders by prefixing your path with "mnt"
      Example : If you wish to go to 'Desktop' - ``` cd /mnt/c/users/<user name>/Desktop ```
     

## Basic Debugging

1. If wrapper is invoked with nohup and failed for some reason - please review the contents of nohup.out on your home directory or on the place of exeuction.
2. For Twilio users - **A reply to at least one message must be sent to the bot within 24 hours** to continue sending alerts beyond that
3. Twilio messages status can also be tracked from Twilio user console to understand the failure reason
4. If Phone number provided **without Twilio String**, code will attempt to trigger whatsapp alert by autmatially opening https://web.whatsapp.com/ and send a message.
           incase while you are using your computer and the process opened the browser and trying to send message - try not to click any buttons
           In anycase, if you observe "send message" not happening from an open https://web.whatsapp.com/ session automatically, you can manually click it and close the browser.
           Alerts through https://web.whatsapp.com/ will take around 40 to 50 seconds to trigger message alert
           Use only Chrome/Safari for basic whatsapp alerts (Not Twilio)
