import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri('http://158.160.15.5:8000')
client = MlflowClient()
experiment = client.get_experiment_by_name("Spark_Experiment")
experiment_id = experiment.experiment_id
print("Experiment_id: {}".format(experiment.experiment_id))
print("Artifact Location: {}".format(experiment.artifact_location))