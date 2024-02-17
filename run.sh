#!/bin/bash
source env/bin/activate
cd app
uvicorn main:app --host 0.0.0.0 --port 8899 --reload