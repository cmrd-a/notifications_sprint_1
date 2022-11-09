# auth_client.UserApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**auth_users_v1_change_password_post**](UserApi.md#auth_users_v1_change_password_post) | **POST** /auth/users/v1/change-password | Change Password
[**auth_users_v1_get_permissions_get**](UserApi.md#auth_users_v1_get_permissions_get) | **GET** /auth/users/v1/get-permissions | Get Permissions
[**auth_users_v1_login_history_get**](UserApi.md#auth_users_v1_login_history_get) | **GET** /auth/users/v1/login-history | Login History
[**auth_users_v1_login_post**](UserApi.md#auth_users_v1_login_post) | **POST** /auth/users/v1/login | Login
[**auth_users_v1_logout_delete**](UserApi.md#auth_users_v1_logout_delete) | **DELETE** /auth/users/v1/logout | Logout
[**auth_users_v1_refresh_post**](UserApi.md#auth_users_v1_refresh_post) | **POST** /auth/users/v1/refresh | Refresh
[**auth_users_v1_register_post**](UserApi.md#auth_users_v1_register_post) | **POST** /auth/users/v1/register | Register


# **auth_users_v1_change_password_post**
> auth_users_v1_change_password_post()

Change Password

### Example

* Bearer Authentication (BearerAuth):

```python
import time
import auth_client
from auth_client.api import user_api
from auth_client.model.http_error import HTTPError
from auth_client.model.validation_error import ValidationError
from auth_client.model.change_password_in import ChangePasswordIn
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
    api_instance = user_api.UserApi(api_client)
    change_password_in = ChangePasswordIn(
        current_password="current_password_example",
        new_password="new_password_example",
    ) # ChangePasswordIn |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Change Password
        api_instance.auth_users_v1_change_password_post(change_password_in=change_password_in)
    except auth_client.ApiException as e:
        print("Exception when calling UserApi->auth_users_v1_change_password_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **change_password_in** | [**ChangePasswordIn**](ChangePasswordIn.md)|  | [optional]

### Return type

void (empty response body)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful response |  -  |
**400** | Validation error |  -  |
**401** | Authentication error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_users_v1_get_permissions_get**
> GetPermissionsOut auth_users_v1_get_permissions_get()

Get Permissions

### Example

* Bearer Authentication (BearerAuth):

```python
import time
import auth_client
from auth_client.api import user_api
from auth_client.model.http_error import HTTPError
from auth_client.model.get_permissions_out import GetPermissionsOut
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
    api_instance = user_api.UserApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get Permissions
        api_response = api_instance.auth_users_v1_get_permissions_get()
        pprint(api_response)
    except auth_client.ApiException as e:
        print("Exception when calling UserApi->auth_users_v1_get_permissions_get: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**GetPermissionsOut**](GetPermissionsOut.md)

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

# **auth_users_v1_login_history_get**
> [LoginHistoryOut] auth_users_v1_login_history_get()

Login History

### Example

* Bearer Authentication (BearerAuth):

```python
import time
import auth_client
from auth_client.api import user_api
from auth_client.model.login_history_out import LoginHistoryOut
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
    api_instance = user_api.UserApi(api_client)
    page_size = 100 # int |  (optional) if omitted the server will use the default value of 100
    page_number = 1 # int |  (optional) if omitted the server will use the default value of 1

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Login History
        api_response = api_instance.auth_users_v1_login_history_get(page_size=page_size, page_number=page_number)
        pprint(api_response)
    except auth_client.ApiException as e:
        print("Exception when calling UserApi->auth_users_v1_login_history_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**|  | [optional] if omitted the server will use the default value of 100
 **page_number** | **int**|  | [optional] if omitted the server will use the default value of 1

### Return type

[**[LoginHistoryOut]**](LoginHistoryOut.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Validation error |  -  |
**401** | Authentication error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_users_v1_login_post**
> LoginRefreshOut auth_users_v1_login_post()

Login

### Example


```python
import time
import auth_client
from auth_client.api import user_api
from auth_client.model.login_refresh_out import LoginRefreshOut
from auth_client.model.validation_error import ValidationError
from auth_client.model.email_password_in import EmailPasswordIn
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = auth_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with auth_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    email_password_in = EmailPasswordIn(
        password="password_example",
        email="email_example",
    ) # EmailPasswordIn |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Login
        api_response = api_instance.auth_users_v1_login_post(email_password_in=email_password_in)
        pprint(api_response)
    except auth_client.ApiException as e:
        print("Exception when calling UserApi->auth_users_v1_login_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **email_password_in** | [**EmailPasswordIn**](EmailPasswordIn.md)|  | [optional]

### Return type

[**LoginRefreshOut**](LoginRefreshOut.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful response |  -  |
**400** | Validation error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **auth_users_v1_logout_delete**
> bool, date, datetime, dict, float, int, list, str, none_type auth_users_v1_logout_delete()

Logout

### Example

* Bearer Authentication (BearerAuth):

```python
import time
import auth_client
from auth_client.api import user_api
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
    api_instance = user_api.UserApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Logout
        api_response = api_instance.auth_users_v1_logout_delete()
        pprint(api_response)
    except auth_client.ApiException as e:
        print("Exception when calling UserApi->auth_users_v1_logout_delete: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

**bool, date, datetime, dict, float, int, list, str, none_type**

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

# **auth_users_v1_refresh_post**
> LoginRefreshOut auth_users_v1_refresh_post()

Refresh

### Example

* Bearer Authentication (BearerAuth):

```python
import time
import auth_client
from auth_client.api import user_api
from auth_client.model.login_refresh_out import LoginRefreshOut
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
    api_instance = user_api.UserApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Refresh
        api_response = api_instance.auth_users_v1_refresh_post()
        pprint(api_response)
    except auth_client.ApiException as e:
        print("Exception when calling UserApi->auth_users_v1_refresh_post: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**LoginRefreshOut**](LoginRefreshOut.md)

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

# **auth_users_v1_register_post**
> auth_users_v1_register_post()

Register

### Example


```python
import time
import auth_client
from auth_client.api import user_api
from auth_client.model.validation_error import ValidationError
from auth_client.model.email_password_in import EmailPasswordIn
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = auth_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with auth_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = user_api.UserApi(api_client)
    email_password_in = EmailPasswordIn(
        password="password_example",
        email="email_example",
    ) # EmailPasswordIn |  (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Register
        api_instance.auth_users_v1_register_post(email_password_in=email_password_in)
    except auth_client.ApiException as e:
        print("Exception when calling UserApi->auth_users_v1_register_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **email_password_in** | [**EmailPasswordIn**](EmailPasswordIn.md)|  | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful response |  -  |
**400** | Validation error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

