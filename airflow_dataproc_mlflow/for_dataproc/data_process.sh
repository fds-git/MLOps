cd /home/ubuntu/MLOps/airflow_dataproc_gen_process_data/for_dataproc

# Считываем имя последнего сгенерированного файла
LAST_DATA_NAME=`cat last_data_name.txt`
# Выполняем предобработку на spark (через sudo не будет работать если директории hdfs созданы не через sudo)
#python3 data_process.py -name ${FILE_NAME}

spark-submit \
--jars mlflow-spark-1.27.0.jar \
python3 data_process.py \
-name ${LAST_DATA_NAME}
