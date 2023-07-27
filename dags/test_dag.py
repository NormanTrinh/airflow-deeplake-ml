from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

# Define path to data
data_path = "/opt/airflow/data/animals_od"
saved_path = "/opt/airflow/results"
deeplake_path = saved_path + '/' + data_path.split('/')[-1] + '_deeplake'
# pred_data_path = "/opt/airflow/data/predict/labels__{{ ds }}.json"
# result_data_path = "/opt/airflow/data/predict/result__{{ ds }}.json"

# Define keyword arguments to use for all DockerOperator tasks
dockerops_kwargs = {
    "mount_tmp_dir": False,
    "mounts": [
        Mount(
            source="/home/dev1/Desktop/airflow-ml/data", # Change to your absolute path
            target="/opt/airflow/data/",
            type="bind",
        ),
        Mount(
            source="/home/dev1/Desktop/airflow-ml/results", # Change to your absolute path
            target="/opt/airflow/results",
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
        task_id="create_deep_lake_data",
        container_name="task__create_data",
        image="load_and_convert:latest",
        auto_remove = True,
        command=f"python data_load.py --data_path {data_path} --saved_path {saved_path}",
        **dockerops_kwargs,
    )

    # Task 2
    show_result = DockerOperator(
        task_id="show_example_in_deeplake",
        container_name="task__show_data",
        image="show_visualize_deeplake:latest",
        auto_remove = True,
        command=f"python show.py --deeplake_path {deeplake_path} --saved_path {saved_path}",
        **dockerops_kwargs,
    )

    # # Task 3
    # news_by_topic = PythonOperator(
    #     task_id="news_by_topic",
    #     python_callable=aggregate_predictions,
    #     op_kwargs={
    #         "pred_data_path": pred_data_path,
    #         "result_data_path": result_data_path,
    #     },
    # )

    # news_load >> news_label >> news_by_topic
    load_images >> show_result
    
taskflow()
