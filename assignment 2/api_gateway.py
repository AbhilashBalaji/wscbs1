import json

import requests
from flask import Flask, request, abort, jsonify, redirect, url_for
import config

api_gateway_app = Flask(__name__)


@api_gateway_app.route('/users', methods=['POST'])
def redirect_to_users():
    print(config.users_app_ip + 'users')
    data = request.json
    dictionary = json.loads(data)
    return requests.post(url=config.users_app_ip + 'users', data=dictionary)


@api_gateway_app.route('/users/login', methods=['POST'])
def redirect_to_login():
    return "redirect to login"


@api_gateway_app.route('/users/logout', methods=['POST'])
def redirect_to_logout():
    return "redirect to logout"


#####################################################

@api_gateway_app.route("/", methods=['POST'])
def redirect_to_shorten():
    return "redirect to shorten"


@api_gateway_app.route("/<potato_id>", methods=['GET'])
def potato(potato_id):
    return "redirect to GET shorten: " + str(potato_id)


@api_gateway_app.route("/", methods=["GET"])
def getAllPotatoes():
    return "redirect to GET all shorten"


@api_gateway_app.route("/<short_url_id>", methods=['DELETE'])
def potatodelete(short_url_id):
    return "redirect to DELETE all shorten: " + str(short_url_id)


@api_gateway_app.route("/", methods=['DELETE'])
def potatodontdelete():
    return "redirect to DELETE"


@api_gateway_app.route("/<shorturl>", methods=["PUT"])
def update(shorturl):
    return "redirect to PUT all shorten: " + str(shorturl)
