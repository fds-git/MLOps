import argparse
import findspark
findspark.init()
findspark.find()
import pyspark
from pyspark.sql import SparkSession

if __name__=='__main__':
    spark = SparkSession\
            .builder\
            .appName("Feature_engin")\
            .getOrCreate()

    parser = argparse.ArgumentParser(description="Start date increment")
    parser.add_argument("-name", dest="name", help="name", required=True, type=str)
    args = parser.parse_args()
    name = args.name
    print(f'{name}')
    data = spark.read.parquet(f'/user/testdata/{name}')
    data.write.parquet(f'/user/processed_data/{name}')
    spark.stop()