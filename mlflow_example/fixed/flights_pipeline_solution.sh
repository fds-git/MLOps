spark-submit \
--jars mlflow-spark-1.27.0.jar \
flights_pipeline_solution.py \
--train_artifact "s3a://mlflowbucket/flights_larger.csv" \
--output_artifact "Dima_flights_LR_only2"
