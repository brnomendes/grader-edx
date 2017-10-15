#!/bin/bash

gunicorn -c gunicorn_config.py Server:app
