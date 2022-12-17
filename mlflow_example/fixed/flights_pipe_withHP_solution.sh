spark-submit \
--jars mlflow-spark-1.27.0.jar \
flights_pipe_withHP_solution.py \
--train_artifact "s3a://mlflowbucket/flights_larger.csv" \
--output_artifact "Fedorov_flights_pipe_withHP"
