cd /home/ubuntu/MLOps/airflow_dataproc_gen_data/for_dataproc

#hdfs dfs -copyFromLocal ./*.parquet /user/testdata/
#sudo rm -r ./*.parquet

# Считываем имя последнего сгенерированного файла и сохраняем его
# в HDFS
FILE_NAME=`cat last_data_name.txt`
hdfs dfs -copyFromLocal ./${FILE_NAME} /user/testdata/
sudo rm -r ./${FILE_NAME=}