#!/bin/bash

#export GOOGLE_APPLICATION_CREDENTIALS=''
source ./venv/bin/activate
gunicorn -w $1 -b $2:$3 main:app
