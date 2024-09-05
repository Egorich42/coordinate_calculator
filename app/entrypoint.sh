#!/bin/bash

python init_db.py

exec gunicorn -w 4 -b 0.0.0.0:8080 main:app
