#!/bin/bash

coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Send incomplete messages and then complete them
(echo -n "exa"; sleep 1; echo "mple.com") | ncat localhost 1025 > tmp.incomplete_messages.out

diff tmp.incomplete_messages.out tests/outputs/incomplete_messages.out

# Terminate the server
echo "!EXIT" | ncat localhost 1025

wait $SERVER_PID
