#!/bin/bash
# export MPLBACKEND=TkAgg
export FLASK_APP=src/server/control.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=src/server/constants.py
python -m flask run


# set FLASK_APP=src\server\control.py
# set FLASK_DEBUG=1
# set APP_CONFIG_FILE=src\server\constants.py
# python -m flask run
