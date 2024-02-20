#!/bin/bash

# Test for adding a domain with an invalid hostname and port
coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Send invalid !ADD command
echo "!ADD domain..com 66000" | ncat localhost 1025 > tmp.invalid_add.out
echo "INVALID" > expected_invalid_add.out
diff tmp.invalid_add.out expected_invalid_add.out

# Terminate the server with !EXIT
echo "!EXIT" | ncat localhost 1025

wait $SERVER_PID
