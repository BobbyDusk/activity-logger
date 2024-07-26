#!/bin/bash

# create venv
python3 -m venv $HOME/activity_logger/venv

# activate venv
source $HOME/activity_logger/venv/bin/activate

# install requirements
pip install -r requirements.txt

# run the app
python main.py