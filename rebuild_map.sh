#!/bin/bash

set -e

cd ./src/utils

python run_analytics.py
python build_map.py