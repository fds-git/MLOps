cd /home/ubuntu/MLOps/airflow_dataproc_gen_process_data/for_dataproc

#hdfs dfs -copyFromLocal ./*.parquet /user/testdata/
#sudo rm -r ./*.parquet

# Считываем имя последнего сгенерированного файла и сохраняем его
# в HDFS
LAST_DATA_NAME=`cat last_data_name.txt`
hdfs dfs -copyFromLocal ./${LAST_DATA_NAME} /user/testdata/
sudo rm -r ./${LAST_DATA_NAME}