#!/bin/bash

# Start the server in the background with a valid config
coverage run --append server.py tests/configs/valid_config.conf &

# Get the PID of the last background command (our server)
SERVER_PID=$!

# Sleep for a bit to ensure server is up
sleep 2

# Send the exit command to shut down the server
ncat localhost 1025 < tests/inputs/valid_startup.in

# Wait for the server to shut down
wait $SERVER_PID

# Compare the output with the expected output
diff <(echo "resolve !EXIT to SHUTDOWN") tests/outputs/valid_startup.out
