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

print("Check completed, All required modules are found - you can run : cowin_crawler_wraper.ksh")
print("Please note - Log will be captured in : ~/log_dump/cowin folder - script creates this path id required ! ")
print("Please verify if Drive path specified in config file is correct and sync is enabled for you to check heartbeats")