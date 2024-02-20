#!/bin/bash

# Test for deleting a domain with an invalid hostname
coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Send invalid !DEL command
echo "!DEL domain..com" | ncat localhost 1025 > tmp.invalid_del.out
echo "INVALID" > expected_invalid_del.out
diff tmp.invalid_del.out expected_invalid_del.out

# Terminate the server with !EXIT
echo "!EXIT" | ncat localhost 1025

wait $SERVER_PID
