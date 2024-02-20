#!/bin/bash

coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Send a valid !ADD command and check the response.
cat tests/inputs/add_command.in | ncat localhost 1025 > tmp.add_command.out
diff tmp.add_command.out tests/outputs/add_command.out

# Send a valid !DEL command and check the response.
cat tests/inputs/del_command.in | ncat localhost 1025 > tmp.del_command.out
diff tmp.del_command.out tests/outputs/del_command.out

# Terminate the server with !EXIT
echo "!EXIT" | ncat localhost 1025 > tmp.exit_command.out
diff tmp.exit_command.out tests/outputs/exit_command.out

wait $SERVER_PID
