echo ******Hello World from AWS EC2 Instance*******
echo $(hostname -i)
cd /home/ubuntu/MLOps/airflow_dataproc_gen_data/for_dataproc
echo $(pwd)

NEW_DATE=`cat date.txt`
sudo python3 increment_date.py
echo ${NEW_DATE}

sudo python3 create_data.py -c 500 -t 100 -d 2 -date ${NEW_DATE} -r 5

hdfs dfs -copyFromLocal ./*.parquet /user/testdata/
sudo rm -r ./*.parquet