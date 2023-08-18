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
    - Select the method we want to use in this table
 
      | Class | Method | HTTP request | Description |
      | ------ | ------ | ------ | ------ |
      | ... | ... | ... | ... |

      **Note**: That table from [this link](https://github.com/apache/airflow-client-python/tree/main/airflow_client#documentation-for-api-endpoints) have 4 columns: Class, Method, HTTP request, Description. The display of some devices may not show <mark>Description</mark> column, we need to *scroll horizontally to the right*

        
    - <ins>First modification</ins>: after selected the method we want to use, in their example code, from the library import, add `as client` in the following line
        ```python
        import airflow_client.client as client
        ```
    - <ins>Next modification</ins>: we must modify the `configuration` variable in that code like this:

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
