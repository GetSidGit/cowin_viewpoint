#!/bin/ksh

# Validate Parameters
if [ $# -gt 1 ]
then
echo "Usage :"
echo " Accepts one optional Argument - Python Virtual Environment actiavte location, None specified no venv is invoked "
echo " Example 1 : nohup <wrapper_path>/setup_check.ksh <path>/venv/bin/activate &"
echo " Example 2 : nohup <wrapper_path>/setup_check.ksh &"
fi

# Start Virtual Env
if [ -z "$1" ]
then
python_interpreter="python3"
else
source $1
python_interpreter=$(which python)
fi

# Set varibles
project_location=$(dirname "$0")

echo "Starting Libraries check"

# Invoke the core service
$python_interpreter "$project_location"/cowin_slot_search.py

if [ $? -ne 0 ]
then
echo "Failure Encountered in check, please make sure below packages are installed : "
echo "
pathlib
ssl
os
datetime
json
pywhatkit
sys
time
urllib.request
"
fi


# Deactivate venv
if [ -z "$1" ]
then
:
else
deactivate
fi