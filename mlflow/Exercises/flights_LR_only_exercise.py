import logging
import argparse
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

import mlflow

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def get_data_path(train_artifact_name):
    data_path = train_artifact_name
    return data_path


def get_regression():
    regression = # используйте Линейную Регрессию.
    # В параметрах укажите: 
    # колонка c признаками (featuresCol) - 'features',
    # колонка с целевой переменной (labelCol) - 'duration'
    return regression


def main(args):
    
    # Create Spark Session. Добавьте в название приложение оригинальное имя - 
    # вместо Student_Name
    logger.info("Creating Spark Session ...")
    spark = SparkSession\
        .builder\
        .appName("Student_Name_flights_LR_only")\
        .getOrCreate()

    # Load data. 
    logger.info("Loading Data ...")
    train_artifact_name = args.train_artifact
    data_path = get_data_path(train_artifact_name)
    
    data = (spark.read.format('csv')
        .options(header='true', inferSchema='true')
        .load(data_path))
    
    assembler = VectorAssembler(inputCols=["mile"], outputCol="features")
    train_data = assembler.transform(data)
    
    regression = get_regression()


    logger.info("Fitting the model ...")
    model = # Запустите обучение модели на датасете train_data

    logger.info("Saving model ...")
    mlflow.spark.save_model(model, args.output_artifact)

    spark.stop()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Model (Inference Pipeline) Training")

    #  При запуске через командную строку
    #  используйте 's3a://mlflow-test/data/flights-larger.csv'
    parser.add_argument(
        "--train_artifact", 
        type=str,
        help='Fully qualified name for training artifact/dataset' 
        'Training dataset will be split into train and validation',
        required=True
    )

    # При запуске в через командную строку используйте оригинальное имя - 
    # например поставьте свой вариант вместо <Student_Name> в 'Student_Name_flights_LR_only'
    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name for the output serialized model (Inference Artifact folder)",
        required=True,
    )

    args = parser.parse_args()

    main(args)