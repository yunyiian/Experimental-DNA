#!/bin/bash

# Missing config
coverage run --append server.py tests/configs/missing.conf 2> tmp.actual.out
diff tmp.actual.out tests/outputs/invalid_configs.out

# Invalid port
coverage run --append server.py tests/configs/invalid_port.conf 2> tmp.actual.out
diff tmp.actual.out tests/outputs/invalid_configs.out

# Invalid domain
coverage run --append server.py tests/configs/invalid_domain.conf 2> tmp.actual.out
diff tmp.actual.out tests/outputs/invalid_configs.out

# Contradicting records
coverage run --append server.py tests/configs/contradicting_records.conf 2> tmp.actual.out
diff tmp.actual.out tests/outputs/invalid_configs.out
