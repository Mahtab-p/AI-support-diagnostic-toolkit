# Import the API request function so we can test
# real responses from api_client.py
from api_client import send_get_request


# --------------------------------------------------
# Diagnose HTTP status codes
# --------------------------------------------------
def diagnose_status(status_code):

    if 200 <= status_code < 300:
        return {
            "error_code": status_code,
            "category": "Success",
            "diagnosis": "API request successful.",
            "severity": "None"
        }

    elif status_code == 400:
        return {
            "error_code": status_code,
            "category": "Client Error",
            "diagnosis": "Bad API request.",
            "severity": "Medium"
        }

    elif status_code == 401:
        return {
            "error_code": status_code,
            "category": "Authentication",
            "diagnosis": "Authentication failure.",
            "severity": "High"
        }

    elif status_code == 403:
        return {
            "error_code": status_code,
            "category": "Authorization",
            "diagnosis": "Authorization failure.",
            "severity": "High"
        }

    elif status_code == 404:
        return {
            "error_code": status_code,
            "category": "Resource",
            "diagnosis": "Requested API resource not found.",
            "severity": "Medium"
        }

    elif status_code == 405:
        return {
            "error_code": status_code,
            "category": "HTTP Method",
            "diagnosis": "HTTP method not allowed.",
            "severity": "Medium"
        }

    elif status_code == 408:
        return {
            "error_code": status_code,
            "category": "Timeout",
            "diagnosis": "API request timeout.",
            "severity": "Medium"
        }

    elif status_code == 409:
        return {
            "error_code": status_code,
            "category": "Conflict",
            "diagnosis": "API resource conflict.",
            "severity": "Medium"
        }

    elif status_code == 422:
        return {
            "error_code": status_code,
            "category": "Validation",
            "diagnosis": "API request validation failure.",
            "severity": "Medium"
        }

    elif status_code == 429:
        return {
            "error_code": status_code,
            "category": "Rate Limit",
            "diagnosis": "API rate limit exceeded.",
            "severity": "Medium"
        }

    elif status_code == 500:
        return {
            "error_code": status_code,
            "category": "Server Error",
            "diagnosis": "Internal API server error.",
            "severity": "High"
        }

    elif status_code == 502:
        return {
            "error_code": status_code,
            "category": "Gateway Error",
            "diagnosis": "API gateway failure.",
            "severity": "High"
        }

    elif status_code == 503:
        return {
            "error_code": status_code,
            "category": "Service Availability",
            "diagnosis": "API service unavailable.",
            "severity": "High"
        }

    elif status_code == 504:
        return {
            "error_code": status_code,
            "category": "Gateway Timeout",
            "diagnosis": "API gateway timeout.",
            "severity": "High"
        }

    else:
        return {
            "error_code": status_code,
            "category": "Unknown",
            "diagnosis": "Unknown API response.",
            "severity": "Unknown"
        }


# --------------------------------------------------
# Diagnose request-level errors
# These happen when a usable HTTP response
# may not be received.
# --------------------------------------------------
def diagnose_request_error(error_type):

    if error_type == "Timeout":
        return {
            "error_code": "Timeout",
            "category": "Network / Performance",
            "diagnosis": "API request timeout.",
            "severity": "Medium"
        }

    elif error_type == "ConnectionError":
        return {
            "error_code": "ConnectionError",
            "category": "Connectivity",
            "diagnosis": "API connection failure.",
            "severity": "High"
        }

    elif error_type == "RequestException":
        return {
            "error_code": "RequestException",
            "category": "Request Failure",
            "diagnosis": "API request failure.",
            "severity": "High"
        }

    else:
        return {
            "error_code": "Unknown",
            "category": "Unknown",
            "diagnosis": "Unknown API request failure.",
            "severity": "Unknown"
        }


# --------------------------------------------------
# Analyze the result returned from api_client.py
# --------------------------------------------------
def analyze_result(api_result):

    # If we received an HTTP response
    if api_result["success"]:
        return diagnose_status(
            api_result["status_code"]
        )

    # If the request failed before a usable
    # HTTP response was received
    return diagnose_request_error(
        api_result["error_type"]
    )


# --------------------------------------------------
# Analyze response speed
# --------------------------------------------------
def diagnose_response_time(response_time):

    if response_time < 1:
        return "Fast"

    elif response_time <= 2:
        return "Acceptable"

    elif response_time <= 5:
        return "Slow"

    else:
        return "Very Slow"


# --------------------------------------------------
# Print a clean diagnostic report
# --------------------------------------------------
def print_diagnostic_report(api_result):

    print("=" * 50)
    print("API DIAGNOSTIC REPORT")
    print("=" * 50)

    # Analyze the response or request error
    diagnosis = analyze_result(api_result)

    # ----------------------------------------------
    # Successful HTTP communication
    # ----------------------------------------------
    if api_result["success"]:

        print(f"URL: {api_result['url']}")

        print(
            f"HTTP Status Code: "
            f"{api_result['status_code']}"
        )

        print(
            f"Response Time: "
            f"{api_result['response_time']:.2f}s"
        )

        # Classify response speed
        performance = diagnose_response_time(
            api_result["response_time"]
        )

        print(f"Performance: {performance}")

        print(
            f"Content Type: "
            f"{api_result['content_type']}"
        )

        # Some APIs do not provide a request ID
        request_id = (
            api_result["request_id"]
            or "Not provided"
        )

        print(f"Request ID: {request_id}")

    # ----------------------------------------------
    # Network or request-level failure
    # ----------------------------------------------
    else:

        print(
            f"Error Code: "
            f"{api_result['error_type']}"
        )

        print(
            f"Error Message: "
            f"{api_result['message']}"
        )

    print("-" * 50)

    # General diagnosis only
    print(
        f"Diagnosis: "
        f"{diagnosis['diagnosis']}"
    )

    print(
        f"Category: "
        f"{diagnosis['category']}"
    )

    print(
        f"Severity: "
        f"{diagnosis['severity']}"
    )

    print("=" * 50)


# --------------------------------------------------
# Test this module only when diagnostics.py
# is executed directly.
# --------------------------------------------------
if __name__ == "__main__":

    print("\nREAL API TEST\n")

    api_result = send_get_request(
        "https://dummyjson.com/products/1"
    )

    print_diagnostic_report(api_result)
