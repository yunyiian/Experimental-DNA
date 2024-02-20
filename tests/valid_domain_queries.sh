#!/bin/bash

coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Query valid domains from inputs and check against outputs
cat tests/inputs/valid_domain_query.in | ncat localhost 1025 > tmp.valid_domain_query.out
diff tmp.valid_domain_query.out tests/outputs/valid_domain_query.out

# Terminate the server with !EXIT
echo "!EXIT" | ncat localhost 1025

wait $SERVER_PID
