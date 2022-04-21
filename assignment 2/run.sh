#!/bin/bash
# Kinda buggy use at your own risk.
trap ctrl_c INT
function ctrl_c() {
    PORT_NUMBER=6000
    lsof -i tcp:${PORT_NUMBER} | awk 'NR!=1 {print $2}' | xargs kill 
    PORT_NUMBER=6001
    lsof -i tcp:${PORT_NUMBER} | awk 'NR!=1 {print $2}' | xargs kill
    PORT_NUMBER=5000
    lsof -i tcp:${PORT_NUMBER} | awk 'NR!=1 {print $2}' | xargs kill  
}
export FLASK_APP=api_gateway
flask run --port 5000 &

export FLASK_APP=shortner
flask run --port 6000 &

export FLASK_APP=users
flask run --port 6001 &