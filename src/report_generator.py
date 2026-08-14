# Import csv so we can create CSV reports
import csv


# --------------------------------------------------
# Save API test results into a CSV file
# --------------------------------------------------
def save_csv_report(results, file_path):

    # These are the columns that will appear
    # in the generated CSV report
    fieldnames = [
        "name",
        "method",
        "url",
        "status_or_error",
        "response_time",
        "category",
        "diagnosis",
        "severity",
        "escalation_required"
    ]

    try:

        # Open the CSV file for writing
        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            # Create a DictWriter using our column names
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            # Write the CSV header row
            writer.writeheader()

            # Loop through all endpoint test results
            for item in results:

                # Extract each part of the analysis
                api_result = item["api_result"]
                diagnosis = item["diagnosis"]
                resolution = item["resolution"]

                # ----------------------------------
                # If an HTTP response was received
                # ----------------------------------
                if api_result["success"]:

                    status_or_error = (
                        api_result["status_code"]
                    )

                    response_time = (
                        f"{api_result['response_time']:.2f}"
                    )

                # ----------------------------------
                # If the request failed before
                # receiving a usable HTTP response
                # ----------------------------------
                else:

                    status_or_error = (
                        api_result["error_type"]
                    )

                    response_time = "N/A"

                # Build one CSV row
                row = {
                    "name": api_result.get(
                        "name",
                        "Unknown"
                    ),

                    "method": api_result.get(
                        "method",
                        "Unknown"
                    ),

                    "url": api_result.get(
                        "url",
                        "N/A"
                    ),

                    "status_or_error": status_or_error,

                    "response_time": response_time,

                    "category": diagnosis[
                        "category"
                    ],

                    "diagnosis": diagnosis[
                        "diagnosis"
                    ],

                    "severity": diagnosis[
                        "severity"
                    ],

                    "escalation_required": resolution[
                        "escalation_required"
                    ]
                }

                # Write this endpoint result
                # into the CSV file
                writer.writerow(row)

        return True

    except OSError as error:

        print(
            f"ERROR: Could not create CSV report: "
            f"{error}"
        )

        return False


