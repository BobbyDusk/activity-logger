#!/bin/bash

# check if in graphical environment
if [ "$DISPLAY" ] || [ "$WAYLAND_DISPLAY" ] || [ "$MIR_SOCKET" ]; then

    DIR=$HOME/activity_logger

    # run the app
    cd $DIR/.src
    uv run main.py
fi

