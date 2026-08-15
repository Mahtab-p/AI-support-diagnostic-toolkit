# Import csv so we can read endpoint information
# from a CSV file
import csv

# Import the API request functions
from api_client import (
    send_get_request,
    send_post_request
)

# Import the diagnostic engine
from diagnostics import analyze_result

# Import the resolution engine
from resolution_engine import get_resolution


# --------------------------------------------------
# Read endpoint definitions from a CSV file
# --------------------------------------------------
def load_endpoints(file_path):

    # Create an empty list to store endpoints
    endpoints = []

    try:
        # Open the CSV file safely
        with open(
            file_path,
            newline="",
            encoding="utf-8"
        ) as file:

            # DictReader converts each CSV row
            # into a Python dictionary
            reader = csv.DictReader(file)

            # Loop through every row
            for row in reader:
                endpoints.append(row)

        # Return the complete endpoint list
        return endpoints

    except FileNotFoundError:

        print(
            f"ERROR: Endpoint file not found: "
            f"{file_path}"
        )

        # Return an empty list instead of crashing
        return []


# --------------------------------------------------
# Test one API endpoint
# --------------------------------------------------
def test_endpoint(endpoint):

    # Read information from the endpoint dictionary
    name = endpoint["name"]
    method = endpoint["method"].upper()
    url = endpoint["url"]

    print(f"\nTesting: {name}")
    print(f"Method: {method}")
    print(f"URL: {url}")

    # --------------------------------------------------
    # GET request
    # --------------------------------------------------
    if method == "GET":

        api_result = send_get_request(
            url
        )

    # --------------------------------------------------
    # POST request
    # --------------------------------------------------
    elif method == "POST":

        # Temporary sample JSON body
        payload = {
            "title": "AI Support Test"
        }

        api_result = send_post_request(
            url,
            payload
        )

    # --------------------------------------------------
    # Unsupported HTTP method
    # --------------------------------------------------
    else:

        return {
            "name": name,
            "method": method,
            "url": url,
            "success": False,
            "error_type": "UnsupportedMethod",
            "message": (
                f"HTTP method {method} "
                f"is not supported by this tool."
            )
        }

    # Add endpoint information to the API result
    # so we do not lose the service name or method
    api_result["name"] = name
    api_result["method"] = method

    return api_result


# --------------------------------------------------
# Combine raw API result + diagnosis + resolution
# --------------------------------------------------
def build_analysis_record(api_result):

    # Ask diagnostics.py what happened
    diagnosis = analyze_result(
        api_result
    )

    # Ask resolution_engine.py what should be done
    resolution = get_resolution(
        api_result
    )

    # Store everything together
    return {
        "api_result": api_result,
        "diagnosis": diagnosis,
        "resolution": resolution
    }


# --------------------------------------------------
# Test every endpoint from the CSV file
# --------------------------------------------------
def test_all_endpoints(file_path):

    # Load all endpoints
    endpoints = load_endpoints(
        file_path
    )

    # Store all completed analyses here
    results = []

    # Loop through every endpoint
    for endpoint in endpoints:

        # Send the API request
        api_result = test_endpoint(
            endpoint
        )

        # Diagnose and create resolution guidance
        analysis = build_analysis_record(
            api_result
        )

        # Add the final record to the result list
        results.append(
            analysis
        )

    return results


# --------------------------------------------------
# Print a readable result for every endpoint
# --------------------------------------------------
def print_results(results):

    print("\n" + "=" * 60)
    print("MULTI-ENDPOINT API TEST RESULTS")
    print("=" * 60)

    # Loop through every completed analysis
    for item in results:

        api_result = item["api_result"]
        diagnosis = item["diagnosis"]
        resolution = item["resolution"]

        print("\n" + "-" * 60)

        print(
            f"Service: "
            f"{api_result.get('name', 'Unknown')}"
        )

        print(
            f"Method: "
            f"{api_result.get('method', 'Unknown')}"
        )

        # --------------------------------------------------
        # If an HTTP response was received
        # --------------------------------------------------
        if api_result["success"]:

            print(
                f"HTTP Status: "
                f"{api_result['status_code']}"
            )

            print(
                f"Response Time: "
                f"{api_result['response_time']:.2f}s"
            )

        # --------------------------------------------------
        # If the request failed before a usable HTTP response
        # --------------------------------------------------
        else:

            print(
                f"Error Code: "
                f"{api_result['error_type']}"
            )

            print(
                f"Error Message: "
                f"{api_result.get('message', 'Not available')}"
            )

        # Print general diagnosis
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

        # Convert boolean into YES or NO
        if resolution["escalation_required"]:
            escalation = "YES"
        else:
            escalation = "NO"

        print(
            f"Escalation Required: "
            f"{escalation}"
        )

    print("\n" + "=" * 60)


