#!/bin/ksh

# Validate Parameters
if [ $# -gt 1 ]
then
echo "Usage :"
echo " Accepts one optional Argument - Python Virtual Environment actiavte location, None specified no venv is invoked "
echo " Example 1 : nohup <wrapper_path>/cowin_crawler_wrapper.ksh <path>/venv/bin/activate &"
echo " Example 2 : nohup <wrapper_path>/cowin_crawler_wrapper.ksh &"
fi

# Start Virtual Env
if [ -z "$1" ]
then
python_interpreter="python3"
else
source $1
python_interpreter=$(which python)
fi
# Cleanup log

if [ -d ~/log_dump/cowin ]
then
if [ -f ~/log_dump/cowin/cowin_crawler.log ]
then
rm -f ~/log_dump/cowin/cowin_crawler_*.log
latest_timestamp=$(date +%d_%m_%y_%H_%m_%s)
mv ~/log_dump/cowin/cowin_crawler.log ~/log_dump/cowin/cowin_crawler_"${latest_timestamp}".log
fi
else
mkdir -p ~/log_dump/cowin
latest_timestamp=$(date +%d_%m_%y_%H_%m_%s)
fi

# Set varibles
project_location=$(dirname "$0")

echo "Starting python code at ${latest_timestamp}"

# Invoke the core service
$python_interpreter "$project_location"/cowin_slot_search.py

if [ $? -ne 0 ]
then
echo "Failure Encountered in Python execution ! "
fi

# Deactivate venv
if [ -z "$1" ]
then
:
else
deactivate
fi
