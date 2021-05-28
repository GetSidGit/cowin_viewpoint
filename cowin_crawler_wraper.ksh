# set project
pycharm_project="cowin"

# Start Virtual Env
source /users/sid/PycharmProjects/${pycharm_project}/venv/bin/activate

# Cleanup log

if [ -f ~/log_dump/cowin/cowin_crawler.log ]
then
rm -f ~/log_dump/cowin/cowin_crawler_*.log
latest_timestamp=`date +%d_%m_%y_%H_%m_%s`
mv ~/log_dump/cowin/cowin_crawler.log ~/log_dump/cowin/cowin_crawler_${latest_timestamp}.log
fi

# Set varibles
python_interpreter=`which python`
project_location="/users/sid/PycharmProjects/cowin"
app_log_location="/users/sid/cowin"

# Invoke the core service
$python_interpreter $project_location/cowin_slot_search.py

# Deactivate venv
deactivate
