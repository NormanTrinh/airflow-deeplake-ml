# Airflow + Deeplake Example Pipeline for Machine Learning (Local Development)

This repository provides an example Apache Airflow pipeline and Deeplake for local development of machine learning projects. The pipeline demonstrates how to load dataset and parse into Deeplake.

## Overview
In this example, we leverage Apache Airflow to automate the following steps:

1. create_deep_lake_data: The pipeline retrieves images and annotations from a folder and then prepares them for Deeplake.

2. show_example_in_deeplake: Show the image with the bounding box from Deeplake dataset

The first and second tasks are executed in separate Docker-containers. By deploying the first two tasks in separate containers, we ensure efficient resource utilization and maintain modularity in the pipeline's execution environment. 

## Usage
To use this pipeline for local development, follow the steps below:

1. Ensure that your Docker Engine has sufficient memory allocated, as running the pipeline may require more memory in certain cases.

2. Сhange path to your local repo in `dags/test_dag.py`. Replace "<absolute_path_to_your_airflow-ml_repo>/data" and "<absolute_path_to_your_airflow-ml_repo>/results" with your path.

3. Before the first Airflow run, prepare the environment by executing the following steps:

    - If you are working on Linux, specify the AIRFLOW_UID by running the command:

    ```bash
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```
    - Perform the database migration and create the initial user account by running the command:

    ```bash
    docker compose up airflow-init
    ```
    The created user account will have the login `airflow` and the password `airflow`.

4. Start Airflow and build custom images to run tasks in Docker-containers:

    ```bash
    docker compose up --build
    ```

5. Access the Airflow web interface in your browser at http://localhost:8080.

6. Trigger the DAG `convert_to_deeplake` to initiate the pipeline execution.

7. When you are finished working and want to clean up your environment, run:

    ```bash
    docker compose down --volumes --rmi all
    ```
    
## To do
- [x] Create API manual in [Airflow_API](Airflow_API) folder
- [x] Trigger dag with next execution time (e.g. Trigger in next 5 minutes, 1 hour, ...) completed
    - <mark>Toggle on</mark> the DAG you want to use at http://localhost:8080
    - Run [trigger_dag.py](Airflow_API/trigger_dag.py)
        - Modify the dag_id you want to trigger at [line 29](https://github.com/TianHuijun/airflow-deeplake-ml/blob/test_img/Airflow_API/trigger_dag.py#L29)
        - Modify the execution_time (this is the next execution time) at [line 32](https://github.com/TianHuijun/airflow-deeplake-ml/blob/test_img/Airflow_API/trigger_dag.py#L32), you may have to modify logical_date at [line 36](https://github.com/TianHuijun/airflow-deeplake-ml/blob/test_img/Airflow_API/trigger_dag.py#L36)
- [ ] XCom in DockerOperator

