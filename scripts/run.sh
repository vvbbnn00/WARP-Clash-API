#!/bin/bash

cd /app || exit 1

python3 app.py background&
python3 app.py web