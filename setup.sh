#!/bin/bash

DIR=$HOME/activity_logger

# install uv (if it isn't installed already)
hash uv 2>/dev/null || {
	echo "Installing uv"
	curl -LsSf https://astral.sh/uv/install.sh | sh
}

# install ffmpeg
hash ffmpeg 2>/dev/null || {
	echo "Installing ffmpeg"
	sudo apt install ffmpeg -y
}

# copy source files
echo "Copying source files"
mkdir $DIR/.src -p
cp ./main.py $DIR/.src/main.py
cp ./run.sh $DIR/.src/run.sh
cp ./Arial.ttf $DIR/.src/Arial.ttf
cp ./pyproject.toml $DIR/.src/pyproject.toml
cp ./uv.lock $DIR/.src/uv.lock

# copy the systemd files
echo "Copying systemd files"
mkdir $HOME/.config/systemd/user -p
cp ./activity_logger.service $HOME/.config/systemd/user/activity_logger.service
cp ./activity_logger.timer $HOME/.config/systemd/user/activity_logger.timer

# install dependencies
echo "Installing dependencies"
cd $DIR/.src
uv sync

# enable and start the service
echo "Enabling and starting the service"
systemctl --user daemon-reload
systemctl --user enable activity_logger.timer
systemctl --user start activity_logger.timer
