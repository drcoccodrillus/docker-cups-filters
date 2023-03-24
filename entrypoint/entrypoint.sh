#!/bin/bash

cd /app
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

flask run --no-reload --host 0.0.0.0 --port 5000