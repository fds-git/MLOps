import logging
import argparse
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.regression import LinearRegression
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit

import mlflow
from mlflow.tracking import MlflowClient


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def get_data_path(train_artifact_name):
    data_path = train_artifact_name
    return data_path


def get_regression():
    regression = LinearRegression(featuresCol='features', labelCol='duration')
    return regression


def main(args):
    
    # Create Spark Session. Добавьте в название приложение оригинальное имя
    logger.info("Creating Spark Session ...")
    spark = SparkSession\
        .builder\
        .appName("model_fit")\
        .getOrCreate()

    # Load data. Исходные данные для задачи находятся по адресу 's3a://mlflow-test/data/flights-larger.csv'
    logger.info("Loading Data ...")
    train_artifact_name = args.train_artifact
    data_name = get_data_path(train_artifact_name)
    
    data=spark.read.parquet(f'/user/processed_data/{data_name}/processed.parquet')
    
    #assembler = VectorAssembler(inputCols=["mile"], outputCol="features")
    #train_data = assembler.transform(data)

    # Prepare MLFlow experiment for logging
    mlflow.set_tracking_uri('http://10.129.0.26:8000')
    client = MlflowClient()
    experiment = client.get_experiment_by_name("Spark_Experiment")
    experiment_id = experiment.experiment_id
    
    #regression = get_regression()

    #model = regression.fit(train_data)

    #logger.info("Saving model ...")
    #mlflow.spark.save_model(model, args.output_artifact)

    print('FITFITFITFIYTFIFTFITFIFIFTFIFTIIF')
    print(experiment_id)

    spark.stop()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Model (Inference Pipeline) Training")

    parser.add_argument(
        "--train_artifact", 
        type=str,
        help='Fully qualified name for training artifact/dataset' 
        'Training dataset will be split into train and validation',
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name for the output serialized model (Inference Artifact folder)",
        required=True,
    )

    args = parser.parse_args()

    main(args)
