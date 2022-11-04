from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(minutes=1)
}

dag = DAG('generate_data',
        schedule_interval='* * * * *' ,
        default_args=default_args
    )

sshHook = SSHHook(remote_host='10.129.0.20', port='22', username='ubuntu', key_file='/home/dima/id_rsa')

# После .sh обязательно пробел
linux_command = 'bash /home/ubuntu/MLOps/airflow_dataproc_gen_data/for_dataproc/generate.sh '
#linux_command = """echo 'Hello'"""

t1 = SSHOperator(
    ssh_hook=sshHook,
    task_id='run_generate',
    command=linux_command,
    dag=dag)
