#!/bin/bash

# create venv
python3 -m venv venv

# activate venv
source venv/bin/activate

# install requirements
pip install -r requirements.txt