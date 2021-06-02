import pathlib
import ssl
import os
import datetime
import json
import pywhatkit
import sys
import time
import urllib.request
import twilio

print("Check completed, All required modules are found - you can run : cowin_crawler_wraper.ksh | Windows users : A "
      "direct run of cowin_slot_search.py <path> should be done ! Please refer Git readme")
print("Please note - Log will be captured in : ~/log_dump/cowin folder - script creates this path id required ! For "
      "Windows Users : Script rel;ys on the passed path by user ! Please refer Git readme ")
print(
    'Please verify if Drive path specified in config file is correct and sync is enabled for you to check heartbeats ! '
    'path should have traiing folder slash - / for mac and unix ; // for windows Please note windows users shold give '
    'path with //')
print("Refer readme.md")