# Import os so Python can read environment variables
import os

# Import load_dotenv so Python can load variables from the .env file
from dotenv import load_dotenv


# Load variables from the .env file into the program
load_dotenv()


# --------------------------------------------------
# Check whether an environment variable exists
# --------------------------------------------------
def check_env(var_name):
    value = os.getenv(var_name)

    if value:
        return {
            "name": var_name,
            "configured": True,
            "value": value
        }

    return {
        "name": var_name,
        "configured": False,
        "value": None
    }


# --------------------------------------------------
# Hide most of a secret before displaying it
# Example: test-token -> test****
# --------------------------------------------------
def mask_secret(value):

    # If the value doesn't exist
    if not value:
        return "Not Configured"

    # If the secret is very short, hide all of it
    if len(value) <= 4:
        return "****"

    # Show only the first 4 characters
    return value[:4] + "****"


# --------------------------------------------------
# Read and validate REQUEST_TIMEOUT
# Environment variables are strings, so we convert
# the timeout into an integer.
# --------------------------------------------------
def get_timeout():

    # Use 5 if REQUEST_TIMEOUT doesn't exist
    timeout_value = os.getenv(
        "REQUEST_TIMEOUT",
        "5"
    )

    try:
        timeout = int(timeout_value)

        # Timeout must be greater than zero
        if timeout <= 0:
            raise ValueError

        return timeout

    except ValueError:
        return None


# --------------------------------------------------
# Decide whether all required configuration exists
# --------------------------------------------------
def configuration_ready():

    base_url = os.getenv("API_BASE_URL")
    api_token = os.getenv("API_TOKEN")
    environment = os.getenv("ENVIRONMENT")
    timeout = get_timeout()

    # all() returns True only if every value is valid
    return all([
        base_url,
        api_token,
        environment,
        timeout
    ])


# --------------------------------------------------
# Create troubleshooting recommendations
# for missing or invalid configuration
# --------------------------------------------------
def get_config_recommendations():

    recommendations = []

    if not os.getenv("API_BASE_URL"):
        recommendations.append(
            "Configure API_BASE_URL in the .env file."
        )

    if not os.getenv("API_TOKEN"):
        recommendations.append(
            "Configure API_TOKEN before sending authenticated requests."
        )

    if not os.getenv("ENVIRONMENT"):
        recommendations.append(
            "Set ENVIRONMENT to development, staging, or production."
        )

    if get_timeout() is None:
        recommendations.append(
            "Set REQUEST_TIMEOUT to a positive whole number."
        )

    return recommendations


# --------------------------------------------------
# Display the complete configuration report
# --------------------------------------------------
def generate_config_report():

    # Read configuration values
    base_url = os.getenv("API_BASE_URL")
    api_token = os.getenv("API_TOKEN")
    environment = os.getenv("ENVIRONMENT")
    timeout = get_timeout()

    print("=" * 50)
    print("CONFIGURATION CHECK")
    print("=" * 50)

    # Show the API URL
    print(
        f"API Base URL: "
        f"{base_url if base_url else 'Missing'}"
    )

    # Never print the complete token
    print(
        f"API Token: {mask_secret(api_token)}"
    )

    # Show current environment
    print(
        f"Environment: "
        f"{environment if environment else 'Missing'}"
    )

    # Validate timeout
    if timeout:
        print(f"Request Timeout: {timeout} seconds")
    else:
        print("Request Timeout: Invalid")

    print("=" * 50)

    # Check overall configuration status
    if configuration_ready():
        print("Configuration Status: READY")

    else:
        print("Configuration Status: INCOMPLETE")

        # Get troubleshooting recommendations
        recommendations = get_config_recommendations()

        if recommendations:
            print("\nRecommended Actions:")

            # Print numbered recommendations
            for number, recommendation in enumerate(
                recommendations,
                start=1
            ):
                print(f"{number}. {recommendation}")


# --------------------------------------------------
# Run the report only when this file is executed
# directly.
#
# python src/config_checker.py
#
# Later, main.py can import these functions without
# automatically running the report.
# --------------------------------------------------
if __name__ == "__main__":
    generate_config_report()
