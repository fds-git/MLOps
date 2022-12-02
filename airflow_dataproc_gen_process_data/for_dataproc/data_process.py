import argparse
import findspark
findspark.init()
findspark.find()
import pyspark
from pyspark.sql import SparkSession

if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Start date increment")
    parser.add_argument("-name", dest="name", help="name", required=True, type=str)
    args = parser.parse_args()
    name = args.name
    print(f'{name}')
    print(pyspark.__version__)

    spark = SparkSession\
            .builder\
            .appName("Feature")\
            .getOrCreate()


    #data = spark.read.csv(f'/user/testdata/{name}/terminals.csv')
    #data.write.parquet(f'/user/processed_data/{name}/processed.parquet')
    #spark.stop()
