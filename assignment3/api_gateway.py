from flask import Flask, redirect
from assignment3.users import config

api_gateway_app = Flask(__name__)


@api_gateway_app.route('/users', methods=['POST'])
def redirect_to_users():
    return redirect(config.users_app_ip + 'users', code=307)


@api_gateway_app.route('/users/login', methods=['POST'])
def redirect_to_login():
    return redirect(config.users_app_ip + 'users/login', code=307)


@api_gateway_app.route('/users/logout', methods=['POST'])
def redirect_to_logout():
    return redirect(config.users_app_ip + 'users/logout', code=307)


#####################################################

@api_gateway_app.route("/", methods=['POST'])
def redirect_to_shorten():
    return redirect(config.shorten_app_ip, code=307)


@api_gateway_app.route("/<potato_id>", methods=['GET'])
def potato(potato_id):
    return redirect(config.shorten_app_ip + potato_id, code=307)


@api_gateway_app.route("/", methods=["GET"])
def getAllPotatoes():
    return redirect(config.shorten_app_ip, code=307)


@api_gateway_app.route("/<short_url_id>", methods=['DELETE'])
def potatodelete(short_url_id):
    return redirect(config.shorten_app_ip + short_url_id, code=307)


@api_gateway_app.route("/", methods=['DELETE'])
def potatodontdelete():
    return redirect(config.shorten_app_ip, code=307)


@api_gateway_app.route("/<shorturl>", methods=["PUT"])
def update(shorturl):
    return "redirect to PUT all shorten: " + str(shorturl)
