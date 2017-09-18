#!/bin/bash
SERVER=127.0.0.1
PORT=1710
THREADS=2

gunicorn Server:app --threads $THREADS -b $SERVER:$PORT
