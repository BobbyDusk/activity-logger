#!/bin/bash

# check if in graphical environment
if [ "$DISPLAY" ] || [ "$WAYLAND_DISPLAY" ] || [ "$MIR_SOCKET" ]; then

    DIR=$HOME/activity_logger

    # activate venv
    source $DIR/.venv/bin/activate

    # run the app
    python3 $DIR/.src/main.py
fi

