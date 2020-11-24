#!/bin/bash
# export MPLBACKEND=TkAgg
export FLASK_APP=src/server/requesthandler.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=src/server/constants.py
python -m flask run

