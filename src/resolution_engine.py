# Import the diagnostic report so we can display
# what happened before showing the solution
from diagnostics import print_diagnostic_report

# Import the API client so we can test a real endpoint
from api_client import send_get_request


# --------------------------------------------------
# Return troubleshooting guidance for HTTP responses
# --------------------------------------------------
def get_http_resolution(status_code):

    # 2xx means the API request succeeded
    if 200 <= status_code < 300:

        return {
            "likely_causes": [
                "No error detected."
            ],
            "recommended_actions": [
                "No corrective action is required."
            ],
            "escalation_required": False,
            "escalation_guidance":
                "No escalation is required."
        }


    # --------------------------------------------------
    # 400 - Bad Request
    # --------------------------------------------------
    elif status_code == 400:

        return {
            "likely_causes": [
                "Invalid JSON body.",
                "Missing required request field.",
                "Incorrect query parameter.",
                "Incorrect data type."
            ],

            "recommended_actions": [
                "Validate the request JSON.",
                "Check required fields.",
                "Verify parameter names.",
                "Compare the request with the API documentation."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if a valid request still returns HTTP 400."
        }


    # --------------------------------------------------
    # 401 - Authentication Failure
    # --------------------------------------------------
    elif status_code == 401:

        return {
            "likely_causes": [
                "Missing API token.",
                "Invalid API token.",
                "Expired API token.",
                "Incorrect authentication scheme."
            ],

            "recommended_actions": [
                "Verify the API token is configured.",
                "Check the Authorization header.",
                "Confirm the expected authentication format.",
                "Verify that the token has not expired.",
                "Confirm the correct environment is being used."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if valid credentials still return HTTP 401."
        }


    # --------------------------------------------------
    # 403 - Authorization Failure
    # --------------------------------------------------
    elif status_code == 403:

        return {
            "likely_causes": [
                "The account does not have permission.",
                "The API token lacks the required scope.",
                "The requested resource is restricted."
            ],

            "recommended_actions": [
                "Verify the user's permissions.",
                "Check API token scopes or roles.",
                "Confirm access to the requested resource."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if permissions are correct but access is still denied."
        }


    # --------------------------------------------------
    # 404 - Resource Not Found
    # --------------------------------------------------
    elif status_code == 404:

        return {
            "likely_causes": [
                "Incorrect endpoint.",
                "Incorrect resource ID.",
                "Resource does not exist.",
                "Incorrect API version."
            ],

            "recommended_actions": [
                "Verify the endpoint URL.",
                "Check the resource identifier.",
                "Confirm the API version.",
                "Compare the request with API documentation."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if the documented resource exists but still returns HTTP 404."
        }


    # --------------------------------------------------
    # 405 - Method Not Allowed
    # --------------------------------------------------
    elif status_code == 405:

        return {
            "likely_causes": [
                "Incorrect HTTP method.",
                "The endpoint does not support this operation."
            ],

            "recommended_actions": [
                "Verify whether the endpoint requires GET, POST, PUT, PATCH, or DELETE.",
                "Compare the HTTP method with the API documentation."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if the documented HTTP method is still rejected."
        }


    # --------------------------------------------------
    # 408 - Request Timeout
    # --------------------------------------------------
    elif status_code == 408:

        return {
            "likely_causes": [
                "The request took too long.",
                "Network latency is high.",
                "The server is processing slowly."
            ],

            "recommended_actions": [
                "Retry the request.",
                "Check network connectivity.",
                "Review request size.",
                "Check server performance if the issue continues."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if repeated HTTP 408 responses occur under normal network conditions."
        }


    # --------------------------------------------------
    # 409 - Conflict
    # --------------------------------------------------
    elif status_code == 409:

        return {
            "likely_causes": [
                "The resource already exists.",
                "The request conflicts with the current resource state."
            ],

            "recommended_actions": [
                "Review the current resource state.",
                "Check whether the resource already exists.",
                "Confirm the expected update workflow."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if the resource state looks correct but the conflict persists."
        }


    # --------------------------------------------------
    # 422 - Validation Error
    # --------------------------------------------------
    elif status_code == 422:

        return {
            "likely_causes": [
                "The JSON syntax is valid but the data is invalid.",
                "A required field contains an unsupported value.",
                "An API validation rule failed."
            ],

            "recommended_actions": [
                "Review API validation requirements.",
                "Check field values.",
                "Check field data types.",
                "Inspect the response body for validation details."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if valid documented data continues to fail validation."
        }


    # --------------------------------------------------
    # 429 - Rate Limit
    # --------------------------------------------------
    elif status_code == 429:

        return {
            "likely_causes": [
                "Too many requests were sent.",
                "The API quota was exceeded.",
                "Requests are being retried too aggressively."
            ],

            "recommended_actions": [
                "Check rate-limit headers.",
                "Check Retry-After if available.",
                "Reduce request frequency.",
                "Use retry logic with backoff.",
                "Review the account API limits."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if usage is below the documented limit but HTTP 429 continues."
        }


    # --------------------------------------------------
    # 500 - Internal Server Error
    # --------------------------------------------------
    elif status_code == 500:

        return {
            "likely_causes": [
                "Unexpected server-side failure.",
                "Application exception.",
                "Backend dependency failure."
            ],

            "recommended_actions": [
                "Capture the request ID.",
                "Retry the request once if appropriate.",
                "Check service logs or monitoring.",
                "Check service health.",
                "Collect request and response details."
            ],

            "escalation_required": True,

            "escalation_guidance":
                "Repeated HTTP 500 responses usually require server-side investigation."
        }


    # --------------------------------------------------
    # 502 - Bad Gateway
    # --------------------------------------------------
    elif status_code == 502:

        return {
            "likely_causes": [
                "Upstream service failure.",
                "Gateway or proxy problem.",
                "Invalid response from a backend service."
            ],

            "recommended_actions": [
                "Retry the request.",
                "Check upstream service health.",
                "Check gateway or proxy logs.",
                "Capture the request ID and timestamp."
            ],

            "escalation_required": True,

            "escalation_guidance":
                "Repeated HTTP 502 responses usually require backend or infrastructure investigation."
        }


    # --------------------------------------------------
    # 503 - Service Unavailable
    # --------------------------------------------------
    elif status_code == 503:

        return {
            "likely_causes": [
                "The service is temporarily unavailable.",
                "The service is overloaded.",
                "Maintenance may be in progress."
            ],

            "recommended_actions": [
                "Check service health.",
                "Retry after a short delay.",
                "Check Retry-After if provided.",
                "Capture the request ID and timestamp."
            ],

            "escalation_required": True,

            "escalation_guidance":
                "Repeated HTTP 503 responses should be escalated when the service should be available."
        }


    # --------------------------------------------------
    # 504 - Gateway Timeout
    # --------------------------------------------------
    elif status_code == 504:

        return {
            "likely_causes": [
                "An upstream service responded too slowly.",
                "A backend dependency timed out.",
                "Network latency exists between services."
            ],

            "recommended_actions": [
                "Retry the request.",
                "Check upstream service health.",
                "Check backend latency.",
                "Capture request timing and request ID."
            ],

            "escalation_required": True,

            "escalation_guidance":
                "Repeated HTTP 504 responses generally require backend or infrastructure investigation."
        }


    # --------------------------------------------------
    # Any status code not specifically supported
    # --------------------------------------------------
    else:

        return {
            "likely_causes": [
                "The HTTP response is not currently classified."
            ],

            "recommended_actions": [
                "Inspect the HTTP response.",
                "Review the API documentation.",
                "Capture request and response details."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if initial troubleshooting cannot explain the issue."
        }


# --------------------------------------------------
# Return troubleshooting guidance for errors where
# no usable HTTP response was received
# --------------------------------------------------
def get_request_error_resolution(error_type):

    # --------------------------------------------------
    # Python requests timeout
    # --------------------------------------------------
    if error_type == "Timeout":

        return {
            "likely_causes": [
                "Slow network connection.",
                "Slow API response.",
                "Configured timeout is too low.",
                "Backend processing is taking too long."
            ],

            "recommended_actions": [
                "Retry the request.",
                "Verify network connectivity.",
                "Review the configured timeout.",
                "Check API response performance."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if repeated timeouts occur under normal network conditions."
        }


    # --------------------------------------------------
    # Unable to establish a connection
    # --------------------------------------------------
    elif error_type == "ConnectionError":

        return {
            "likely_causes": [
                "Incorrect hostname.",
                "DNS resolution failure.",
                "Network connectivity problem.",
                "Firewall or proxy restriction.",
                "Remote service is unreachable."
            ],

            "recommended_actions": [
                "Verify the API hostname.",
                "Check internet or network connectivity.",
                "Test DNS resolution.",
                "Test the endpoint with curl or Postman.",
                "Review firewall or proxy configuration."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if the endpoint is valid and reachable from other systems but fails from this environment."
        }


    # --------------------------------------------------
    # Generic requests library failure
    # --------------------------------------------------
    elif error_type == "RequestException":

        return {
            "likely_causes": [
                "HTTP request configuration problem.",
                "Invalid URL.",
                "TLS or certificate problem.",
                "Unexpected HTTP request failure."
            ],

            "recommended_actions": [
                "Inspect the exception message.",
                "Verify the URL.",
                "Verify request configuration.",
                "Reproduce the request using curl or Postman."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if the request configuration is valid and the failure cannot be explained."
        }


    # --------------------------------------------------
    # Unknown request-level error
    # --------------------------------------------------
    else:

        return {
            "likely_causes": [
                "Unknown request failure."
            ],

            "recommended_actions": [
                "Inspect the exception details.",
                "Verify API configuration.",
                "Verify network connectivity."
            ],

            "escalation_required": False,

            "escalation_guidance":
                "Escalate if initial troubleshooting does not identify the problem."
        }


# --------------------------------------------------
# Decide which resolution function should be used
# --------------------------------------------------
def get_resolution(api_result):

    # If the API returned an HTTP response,
    # diagnose using the HTTP status code
    if api_result["success"]:

        return get_http_resolution(
            api_result["status_code"]
        )

    # Otherwise diagnose the request/network error
    return get_request_error_resolution(
        api_result["error_type"]
    )


# --------------------------------------------------
# Print the troubleshooting solution report
# --------------------------------------------------
def print_resolution_report(api_result):

    # Get the correct solution
    resolution = get_resolution(api_result)

    print("\nLIKELY CAUSES")
    print("-" * 50)

    # Print every possible cause
    for cause in resolution["likely_causes"]:
        print(f"- {cause}")

    print("\nRECOMMENDED ACTIONS")
    print("-" * 50)

    # Number every troubleshooting step
    for number, action in enumerate(
        resolution["recommended_actions"],
        start=1
    ):
        print(f"{number}. {action}")

    print("\nESCALATION")
    print("-" * 50)

    # Show whether escalation is currently recommended
    if resolution["escalation_required"]:
        print("Escalation Required: YES")

    else:
        print("Escalation Required: NO")

    print(
        f"Guidance: "
        f"{resolution['escalation_guidance']}"
    )

    print("=" * 50)


# --------------------------------------------------
# Test the complete diagnosis + resolution workflow
# only when this file is executed directly
# --------------------------------------------------
if __name__ == "__main__":

    # Send a real GET request
    api_result = send_get_request(
        "https://dummyjson.com/products/1"
    )

    # First show what happened
    print_diagnostic_report(api_result)

    # Then show what should be done
    print_resolution_report(api_result)

#=============>test result

#if __name__ == "__main__":

 #   test_result = {
  #      "success": True,
   #     "status_code": 401
    #}

   # print_resolution_report(test_result)
