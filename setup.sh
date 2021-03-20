#! /bin/bash
if [ -d ./venv ]; then
  rm -rf ./venv/.*
  rm -rf ./venv/*
  rmdir ./venv
fi
mkdir venv
python3 -m venv venv
source ./venv/bin/activate
pip install -U pip
pip install -r requirements.txt
deactivate
