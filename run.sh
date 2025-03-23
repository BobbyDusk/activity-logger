#!/bin/bash

# Copyright (c) 2025, Edge of Dusk
# This project is licensed under the MIT License - see the LICENSE file for details

# check if in graphical environment
if [ "$DISPLAY" ] || [ "$WAYLAND_DISPLAY" ] || [ "$MIR_SOCKET" ]; then

    DIR=$HOME/activity_logger

    # run the app
    cd $DIR/.src
    uv run main.py
fi

