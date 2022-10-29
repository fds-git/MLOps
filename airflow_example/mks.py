from airflow import DAG
from airflow.utils.dates import days_ago
# from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator
import requests
import json


def get_mks_data():
    """
    Function that returns mks geoposition from open-notify API
    """

    url_response = requests.get('http://api.open-notify.org/iss-now.json')
    dict_of_values = json.loads(url_response.text)

    longitude = dict_of_values['iss_position']['longitude']
    latitude = dict_of_values['iss_position']['latitude']
    timestamp = dict_of_values['timestamp']
    message = dict_of_values['message']

    # population_string = """ INSERT INTO mks_position 
    #                         (longtitude, latitude, created_at, message) 
    #                         VALUES ({0}, {1}, {2}, '{3}');
    #                     """ \
    #                     .format(longitude, latitude, timestamp, message)

    # return population_string
    print("ISS is now at {}, {}".format(longitude, latitude))


args = {
    'owner': 'airflow',
}

dag = DAG(
    dag_id='mks_geo',
    default_args=args,
    schedule_interval='*/30 * * * *',
    start_date=days_ago(2),
    tags=['API'],
)

# populate_pet_table = PostgresOperator(
#     task_id="mks_data",
#     postgres_conn_id="yandex_postgresql",
#     sql=get_mks_data(),
#     dag=dag
# )
print_geo = PythonOperator(task_id='get_and_print_coordinates', 
                            python_callable=get_mks_data, dag=dag)

print_geo
