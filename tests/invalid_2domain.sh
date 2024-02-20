#!/bin/bash

# Test for invalid domain names with more than 2 parts
coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Query invalid domains from inputs and check against expected outputs
echo -e "-.com.org\ndomain-.com.org\ndomain..com.org" | ncat localhost 1025 > tmp.invalid_domains.out
echo -e "INVALID\nINVALID\nINVALID" > expected_invalid_domains.out
diff tmp.invalid_domains.out expected_invalid_domains.out

# Terminate the server with !EXIT
echo "!EXIT" | ncat localhost 1025

wait $SERVER_PID
