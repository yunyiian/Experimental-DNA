#!/bin/bash

coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Query invalid single-part hostnames
echo "-example" | ncat localhost 1025 > tmp.invalid_single_hostname.out
echo "example-" | ncat localhost 1025 >> tmp.invalid_single_hostname.out

diff tmp.invalid_single_hostname.out tests/outputs/invalid_single_hostname.out

# Terminate the server
echo "!EXIT" | ncat localhost 1025

wait $SERVER_PID