# --------------------------------------------------
# Generate summary statistics for the whole test run
# --------------------------------------------------
def generate_summary(results):

    # Total number of endpoint tests
    total = len(results)

    # Counters
    successful = 0
    client_errors = 0
    server_errors = 0
    request_errors = 0
    high_severity = 0

    # Loop through every analysis
    for item in results:

        api_result = item["api_result"]
        diagnosis = item["diagnosis"]

        # --------------------------------------------------
        # HTTP response received
        # --------------------------------------------------
        if api_result["success"]:

            status = api_result["status_code"]

            # Successful HTTP response
            if 200 <= status < 300:
                successful += 1

            # 4xx errors
            elif 400 <= status < 500:
                client_errors += 1

            # 5xx errors
            elif 500 <= status < 600:
                server_errors += 1

        # --------------------------------------------------
        # No usable HTTP response
        # --------------------------------------------------
        else:

            request_errors += 1

        # Count high-severity results
        if diagnosis["severity"] == "High":
            high_severity += 1

    # Return summary as a dictionary
    return {
        "total": total,
        "successful": successful,
        "client_errors": client_errors,
        "server_errors": server_errors,
        "connection_errors": connection_errors,
        "high_severity": high_severity
    }


# --------------------------------------------------
# Count overall endpoint test results
# --------------------------------------------------
def generate_summary(results):

    # Total number of endpoint results
    total = len(results)

    # Create counters
    successful = 0
    client_errors = 0
    server_errors = 0
    connection_errors = 0
    high_severity = 0

    # Check every endpoint result
    for item in results:

        api_result = item["api_result"]
        diagnosis = item["diagnosis"]

        # ------------------------------------------
        # We received an HTTP response
        # ------------------------------------------
        if api_result["success"]:

            status = api_result["status_code"]

            # 2xx
            if 200 <= status < 300:
                successful += 1

            # 4xx
            elif 400 <= status < 500:
                client_errors += 1

            # 5xx
            elif 500 <= status < 600:
                server_errors += 1

        # ------------------------------------------
        # Request failed before usable HTTP response
        # ------------------------------------------
        else:
            connection_errors += 1

        # Count high-severity incidents
        if diagnosis["severity"] == "High":
            high_severity += 1

    # Return all summary information
    return {
        "total": total,
        "successful": successful,
        "client_errors": client_errors,
        "server_errors": server_errors,
        "connection_errors": connection_errors,
        "high_severity": high_severity
    }
# --------------------------------------------------
# Print complete diagnostic and resolution results
# --------------------------------------------------
def print_results(results):

    print("\n" + "=" * 60)
    print("MULTI-ENDPOINT API DIAGNOSTIC RESULTS")
    print("=" * 60)

    for item in results:

        api_result = item["api_result"]
        diagnosis = item["diagnosis"]
        resolution = item["resolution"]

        print("\n" + "-" * 60)

        # ------------------------------------------
        # Basic endpoint information
        # ------------------------------------------
        print(
            f"Service: "
            f"{api_result.get('name', 'Unknown')}"
        )

        print(
            f"Method: "
            f"{api_result.get('method', 'Unknown')}"
        )

        print(
            f"URL: "
            f"{api_result.get('url', 'N/A')}"
        )

        # ------------------------------------------
        # HTTP response
        # ------------------------------------------
        if api_result["success"]:

            print(
                f"HTTP Status Code: "
                f"{api_result['status_code']}"
            )

            print(
                f"Response Time: "
                f"{api_result['response_time']:.2f}s"
            )

        # ------------------------------------------
        # Request/network failure
        # ------------------------------------------
        else:

            print(
                f"Error Code: "
                f"{api_result['error_type']}"
            )

            print(
                f"Error Message: "
                f"{api_result['message']}"
            )

        # ------------------------------------------
        # Diagnosis
        # ------------------------------------------
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

        # ------------------------------------------
        # Likely causes
        # ------------------------------------------
        print("\nLikely Causes:")

        for cause in resolution[
            "likely_causes"
        ]:

            print(
                f"- {cause}"
            )

        # ------------------------------------------
        # Recommended troubleshooting actions
        # ------------------------------------------
        print("\nRecommended Actions:")

        for number, action in enumerate(
            resolution["recommended_actions"],
            start=1
        ):

            print(
                f"{number}. {action}"
            )

        # ------------------------------------------
        # Escalation
        # ------------------------------------------
        if resolution["escalation_required"]:
            escalation = "YES"

        else:
            escalation = "NO"

        print(
            f"\nEscalation Required: "
            f"{escalation}"
        )

        guidance = resolution.get(
            "escalation_guidance",
            resolution.get(
                "escalation_reason",
                "Not provided"
            )
        )

        print(
            f"Escalation Guidance: "
            f"{guidance}"
        )

    print("\n" + "=" * 60)


# --------------------------------------------------
# Print the overall endpoint testing summary
# --------------------------------------------------
def print_summary(summary):

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    print(
        f"Total Endpoints: "
        f"{summary['total']}"
    )

    print(
        f"Successful: "
        f"{summary['successful']}"
    )

    print(
        f"Client Errors: "
        f"{summary['client_errors']}"
    )

    print(
        f"Server Errors: "
        f"{summary['server_errors']}"
    )

    print(
        f"Connection Errors: "
        f"{summary['connection_errors']}"
    )

    print(
        f"High Severity: "
        f"{summary['high_severity']}"
    )

    print("=" * 60)






if __name__ == "__main__":

    results = test_all_endpoints(
        "data/endpoints.csv"
    )

    print_results(results)

    summary = generate_summary(
        results
    )

    print_summary(summary)


