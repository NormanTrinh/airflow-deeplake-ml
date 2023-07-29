import time
import airflow_client.client as client
from airflow_client.client.api import permission_api
from airflow_client.client.model.action_collection import ActionCollection
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
    host="http://localhost:8080/api/v1",
    username = 'YOUR_USERNAME',
    password = 'YOUR_PASSWORD'
)

# Enter a context with an instance of the API client
with client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = permission_api.PermissionApi(api_client)
    limit = 100 # int | The numbers of items to return. (optional) if omitted the server will use the default value of 100
    offset = 0 # int | The number of items to skip before starting to collect the result set. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List permissions
        api_response = api_instance.get_permissions(limit=limit, offset=offset)
        pprint(api_response)
    except client.ApiException as e:
        print("Exception when calling PermissionApi->get_permissions: %s\n" % e)