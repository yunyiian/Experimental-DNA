#!/bin/bash

coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Send incomplete message and check the response
cat tests/inputs/incomplete_message.in | ncat localhost 1025 > tmp.incomplete_message.out
diff tmp.incomplete_message.out tests/outputs/incomplete_message.out

# Terminate the server with !EXIT
echo "!EXIT" | ncat localhost 1025

wait $SERVER_PID
