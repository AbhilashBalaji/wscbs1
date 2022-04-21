#!/bin/bash

export FLASK_APP=api_gateway
flask run --port 5000 &

export FLASK_APP=shortner
flask run --port 6000 &

export FLASK_APP=users
flask run --port 6001 &
