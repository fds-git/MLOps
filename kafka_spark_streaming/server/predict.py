"""OTUS BigData ML kafka consumer example"""

import json
import argparse
from typing import Dict, NamedTuple
import kafka

from pyspark.sql import SparkSession

def main():
    spark = SparkSession\
        .builder\
        .appName("fit_rand_forest")\
        .getOrCreate()

    df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "rc1b-gp5vr3anrc8k7fso.mdb.yandexcloud.net:9091") \
    .option("subscribe", "features") \
    .option("kafka.partition.assignment.strategy", "RoundRobinAssignor") \
    .load()

    df.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "rc1b-gp5vr3anrc8k7fso.mdb.yandexcloud.net:9091") \
    .option("topic", "predictions") \
    .option("checkpointLocation", "./checkpoint") \
    .option("kafka.partition.assignment.strategy", "RoundRobinPartitionAssignor") \
    .start().awaitTermination()

    #df.writeStream \
    #.format("console") \
    #.outputMode("append") \
    #.option("kafka.partition.assignment.strategy", "RoundRobinAssignor") \
    #.start().awaitTermination()

    #spark.streams.awaitAnyTermination()
    #print("dfgdfgdfg")
    #df.write.parquet(f'processed.parquet')
    #spark.stop()

if __name__ == "__main__":
    main()
