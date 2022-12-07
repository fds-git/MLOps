import logging
import argparse
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.regression import LinearRegression

from pyspark.ml import Pipeline

import mlflow
from mlflow.tracking import MlflowClient


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def get_data_path(train_artifact_name):
    data_path = train_artifact_name
    return data_path


def get_pipeline():
    # Используя StringIndexer, OneHotEncoder, VectorAssembler и LinearRegression
    # задайте различные этапы пайплайна
    indexer = # работа с колонкой org
    onehot = # продолжение работы с колонкой org
    assembler = # объедините результат предыдущей работы и колонку mile
    regression = # целевая переменная - duration
    
    pipeline = # Свяжите объекты, представленные выше в единый пайплайн
    return pipeline


def main(args):
    
    # Create Spark Session. Добавьте в название приложения оригинальное имя
    logger.info("Creating Spark Session ...")
    spark = SparkSession\
        .builder\
        .appName("Student_Name_flights_pipeline")\
        .getOrCreate()

    # Load data.
    logger.info("Loading Data ...")
    train_artifact_name = args.train_artifact
    data_path = get_data_path(train_artifact_name)
    
    data = (spark.read.format('csv')
        .options(header='true', inferSchema='true')
        .load(data_path))
 

    # Prepare MLFlow experiment for logging
    client = MlflowClient()
    experiment = client.get_experiment_by_name("Spark_Experiment")
    experiment_id = experiment.experiment_id
    
    
    # Добавьте в название вашего run имя, по которому его можно будет найти в MLFlow
    run_name = 'Student_Name_flights_pipeline' + ' ' + str(datetime.now())

    with mlflow.start_run(run_name=run_name, experiment_id=experiment_id):
        
        inf_pipeline = get_pipeline()

        logger.info("Fitting new model / inference pipeline ...")
        model = # Обучите пайалайн
        
        logger.info("Scoring the model ...")
        evaluator = RegressionEvaluator(labelCol='duration')
        predictions = model.transform(data)
        rmse = evaluator.evaluate(predictions)
                    
        run_id = mlflow.active_run().info.run_id
        logger.info(f"Logging metrics to MLflow run {run_id} ...")
        # Залогируйте метрику rmse c помощью Mlflow
        logger.info(f"Model RMSE: {rmse}")

        logger.info("Saving model ...")
        mlflow.spark.save_model(model, args.output_artifact)

        logger.info("Exporting/logging model ...")
        # Экспортируйте сериализованный pipeline в MLFlow
        # Подсказка: используйте функцию log_model
        # по аналогии с использованием save_model выше
        logger.info("Done")

    spark.stop()
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Model (Inference Pipeline) Training")

    #  При запуске используйте 's3a://mlflow-test/data/flights-larger.csv'
    parser.add_argument(
        "--train_artifact", 
        type=str,
        help='Fully qualified name for training artifact/dataset' 
        'Training dataset will be split into train and validation',
        required=True
    )

    # При запуске используйте оригинальное имя 'Student_Name_flights_pipeline'
    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name for the output serialized model (Inference Artifact folder)",
        required=True,
    )

    args = parser.parse_args()

    main(args)

