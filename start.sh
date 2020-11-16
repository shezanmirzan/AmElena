#!/bin/bash
# export MPLBACKEND=TkAgg
export FLASK_APP=AmElena/server/control.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=AmElena/server/constants.py
python -m flask run


set FLASK_APP=AmElena\server\control.py
set FLASK_DEBUG=1
set APP_CONFIG_FILE=AmElena\server\constants.py
python -m flask run