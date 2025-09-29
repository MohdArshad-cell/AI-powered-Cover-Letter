import sys
import time

# This message should appear in your Spring Boot console
print("--- Python test_script.py has started ---", file=sys.stderr)

# Simulate some work
time.sleep(2)

# This message should appear in the browser preview panel
print("This is a successful message from the test script.")

# This message should also appear in your Spring Boot console
print("--- Python test_script.py has finished ---", file=sys.stderr)

sys.exit(0)