# To do
- [x] Trigger dag with next execution time (e.g. Trigger in next 5 minutes, 1 hour, ...) completed
    - <mark>Toggle on</mark> the DAG you want to use at http://localhost:8080
    - Run [trigger_dag.py](Airflow_API/trigger_dag.py)
        - Modify the dag_id you want to trigger at [line 29](https://gitlab.com/TianHuijun/airflow-demo/-/blob/main/Airflow_API/trigger_dag.py#L29)
        - Modify the logical_date (this is the next execution time) at [line 36](https://gitlab.com/TianHuijun/airflow-demo/-/blob/main/Airflow_API/trigger_dag.py#L36)
- [ ] Xcom in DockerOperator

# How to use Airflow API
## Create environment
- First create conda environment
```bash
conda create -n airflow python=3.9.7
```

```bash
conda activate airflow
```

- Install requirement
```bash
pip install -r requirement.txt
```

- Now we can controlling airflow what ever we want using [these API](https://github.com/apache/airflow-client-python/tree/main/airflow_client#documentation-for-api-endpoints)
    - **Note**: The table in above link have 4 columns: Class, Method, HTTP request, Description

        (The display of some devices may not show <mark>Description</mark> column, we need to *scroll horizontally to the right*)
        | Class | Method | HTTP request | Description |
        | ------ | ------ | ------ | ------ |
        |  |  |  |  |
    - <ins>First modification is</ins>: add `as client` in the library import in the following line
        ```python
        import airflow_client.client as client
        ```
    - <ins>Next modification</ins>: you must modify the `configuration` in all example code in Method column like this:

        Change
        ```python
        configuration = client.Configuration(
            host = "/api/v1"
        )

        configuration = client.Configuration(
            username = 'YOUR_USERNAME',
            password = 'YOUR_PASSWORD'
        )
        ```
        to this:
        ```python
        configuration = client.Configuration(
            host="http://0.0.0.0:8080/api/v1",  # depend on your setup
            username = 'airflow',
            password = 'airflow'
        )
        ```

## Source
https://github.com/apache/airflow-client-python
