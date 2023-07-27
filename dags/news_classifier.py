from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

from utils import aggregate_predictions

# Define path to data
raw_data_path = "/opt/airflow/data/raw/data__{{ ds }}.csv"
pred_data_path = "/opt/airflow/data/predict/labels__{{ ds }}.json"
result_data_path = "/opt/airflow/data/predict/result__{{ ds }}.json"

# Define keyword arguments to use for all DockerOperator tasks
dockerops_kwargs = {
    "mount_tmp_dir": False,
    "mounts": [
        Mount(
            source="/home/dev1/Desktop/airflow-ml/data", # Change to your absolute path
            target="/opt/airflow/data/",
            type="bind",
        )
    ],
    "retries": 1,
    "api_version": "1.30",
    "docker_url": "tcp://docker-socket-proxy:2375", 
    "network_mode": "bridge",
}


# Create DAG
@dag("convert_to_deeplake", start_date=days_ago(0), schedule="@daily", catchup=False)
def taskflow():
    # Task 1
    load_images = DockerOperator(
        task_id="load_images",
        container_name="task__images_load",
        image="load_and_convert:latest",
        auto_remove = True,
        command=f"python data_load.py --data_path {raw_data_path}",
        **dockerops_kwargs,
    )

    # Task 2
    news_label = DockerOperator(
        task_id="news_label",
        container_name="task__news_label",
        image="model-prediction:latest",
        auto_remove = True,
        command=f"python model_predict.py --data_path {raw_data_path} --pred_path {pred_data_path}",
        **dockerops_kwargs,
    )

    # Task 3
    news_by_topic = PythonOperator(
        task_id="news_by_topic",
        python_callable=aggregate_predictions,
        op_kwargs={
            "pred_data_path": pred_data_path,
            "result_data_path": result_data_path,
        },
    )

    news_load >> news_label >> news_by_topic

    
taskflow()
