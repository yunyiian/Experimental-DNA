#!/bin/bash

# Test for receiving an incomplete message
coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Send parts of a domain query in separate messages
echo -n "exa" | ncat localhost 1025 > tmp.partial_query1.out
echo "mple.com" | ncat localhost 1025 > tmp.partial_query2.out

# Check against expected output
echo "1026" > expected_complete_query.out
diff tmp.partial_query2.out expected_complete_query.out

# Terminate the server with !EXIT
echo "!EXIT" | ncat localhost 1025

wait $SERVER_PID
