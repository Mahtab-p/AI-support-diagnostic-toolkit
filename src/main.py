# Import configuration checks
from config_checker import (
    generate_config_report,
    configuration_ready
)

# Import endpoint testing
from endpoint_tester import (
    test_all_endpoints,
    print_results,
    generate_summary,
    print_summary
)

# Import report generation
from report_generator import generate_reports

# Import logging
from logger import write_log


# --------------------------------------------------
# Main application workflow
# --------------------------------------------------
def main():

    print("=" * 60)
    print("AI SUPPORT DIAGNOSTIC & RESOLUTION TOOLKIT")
    print("=" * 60)

    # Log application startup
    write_log(
        "INFO",
        "Diagnostic toolkit started."
    )

    # ----------------------------------------------
    # Step 1: Check configuration
    # ----------------------------------------------
    generate_config_report()

    if not configuration_ready():

        print(
            "\nSystem startup: BLOCKED"
        )

        print(
            "Fix configuration issues before continuing."
        )

        write_log(
            "ERROR",
            "Application blocked due to invalid configuration."
        )

        return

    print(
        "\nSystem startup: READY"
    )

    # ----------------------------------------------
    # Step 2: Test all endpoints
    # ----------------------------------------------
    results = test_all_endpoints(
        "data/endpoints.csv"
    )

    # ----------------------------------------------
    # Step 3: Print endpoint results
    # ----------------------------------------------
    print_results(
        results
    )

    # ----------------------------------------------
    # Step 4: Generate summary
    # ----------------------------------------------
    summary = generate_summary(
        results
    )

    print_summary(
        summary
    )

    # ----------------------------------------------
    # Step 5: Generate CSV and text reports
    # ----------------------------------------------
    reports_created = generate_reports(
        results,
        summary
    )

    if reports_created:

        write_log(
            "INFO",
            "Diagnostic reports generated successfully."
        )

    else:

        write_log(
            "ERROR",
            "One or more diagnostic reports failed."
        )

    # ----------------------------------------------
    # Step 6: Log overall run results
    # ----------------------------------------------
    write_log(
        "INFO",
        (
            f"Run completed. "
            f"Total={summary['total']}, "
            f"Successful={summary['successful']}, "
            f"ClientErrors={summary['client_errors']}, "
            f"ServerErrors={summary['server_errors']}, "
            f"ConnectionErrors={summary['connection_errors']}"
        )
    )

    print(
        "\nDiagnostic run completed."
    )


# --------------------------------------------------
# Start the application
# --------------------------------------------------
if __name__ == "__main__":
    main()
