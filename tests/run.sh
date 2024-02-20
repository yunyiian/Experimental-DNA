#!/bin/bash

# Self-testing script for server.py

# Clear previous coverage data
echo "Erasing previous coverage data..."
coverage erase

# Array of all test scripts
TESTS=(
  "./tests/valid_startup.sh"
  "./tests/invalid_configs.sh"
  "./tests/valid_commands.sh"
  "./tests/invalid_commands.sh"
  "./tests/incomplete_messages.sh"
  "./tests/test_invalid_single_part_hostname.sh"
  "./tests/test_invalid_multi_part_hostname.sh"
  "./tests/test_invalid_args.sh"
  "./tests/invalid_2domain.sh"
  "./tests/invalid_port2.sh"
  "./tests/add_invalidhost.sh"
  "./tests/deletehost.sh"
  "./tests/messageincomplete2.sh"
)

# Execute each test script
for test in "${TESTS[@]}"; do
    echo "Running $test..."
    $test
    # Check the exit code of the test. If it's non-zero, the test failed.
    if [[ $? -ne 0 ]]; then
        echo "Error during test: $test"
        exit 1
    fi
done

# Generate the coverage report
echo "Generating coverage report..."
coverage report -m

echo "All tests completed successfully!"

lsof -i :1025 | awk 'NR!=1 {print $2}' | xargs kill


