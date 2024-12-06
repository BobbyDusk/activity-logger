#!/bin/bash

DIR=$HOME/activity_logger

# create venv
python3 -m venv $DIR/.venv

# activate venv
source $DIR/.venv/bin/activate

# install requirements
pip install -r requirements.txt

# install ffmpeg
sudo apt install ffmpeg -y

# copy source files
mkdir $DIR/.src -p
cp ./main.py $DIR/.src/main.py
cp ./run.sh $DIR/.src/run.sh
cp ./Arial.ttf $DIR/.src/Arial.ttf

# copy the systemd files
cp ./activity_logger.service $HOME/.config/systemd/user/activity_logger.service
cp ./activity_logger.timer $HOME/.config/systemd/user/activity_logger.timer

# enable and start the service
systemctl --user daemon-reload
systemctl --user enable activity_logger.timer
