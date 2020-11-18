#!/bin/bash
# export MPLBACKEND=TkAgg
export FLASK_APP=src/server/requesthandler.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=src/server/constants.py
python -m flask run


# set FLASK_APP=src\server\requesthandler.py
# set FLASK_DEBUG=1
# set APP_CONFIG_FILE=src\server\constants.py
# python -m flask run
