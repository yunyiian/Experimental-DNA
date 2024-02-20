#!/bin/bash

# Start server with no arguments
coverage run --append server.py > tmp.invalid_args.out
coverage run --append server.py arg1 arg2 >> tmp.invalid_args.out

diff tmp.invalid_args.out tests/outputs/invalid_args.out
