import findspark
findspark.init()
findspark.find()
import pyspark

from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("Student_Name_flights_LR_only")\
        .getOrCreate()

with open('/home/ubuntu/MLOps/airflow_dataproc_gen_process_data/for_dataproc/last_data_name.txt') as f:
    last_data_name = f.readline()

#data = spark.read.parquet(f'/user/testdata/{last_data_name}')
data = spark.read.parquet('/user/testdata/transactions_17_10_2021-22_10_2021.parquet')
data.write.parquet(f'/user/processed_data/transactions_17_10_2021-22_10_2021.parquet')
#print(f'/user/testdata/{last_data_name}')
# Здесь код предобработки данных

#data.write.parquet(f'/user/processed_data/{last_data_name}') 