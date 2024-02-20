#!/bin/bash

coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Query invalid domains from inputs and check against outputs
cat tests/inputs/invalid_domain_query.in | ncat localhost 1025 > tmp.invalid_domain_query.out
diff tmp.invalid_domain_query.out tests/outputs/invalid_domain_query.out

# Terminate the server with !EXIT
echo "!EXIT" | ncat localhost 1025

wait $SERVER_PID
