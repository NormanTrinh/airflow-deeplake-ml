import time
import airflow_client.client as client
from airflow_client.client.api import dag_run_api
from airflow_client.client.model.dag_run import DAGRun
from airflow_client.client.model.error import Error
from airflow.utils.dates import days_ago, datetime
from datetime import timedelta
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: Basic
configuration = client.Configuration(
    host="http://0.0.0.0:8080/api/v1",
    username = 'airflow',
    password = 'airflow'
)

# Enter a context with an instance of the API client
with client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = dag_run_api.DAGRunApi(api_client)
    dag_id = "convert_to_deeplake" # str | The DAG ID.

    # Calculate the execution time in the next 10 seconds
    execution_time = datetime.utcnow() + timedelta(seconds=10)
    
    dag_run = DAGRun(
        # dag_run_id="dag_run_id_example",  #set id for dag, if not set, the id will look like this: manual__2023-08-14T01:18:46+00:00
        logical_date=days_ago(0, hour=execution_time.hour, minute=execution_time.minute, second=execution_time.second),
        # conf={},
        # note="note_example",
    ) # DAGRun | 

    # example passing only required values which don't have defaults set
    try:
        # Trigger a new DAG run
        api_response = api_instance.post_dag_run(dag_id, dag_run)
        pprint(api_response)
    except client.ApiException as e:
        print("Exception when calling DAGRunApi->post_dag_run: %s\n" % e)
