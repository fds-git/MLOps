from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from datetime import datetime, timedelta

# minutes=2 - чтобы скрипт точно запустился
default_args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(minutes=2)
}

sshHook = SSHHook(remote_host='10.129.0.13', port='22', username='ubuntu', key_file='/home/dima/id_rsa', timeout=50)
generate_command = 'bash /home/ubuntu/MLOps/airflow_dataproc_mlflow/for_dataproc/generate.sh '
to_hdfs_command = 'bash /home/ubuntu/MLOps/airflow_dataproc_mlflow/for_dataproc/to_hdfs.sh '
process_command = 'bash /home/ubuntu/MLOps/airflow_dataproc_mlflow/for_dataproc/data_process.sh '
fit_command = 'bash /home/ubuntu/MLOps/airflow_dataproc_mlflow/for_dataproc/fit.sh '

with DAG('generate_data',
    schedule_interval='* * * * *' ,
    default_args=default_args
    ) as dag:

    generate_task = SSHOperator(
    ssh_hook=sshHook,
    task_id='run_generate',
    command=generate_command
    )

    to_hdfs_task = SSHOperator(
    ssh_hook=sshHook,
    task_id='run_to_hdfs',
    command=to_hdfs_command
    )

    process_task = SSHOperator(
    ssh_hook=sshHook,
    task_id='run_process',
    command=process_command
    )

    fit_task = SSHOperator(
    ssh_hook=sshHook,
    task_id='fit',
    command=fit_command
    )

    generate_task >> to_hdfs_task >> process_task >> fit_task
