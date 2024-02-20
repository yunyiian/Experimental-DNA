#!/bin/bash

coverage run --append server.py tests/configs/valid_config.conf &

SERVER_PID=$!
sleep 2

# Query invalid multi-part hostnames
echo "-example.com" | ncat localhost 1025 > tmp.invalid_multi_hostname.out
echo "example-.com" | ncat localhost 1025 >> tmp.invalid_multi_hostname.out
echo "example.-com" | ncat localhost 1025 >> tmp.invalid_multi_hostname.out
echo "example.com." | ncat localhost 1025 >> tmp.invalid_multi_hostname.out

diff tmp.invalid_multi_hostname.out tests/outputs/invalid_multi_hostname.out

# Terminate the server
echo "!EXIT" | ncat localhost 1025

wait $SERVER_PID