# --------------------------------------------------
# Save a human-readable text report
# --------------------------------------------------
def save_text_report(
    results,
    summary,
    file_path
):

    try:

        # Open the text report for writing
        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            # Main report title
            file.write(
                "=" * 60 + "\n"
            )

            file.write(
                "AI SUPPORT DIAGNOSTIC & RESOLUTION REPORT\n"
            )

            file.write(
                "=" * 60 + "\n\n"
            )

            # --------------------------------------
            # Process each endpoint
            # --------------------------------------
            for item in results:

                api_result = item["api_result"]
                diagnosis = item["diagnosis"]
                resolution = item["resolution"]

                # Basic endpoint information
                file.write(
                    f"Service: "
                    f"{api_result.get('name', 'Unknown')}\n"
                )

                file.write(
                    f"Method: "
                    f"{api_result.get('method', 'Unknown')}\n"
                )

                file.write(
                    f"URL: "
                    f"{api_result.get('url', 'N/A')}\n"
                )

                # ----------------------------------
                # HTTP response information
                # ----------------------------------
                if api_result["success"]:

                    file.write(
                        f"HTTP Status: "
                        f"{api_result['status_code']}\n"
                    )

                    file.write(
                        f"Response Time: "
                        f"{api_result['response_time']:.2f}s\n"
                    )

                    file.write(
                        f"Content Type: "
                        f"{api_result.get('content_type', 'Unknown')}\n"
                    )

                    request_id = (
                        api_result.get("request_id")
                        or "Not provided"
                    )

                    file.write(
                        f"Request ID: "
                        f"{request_id}\n"
                    )

                # ----------------------------------
                # Network/request failure
                # ----------------------------------
                else:

                    file.write(
                        f"Error Code: "
                        f"{api_result['error_type']}\n"
                    )

                    file.write(
                        f"Error Message: "
                        f"{api_result['message']}\n"
                    )

                # ----------------------------------
                # Diagnostic information
                # ----------------------------------
                file.write(
                    f"Category: "
                    f"{diagnosis['category']}\n"
                )

                file.write(
                    f"Diagnosis: "
                    f"{diagnosis['diagnosis']}\n"
                )

                file.write(
                    f"Severity: "
                    f"{diagnosis['severity']}\n"
                )

                # ----------------------------------
                # Likely causes
                # ----------------------------------
                file.write(
                    "\nLikely Causes:\n"
                )

                for cause in resolution[
                    "likely_causes"
                ]:

                    file.write(
                        f"- {cause}\n"
                    )

                # ----------------------------------
                # Recommended troubleshooting steps
                # ----------------------------------
                file.write(
                    "\nRecommended Actions:\n"
                )

                for number, action in enumerate(
                    resolution[
                        "recommended_actions"
                    ],
                    start=1
                ):

                    file.write(
                        f"{number}. {action}\n"
                    )

                # ----------------------------------
                # Escalation decision
                # ----------------------------------
                if resolution[
                    "escalation_required"
                ]:

                    escalation = "YES"

                else:
                    escalation = "NO"

                file.write(
                    f"\nEscalation Required: "
                    f"{escalation}\n"
                )

                # Support both versions of the
                # escalation field used in our project
                guidance = resolution.get(
                    "escalation_guidance",
                    resolution.get(
                        "escalation_reason",
                        "Not provided"
                    )
                )

                file.write(
                    f"Escalation Guidance: "
                    f"{guidance}\n"
                )

                # Separator between endpoints
                file.write(
                    "\n" + "-" * 60 + "\n\n"
                )

            # --------------------------------------
            # Overall summary
            # --------------------------------------
            file.write(
                "=" * 60 + "\n"
            )

            file.write(
                "SUMMARY\n"
            )

            file.write(
                "=" * 60 + "\n"
            )

            file.write(
                f"Total Endpoints: "
                f"{summary['total']}\n"
            )

            file.write(
                f"Successful: "
                f"{summary['successful']}\n"
            )

            file.write(
                f"Client Errors: "
                f"{summary['client_errors']}\n"
            )

            file.write(
                f"Server Errors: "
                f"{summary['server_errors']}\n"
            )

            file.write(
                f"Connection Errors: "
                f"{summary['connection_errors']}\n"
            )

            file.write(
                f"High Severity: "
                f"{summary['high_severity']}\n"
            )

        return True

    except OSError as error:

        print(
            f"ERROR: Could not create text report: "
            f"{error}"
        )

        return False


# --------------------------------------------------
# Generate both CSV and TXT reports
# --------------------------------------------------
def generate_reports(
    results,
    summary
):

    # Generate CSV report
    csv_created = save_csv_report(
        results,
        "reports/api_report.csv"
    )

    # Generate human-readable text report
    text_created = save_text_report(
        results,
        summary,
        "reports/api_report.txt"
    )

    # Check whether both files were created
    if csv_created and text_created:

        print(
            "\nReports generated successfully."
        )

        print(
            "CSV Report: reports/api_report.csv"
        )

        print(
            "Text Report: reports/api_report.txt"
        )

        return True

    print(
        "\nOne or more reports "
        "could not be generated."
    )

    return False


# --------------------------------------------------
# Test this module when report_generator.py
# is executed directly
# --------------------------------------------------
if __name__ == "__main__":

    # Import functions from Stage 6
    from endpoint_tester import (
        test_all_endpoints,
        generate_summary
    )

    # Test all endpoints from the CSV file
    results = test_all_endpoints(
        "data/endpoints.csv"
    )

    # Generate summary statistics
    summary = generate_summary(
        results
    )

    # Generate CSV and text reports
    generate_reports(
        results,
        summary
    )
