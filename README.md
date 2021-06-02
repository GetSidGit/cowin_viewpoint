# cowin viewpoint

<h2 align="center"> Automated COWIN Slots Notifier on Email & Whatsapp </h1>

This is an automation to find detect free slots on COWIN and notify users through Whatsapp Message and Mail Alerts

</div>

Automated booking on slot availability is not yet added, but this can trigger alerts within around 2 seconds when an open slot is detected based on search critieria

User should trigger this code from his computer and let it run as long as watchout for slots is required.

Supports Twilio

Automated utilities are built for easy setup and quick start

Python version greater than 3.8 is a minimum requirement

Setup scripts will invoke pip wheel to download depedencies, if intended to download packages in anyother way - please make sure that all the packages in package_details.txt are installed

To use this, either git clone or download the code manually using the download button

No direct support to windows, but can be run through ubuntu shell (More on this below)




### Quick & Easy steps 

1. Verify if installed python version is 3.8+. If required, please use - https://python.org to download the latest version

2. use git clone or download the code manually using the download button

3. cd to the project location - ``` cd /code/path ```

4. run ``` pip install -r package_details.txt  `` - you can copy and paste this command 

5. To verify if the installtion has completed succesfully: <br>
    If you dont know or dont have any python virtual environments, <br>
      run : ``` ksh setup_check.sh ``` <br>
    If you have a Virtual Environment and intentd to use it for this, same as above but pass venv actiave 
      run : ``` ksh setup_check.sh <venv actiave location> ``` <br>
      
6. Input to the slot search is controlled by "cowin_user_config.json", just keyin values (self explanatory). Make sure you are in project folder (step 1)<br>
    ``` vi cowin_user_config.json ```
    edit details, review and save with ":wq!" <br>
    
    A detailed guide on filling user config sheet, click_here

 -------------------------  SETUP Completed -------------------------
 
 Now that setup is completed, you are good to start, its extreemly simple ! Make sure you are in project directory (Step 1 above)
 
  If you dont know or dont have any python virtual environments, <br>
    run : ``` ksh cowin_crawler_wrapper.ksh ```
  If you have a Virtual Environment and intentd to use it for this, same as above but pass venv actiave 
      run : ``` ksh setup_check.sh <venv actiave location> ``` <br>
 
<br>
