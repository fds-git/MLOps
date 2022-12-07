# if you plan to run this script file
# don't forget to provide neccessary execution rights, i.e.
# chmode +x ./flights_LR_only_exercise.sh

#Change names in <> for the correct values

spark-submit \
--jars mlflow-spark-1.27.0.jar \
<Your main app file>.py \
--train_artifact "s3a://mlflow-test/data/flights-larger.csv" \
--output_artifact <Your folder name with the model>