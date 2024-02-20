#!/bin/bash

coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Send invalid commands from the inputs directory and check against the corresponding outputs.
cat tests/inputs/invalid_command_structure.in | ncat localhost 1025 > tmp.invalid_command_structure.out
diff tmp.invalid_command_structure.out tests/outputs/invalid_command_structure.out

# Terminate the server with !EXIT
echo "!EXIT" | ncat localhost 1025

wait $SERVER_PID
