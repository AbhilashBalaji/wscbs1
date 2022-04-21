#!/bin/bash

export FLASK_APP=api_gateway
flask run --port 5000 &

export FLASK_APP=hello
flask run --port 6000 &

export FLASK_APP=behnam
flask run --port 6001 &
