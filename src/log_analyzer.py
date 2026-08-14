# --------------------------------------------------
# Read all log entries from a log file
# --------------------------------------------------
def read_logs(
    file_path="logs/support.log"
):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.readlines()

    except FileNotFoundError:

        print(
            f"Log file not found: {file_path}"
        )

        return []

    except OSError as error:

        print(
            f"Could not read log file: {error}"
        )

        return []


# --------------------------------------------------
# Count different log levels
# --------------------------------------------------
def count_log_levels(logs):

    counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0
    }

    for line in logs:

        if "| INFO |" in line:
            counts["INFO"] += 1

        elif "| WARNING |" in line:
            counts["WARNING"] += 1

        elif "| ERROR |" in line:
            counts["ERROR"] += 1

        elif "| CRITICAL |" in line:
            counts["CRITICAL"] += 1

    return counts


# --------------------------------------------------
# Find only error and critical log entries
# --------------------------------------------------
def find_errors(logs):

    errors = []

    for line in logs:

        if (
            "| ERROR |" in line
            or "| CRITICAL |" in line
        ):
            errors.append(
                line.strip()
            )

    return errors


# --------------------------------------------------
# Print a readable log analysis report
# --------------------------------------------------
def print_log_analysis(
    logs,
    counts,
    errors
):

    print("=" * 60)
    print("SUPPORT LOG ANALYSIS")
    print("=" * 60)

    print(
        f"Total Log Entries: "
        f"{len(logs)}"
    )

    print(
        f"INFO: "
        f"{counts['INFO']}"
    )

    print(
        f"WARNING: "
        f"{counts['WARNING']}"
    )

    print(
        f"ERROR: "
        f"{counts['ERROR']}"
    )

    print(
        f"CRITICAL: "
        f"{counts['CRITICAL']}"
    )

    print("\nERROR EVENTS")
    print("-" * 60)

    if errors:

        for error in errors:
            print(error)

    else:
        print("No error events found.")

    print("=" * 60)


# --------------------------------------------------
# Test log analyzer directly
# --------------------------------------------------
if __name__ == "__main__":

    logs = read_logs()

    counts = count_log_levels(
        logs
    )

    errors = find_errors(
        logs
    )

    print_log_analysis(
        logs,
        counts,
        errors
    )


# --------------------------------------------------
# Search logs for a keyword
# --------------------------------------------------
def search_logs(
    logs,
    keyword
):

    matches = []

    for line in logs:

        if keyword.lower() in line.lower():

            matches.append(
                line.strip()
            )

    return matches




#temp test

#print("\nSEARCH RESULTS")
#print("-" * 60)

#matches = search_logs(
 #   logs,
  #  "connection"
#)

#for match in matches:
 #   print(match)


