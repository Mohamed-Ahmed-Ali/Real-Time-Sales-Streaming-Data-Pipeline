# dags/order_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from plugins.operators.kafka_producer_operator import KafkaProducerOperator
from data_generator import generate_order
import random
import time

default_args = {
    'owner': 'Mohamed-Ali',
    'start_date': datetime(2023, 1, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'order_dag',
    default_args=default_args,
    description='An example Airflow DAG for producing orders to Kafka',
    schedule_interval=timedelta(minutes=5),
)

def generate_and_produce_order():
    dummy_message = generate_order()
    print(f'Producing message @ {datetime.now()} | Message = {str(dummy_message)}')
    return dummy_message

task_generate_order = PythonOperator(
    task_id='generate_order',
    python_callable=generate_and_produce_order,
    dag=dag,
)

task_produce_to_kafka = KafkaProducerOperator(
    task_id='produce_to_kafka',
    bootstrap_servers=['172.18.0.4:9092'],
    topic='Order',
    message="{{ task_instance.xcom_pull(task_ids='generate_order') }}",
    provide_context=True,
    dag=dag,
)

task_generate_order >> task_produce_to_kafka
