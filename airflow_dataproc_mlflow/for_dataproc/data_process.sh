cd /home/ubuntu/MLOps/airflow_dataproc_mlflow/for_dataproc

# Считываем имя последнего сгенерированного файла
LAST_DATA_NAME=`cat last_data_name.txt`

spark-submit \
--jars mlflow-spark-1.27.0.jar \
data_process.py \
-name ${LAST_DATA_NAME}
