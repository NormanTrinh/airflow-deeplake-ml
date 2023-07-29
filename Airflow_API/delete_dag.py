import time
import airflow_client.client as client
from airflow_client.client.api import dag_api
from airflow_client.client.model.error import Error
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
    api_instance = dag_api.DAGApi(api_client)
    dag_id = "dataset_produces_1" # str | The DAG ID.

    # example passing only required values which don't have defaults set
    try:
        # Delete a DAG
        api_instance.delete_dag(dag_id)
        print('DELETE successful!')
    except client.ApiException as e:
        print("Exception when calling DAGApi->delete_dag: %s\n" % e)