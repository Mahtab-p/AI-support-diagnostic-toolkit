from config_checker import (
    generate_config_report,
    configuration_ready
)


print("=" * 50)
print("AI SUPPORT DIAGNOSTIC & RESOLUTION TOOLKIT")
print("=" * 50)

generate_config_report()

if configuration_ready():
    print("\nSystem startup: READY")
else:
    print("\nSystem startup: BLOCKED")
    print("Fix configuration issues before continuing.")
