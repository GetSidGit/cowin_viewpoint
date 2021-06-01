all_killed=0
for process in cowin_crawler_wraper.ksh cowin_slot_search.py
do
echo "Killing ${process}"
kill `ps -ef|grep -i ${process}| grep -v grep| awk '{print $2}'`
if [ $? -eq 0 ]
then
echo "Process killed succesfully !"
else
echo "Kill failed, please search and kill manually !"
all_killed=1
fi
done

if [ ${all_killed} -eq 1 ]
then
echo "Complete kill is not succesfull ! please review output and kill process manually"
else
echo "All cowin crawlers are killed !"
fi

