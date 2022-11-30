spark-submit \
--jars mlflow-spark-1.27.0.jar \
flights_LR_only_solution.py \
--train_artifact "s3a://mlflow-test/data/flights_larger.csv" \
--output_artifact "Student_Name_flights_LR_only2"