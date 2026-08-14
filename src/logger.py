# Import datetime so every log entry has a timestamp
from datetime import datetime


# --------------------------------------------------
# Write one event into the support log
# --------------------------------------------------
def write_log(
    level,
    message,
    file_path="logs/support.log"
):

    # Get the current date and time
    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Build one log line
    log_entry = (
        f"{timestamp} | "
        f"{level.upper()} | "
        f"{message}"
    )

    try:

        # "a" means append.
        # We add new logs instead of deleting old ones.
        with open(
            file_path,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                log_entry + "\n"
            )

        return True

    except OSError as error:

        print(
            f"Logging Error: {error}"
        )

        return False


# --------------------------------------------------
# Test logger.py directly
# --------------------------------------------------
if __name__ == "__main__":

    write_log(
        "INFO",
        "AI Support Diagnostic Toolkit started."
    )

    write_log(
        "ERROR",
        "Test API connection failure."
    )

    print("Test logs created.")


#temp Test

write_log(
    "WARNING",
    "API response time is slower than expected."
)

write_log(
    "CRITICAL",
    "Multiple API services are unavailable."
)
