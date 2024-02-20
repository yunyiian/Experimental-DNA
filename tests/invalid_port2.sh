#!/bin/bash

# Test for an invalid port in the configuration
coverage run --append server.py tests/configs/invalid_port_config.conf

if [ $? -ne 0 ]; then
    echo "Error: Expected INVALID CONFIGURATION"
    exit 1
fi