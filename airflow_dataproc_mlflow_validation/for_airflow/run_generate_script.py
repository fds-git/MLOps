from airflow import DAG, XComArg
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from datetime import datetime, timedelta
from airflow.models import Variable
import base64
from airflow.operators.python import PythonOperator

# minutes=2 - чтобы скрипт точно запустился
default_args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(minutes=10)
}

# Результат функции можно будет получить через Xcom
def _decode_message(task_name, ti):
    message = ti.xcom_pull(task_ids=task_name)
    return base64.b64decode(message).decode()

# Загружаем переменные окружения
DATAPROC_IP = Variable.get("DATAPROC_IP")
DATAPROC_PORT = Variable.get("DATAPROC_PORT")
USERNAME = Variable.get("USERNAME")
KEY_FILE = Variable.get("KEY_FILE")

sshHook = SSHHook(remote_host=DATAPROC_IP, port=DATAPROC_PORT, username=USERNAME, key_file=KEY_FILE, timeout=1000)
generate_command = 'bash /home/ubuntu/MLOps/airflow_dataproc_mlflow_validation/for_dataproc/scripts/generate.sh '
to_hdfs_command = 'bash /home/ubuntu/MLOps/airflow_dataproc_mlflow_validation/for_dataproc/scripts/to_hdfs.sh {{ ti.xcom_pull(task_ids="decode_generated_file_name") }}'
process_command = 'bash /home/ubuntu/MLOps/airflow_dataproc_mlflow_validation/for_dataproc/scripts/data_process.sh {{ ti.xcom_pull(task_ids="decode_generated_file_name") }}'
fit_log_reg_command = 'bash /home/ubuntu/MLOps/airflow_dataproc_mlflow_validation/for_dataproc/scripts/fit_lr.sh {{ ti.xcom_pull(task_ids="decode_generated_file_name") }}'
fit_rand_for_command = 'bash /home/ubuntu/MLOps/airflow_dataproc_mlflow_validation/for_dataproc/scripts/fit_rf.sh {{ ti.xcom_pull(task_ids="decode_generated_file_name") }}'
ttest_command = 'bash /home/ubuntu/MLOps/airflow_dataproc_mlflow_validation/for_dataproc/scripts/ttest.sh '

with DAG('gen_data',
    schedule_interval='*/5 * * * *' ,
    default_args=default_args
    ) as dag:

    generate_task = SSHOperator(
    ssh_hook=sshHook,
    task_id='generate_data',
    command=generate_command,
    cmd_timeout=100
    )

    # Название сгенерированного файла надо декодировать
    # для передачи следующим таскам
    decoder = PythonOperator(
    task_id='decode_generated_file_name',
    python_callable=_decode_message,
    op_args=['generate_data'],
    )

    to_hdfs_task = SSHOperator(
    ssh_hook=sshHook,
    task_id='data_to_hdfs',
    command=to_hdfs_command
    )

    process_task = SSHOperator(
    ssh_hook=sshHook,
    task_id='process_data',
    command=process_command
    )

    fit_log_reg_task = SSHOperator(
    ssh_hook=sshHook,
    task_id='fit_log_reg',
    command=fit_log_reg_command,
    conn_timeout=1000,
    cmd_timeout=1000
    )

    fit_rand_for_task = SSHOperator(
    ssh_hook=sshHook,
    task_id='fit_rand_forest',
    command=fit_rand_for_command,
    conn_timeout=1000,
    cmd_timeout=1000
    )

    ttest_task = SSHOperator(
    ssh_hook=sshHook,
    task_id='ttest',
    command=ttest_command
    )

    generate_task >> decoder >> to_hdfs_task >> process_task >> [fit_log_reg_task, fit_rand_for_task] >> ttest_task
