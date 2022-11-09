# auth_client.AdminApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**auth_admin_v1_change_role_post**](AdminApi.md#auth_admin_v1_change_role_post) | **POST** /auth/admin/v1/change-role | Change Role
[**auth_admin_v1_create_role_post**](AdminApi.md#auth_admin_v1_create_role_post) | **POST** /auth/admin/v1/create-role | Create Role
[**auth_admin_v1_delete_role_delete**](AdminApi.md#auth_admin_v1_delete_role_delete) | **DELETE** /auth/admin/v1/delete-role | Delete Role
[**auth_admin_v1_get_all_roles_get**](AdminApi.md#auth_admin_v1_get_all_roles_get) | **GET** /auth/admin/v1/get-all-roles | Get All Roles
[**auth_admin_v1_set_user_role_post**](AdminApi.md#auth_admin_v1_set_user_role_post) | **POST** /auth/admin/v1/set-user-role | Set User Role


# **auth_admin_v1_change_role_post**
> bool, date, datetime, dict, float, int, list, str, none_type auth_admin_v1_change_role_post()

Change Role

### Example

* Bearer Authentication (BearerAuth):

```python
import time
import auth_client
from auth_client.api import admin_api
from auth_client.model.http_error import HTTPError
from auth_client.model.validation_error import ValidationError
from auth_client.model.change_role_in import ChangeRoleIn
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = auth_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = auth_client.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with auth_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = admin_api.AdminApi(api_client)
    change_role_in = ChangeRoleIn(
        new_role_permissions=[
            "new_role_permissions_example",
        ],
        new_role_name="new_role_name_example",
        old_role_name="old_role_name_example",
    ) # ChangeRoleIn |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Change Role
        api_response = api_instance.auth_admin_v1_change_role_post(change_role_in=change_role_in)
        pprint(api_response)
    except auth_client.ApiException as e:
        print("Exception when calling AdminApi->auth_admin_v1_change_role_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **change_role_in** | [**ChangeRoleIn**](ChangeRoleIn.md)|  | [optional]

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Validation error |  -  |
**401** | Authentication error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_admin_v1_create_role_post**
> CreateRoleOut auth_admin_v1_create_role_post()

Create Role

### Example

* Bearer Authentication (BearerAuth):

```python
import time
import auth_client
from auth_client.api import admin_api
from auth_client.model.create_role_in import CreateRoleIn
from auth_client.model.http_error import HTTPError
from auth_client.model.validation_error import ValidationError
from auth_client.model.create_role_out import CreateRoleOut
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = auth_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = auth_client.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with auth_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = admin_api.AdminApi(api_client)
    create_role_in = CreateRoleIn(
        role_name="role_name_example",
        permissions=[
            "permissions_example",
        ],
    ) # CreateRoleIn |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create Role
        api_response = api_instance.auth_admin_v1_create_role_post(create_role_in=create_role_in)
        pprint(api_response)
    except auth_client.ApiException as e:
        print("Exception when calling AdminApi->auth_admin_v1_create_role_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_role_in** | [**CreateRoleIn**](CreateRoleIn.md)|  | [optional]

### Return type

[**CreateRoleOut**](CreateRoleOut.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Validation error |  -  |
**401** | Authentication error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_admin_v1_delete_role_delete**
> bool, date, datetime, dict, float, int, list, str, none_type auth_admin_v1_delete_role_delete()

Delete Role

### Example

* Bearer Authentication (BearerAuth):

```python
import time
import auth_client
from auth_client.api import admin_api
from auth_client.model.http_error import HTTPError
from auth_client.model.validation_error import ValidationError
from auth_client.model.delete_role_in import DeleteRoleIn
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = auth_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = auth_client.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with auth_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = admin_api.AdminApi(api_client)
    delete_role_in = DeleteRoleIn(
        role_name="role_name_example",
    ) # DeleteRoleIn |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Role
        api_response = api_instance.auth_admin_v1_delete_role_delete(delete_role_in=delete_role_in)
        pprint(api_response)
    except auth_client.ApiException as e:
        print("Exception when calling AdminApi->auth_admin_v1_delete_role_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **delete_role_in** | [**DeleteRoleIn**](DeleteRoleIn.md)|  | [optional]

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Validation error |  -  |
**401** | Authentication error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_admin_v1_get_all_roles_get**
> [GetAllRolesOut] auth_admin_v1_get_all_roles_get()

Get All Roles

### Example

* Bearer Authentication (BearerAuth):

```python
import time
import auth_client
from auth_client.api import admin_api
from auth_client.model.get_all_roles_out import GetAllRolesOut
from auth_client.model.http_error import HTTPError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = auth_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = auth_client.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with auth_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = admin_api.AdminApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get All Roles
        api_response = api_instance.auth_admin_v1_get_all_roles_get()
        pprint(api_response)
    except auth_client.ApiException as e:
        print("Exception when calling AdminApi->auth_admin_v1_get_all_roles_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[GetAllRolesOut]**](GetAllRolesOut.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**401** | Authentication error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_admin_v1_set_user_role_post**
> bool, date, datetime, dict, float, int, list, str, none_type auth_admin_v1_set_user_role_post()

Set User Role

### Example

* Bearer Authentication (BearerAuth):

```python
import time
import auth_client
from auth_client.api import admin_api
from auth_client.model.set_user_role_in import SetUserRoleIn
from auth_client.model.http_error import HTTPError
from auth_client.model.validation_error import ValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = auth_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = auth_client.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with auth_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = admin_api.AdminApi(api_client)
    set_user_role_in = SetUserRoleIn(
        role="role_example",
        email="email_example",
    ) # SetUserRoleIn |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Set User Role
        api_response = api_instance.auth_admin_v1_set_user_role_post(set_user_role_in=set_user_role_in)
        pprint(api_response)
    except auth_client.ApiException as e:
        print("Exception when calling AdminApi->auth_admin_v1_set_user_role_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **set_user_role_in** | [**SetUserRoleIn**](SetUserRoleIn.md)|  | [optional]

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Validation error |  -  |
**401** | Authentication error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

