# Import requests so we can send HTTP requests
import requests


# --------------------------------------------------
# Send a GET request
# --------------------------------------------------
def send_get_request(url, timeout=5):

    try:
        response = requests.get(
            url,
            timeout=timeout
        )

        # Try to convert the response to JSON
        try:
            response_data = response.json()

        except ValueError:
            response_data = None

        return {
            "success": True,
            "method": "GET",
            "url": response.url,
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "content_type": response.headers.get(
                "Content-Type",
                "Unknown"
            ),
            "request_id": response.headers.get(
                "X-Request-ID"
            ),
            "json": response_data,
            "text": response.text
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "method": "GET",
            "error_type": "Timeout",
            "message": "The API request timed out."
        }

    except requests.exceptions.ConnectionError:

        return {
            "success": False,
            "method": "GET",
            "error_type": "ConnectionError",
            "message": "Unable to connect to the API."
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "method": "GET",
            "error_type": "RequestException",
            "message": str(error)
        }


# --------------------------------------------------
# Send a POST request
# --------------------------------------------------
def send_post_request(url, payload, timeout=5):

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=timeout
        )

        # Try to convert the response to JSON
        try:
            response_data = response.json()

        except ValueError:
            response_data = None

        return {
            "success": True,
            "method": "POST",
            "url": response.url,
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "content_type": response.headers.get(
                "Content-Type",
                "Unknown"
            ),
            "request_id": response.headers.get(
                "X-Request-ID"
            ),
            "json": response_data,
            "text": response.text
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "method": "POST",
            "error_type": "Timeout",
            "message": "The API request timed out."
        }

    except requests.exceptions.ConnectionError:

        return {
            "success": False,
            "method": "POST",
            "error_type": "ConnectionError",
            "message": "Unable to connect to the API."
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "method": "POST",
            "error_type": "RequestException",
            "message": str(error)
        }


# --------------------------------------------------
# Test the API client
# This section only runs when we execute:
# python src/api_client.py
# --------------------------------------------------
if __name__ == "__main__":

    print("=== GET TEST ===")

    get_result = send_get_request(
        "https://dummyjson.com/products/1"
    )

    if get_result["success"]:
        print(f"Method: {get_result['method']}")
        print(f"Status: {get_result['status_code']}")
        print(f"URL: {get_result['url']}")
        print(
            f"Response Time: "
            f"{get_result['response_time']:.2f}s"
        )
    else:
        print(f"Error: {get_result['message']}")


    print("\n=== POST TEST ===")

    payload = {
        "title": "AI Support Diagnostic Test"
    }

    post_result = send_post_request(
        "https://dummyjson.com/products/add",
        payload
    )

    if post_result["success"]:
        print(f"Method: {post_result['method']}")
        print(f"Status: {post_result['status_code']}")
        print(f"URL: {post_result['url']}")
        print(
            f"Response Time: "
            f"{post_result['response_time']:.2f}s"
        )
        print(f"Response JSON: {post_result['json']}")
    else:
        print(f"Error: {post_result['message']}")
