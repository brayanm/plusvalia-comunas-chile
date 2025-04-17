from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Importar scripts ETL
import sys
sys.path.append('/opt/airflow/etl')  # Añadir la carpeta etl al sys.path
from extract_avaluos import extract_avaluos
from extract_geodata import extract_geodata
from transform_cruces import transformar_datos
from load_outputs import guardar_resultados

# Configuración básica del DAG
default_args = {
    'owner': 'Brayan Miranda',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='plusvalia_pipeline',
    default_args=default_args,
    description='Pipeline ETL de Plusvalía Inmobiliaria en Chile',
    schedule_interval=None,  # Puede cambiarse a un cron como '0 6 * * *'
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['plusvalia', 'chile', 'etl']
) as dag:

    # Tareas de extracción
    task_extract_avaluos = PythonOperator(
        task_id='extract_avaluos',
        python_callable=extract_avaluos
    )

    task_extract_geodata = PythonOperator(
        task_id='extract_geodata',
        python_callable=extract_geodata
    )

    # Tarea de transformación
    task_transform = PythonOperator(
        task_id='transform_cruces',
        python_callable=transformar_datos
    )

    # Tarea de carga
    task_load_outputs = PythonOperator(
        task_id='load_outputs',
        python_callable=guardar_resultados
    )

    # Definir la secuencia del pipeline
    task_extract_avaluos >> task_extract_geodata >> task_transform >> task_load_outputs
