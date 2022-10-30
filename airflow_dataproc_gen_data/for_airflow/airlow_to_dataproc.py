from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.hooks import SSHHook
from datetime import datetime, timedelta

dag = DAG('hello_connections1',
        schedule_interval='* * * * *' ,
        default_args=default_args
    )

sshHook = SSHHook(remote_host='10.129.0.33', usrname='ubuntu', key_file='/opt/airflow/keys/ssh.key')
linux_command = "sh /home/ec2-user/my_test.sh "

t1 = SSHOperator(
    ssh_hook=sshHook,
    task_id='test_remote_script',
    command=linux_command,
    dag=dag)
