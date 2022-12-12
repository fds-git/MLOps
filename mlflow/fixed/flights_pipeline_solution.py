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
    indexer = StringIndexer(inputCol='org', outputCol='org_idx')
    onehot = OneHotEncoder(inputCols=['org_idx'], outputCols=['org_dummy'])
    assembler = VectorAssembler(inputCols=['mile', 'org_dummy'], outputCol='features')
    regression = LinearRegression(featuresCol='features', labelCol='duration')
    
    pipeline = Pipeline(stages=[indexer, onehot, assembler, regression])
    return pipeline


def main(args):
    
    # Create Spark Session. Добавьте в название приложения оригинальное имя
    logger.info("Creating Spark Session ...")
    spark = SparkSession\
        .builder\
        .appName("Student_Name_flights_pipeline")\
        .getOrCreate()

    # Load data. Исходные данные для задачи находятся по адресу 's3a://mlflow-test/data/flights-larger.csv'
    logger.info("Loading Data ...")
    train_artifact_name = args.train_artifact
    data_path = get_data_path(train_artifact_name)
    
    data = (spark.read.format('csv')
        .options(header='true', inferSchema='true')
        .load(data_path))
 

    # Prepare MLFlow experiment for logging
    tracking_uri = 'http://10.129.0.26:8000'
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()
    experiment = client.get_experiment_by_name("Spark_Experiment")
    experiment_id = experiment.experiment_id
    
    
    # Добавьте в название вашего run имя, по которому его можно будет найти в MLFlow
    run_name = 'Student_Name_flights_pipeline' + ' ' + str(datetime.now())

    with mlflow.start_run(run_name=run_name, experiment_id=experiment_id):
        
        inf_pipeline = get_pipeline()

        logger.info("Fitting new model / inference pipeline ...")
        model = inf_pipeline.fit(data)
        
        logger.info("Scoring the model ...")
        evaluator = RegressionEvaluator(labelCol='duration')
        predictions = model.transform(data)
        rmse = evaluator.evaluate(predictions)
                    
        run_id = mlflow.active_run().info.run_id
        logger.info(f"Logging metrics to MLflow run {run_id} ...")
        mlflow.log_metric("rmse", rmse)
        logger.info(f"Model RMSE: {rmse}")

        logger.info("Saving model ...")
        mlflow.spark.save_model(model, args.output_artifact)

        logger.info("Exporting/logging model ...")
        mlflow.spark.log_model(model, args.output_artifact)
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
