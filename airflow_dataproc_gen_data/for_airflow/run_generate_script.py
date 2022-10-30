from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.hooks import SSHHook
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
}

dag = DAG('hello_connections1',
        schedule_interval='* * * * *' ,
        default_args=default_args
    )

sshHook = SSHHook(remote_host='10.129.0.33', port='22', username='ubuntu', key_file='/home/dima/.ssh/id.rsa')
linux_command = "sh /home/ubuntu/MLOps/airflow_dataproc_gen_data/for_dataproc/generate.sh"

t1 = SSHOperator(
    ssh_hook=sshHook,
    task_id='test_remote_script',
    command=linux_command,
    dag=dag)