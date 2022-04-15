from crypt import methods
from auth import Token
import hashlib
from os import strerror
import random
import re
from flask import Flask, request, abort, jsonify, redirect, url_for
import time
from behnam import User

app = Flask(__name__)
# storage = {}
user_url_storage = {}  # {'user_id': {'short': long}}
newToken = Token()

regex = re.compile(
    r'^(?:http)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def url_valid(url):
    return re.match(regex, url) is not None


def user_valid(token, user_id):
    return newToken.verifyToken(token, user_id)


def check_login(token, user_id):
    if newToken.verifyToken(token, user_id):
        return User.filter_by(token=token).first() is not None
    else:
        return False


@app.route("/", methods=['POST'])
def shorten():
    url = request.json['url']

    # get token
    token = request.headers['Authorization']

    # get user from DB based on token
    user_record = User.filter_by(token=token).first()
    user_id = user_record.user_id

    # check if url valid
    if (user_valid(token, user_id)):
        if url_valid(url):

            # check if user logged in
            if check_login(token, user_id):
                hash_url = str(hashlib.shake_256(url.encode("UTF-8")).hexdigest(3))
                user_url_storage[user_id] = {hash_url: url}

                return str(hash_url), 201

            else:
                return "unauthorized short url creation", 403

        else:
            return "URL Not valid format.", 400

    else:
        return "forbidden", 403


@app.route("/<potato_id>", methods=['GET'])
def potato(potato_id):
    token = request.headers['Authorization']
    user_record = User.filter_by(token=token).first()
    user_id = user_record.user_id

    # check if user is valid
    if (user_valid(token, user_record.user_id)):

        # check if user is logged in
        if check_login(token, user_id):
            if potato_id in user_url_storage.keys():
                return redirect(user_url_storage[potato_id]), 301
            else:
                return "short url not found.", 404
        else:
            return "unauthorized, user not logged in", 403

    else:
        return "forbidden", 403


@app.route("/", methods=["GET"])
def getAllPotatoes():
    return jsonify({"IDs": list(user_url_storage.keys())})


@app.route("/<id>", methods=['DELETE'])
def potatodelete(id):
    if 'alg' in request.headers:
        token = request.headers.get('alg')

    if (user_valid(token)):
        if id in user_url_storage.keys():
            del user_url_storage[id]
            return "successfully deleted", 204
        else:
            return "Shortened URL not found", 404
    else:
        return "forbidden", 403


@app.route("/", methods=['DELETE'])
def potatodontdelete():
    if 'alg' in request.headers:
        token = request.headers.get('alg')

    if (user_valid(token)):
        return "", 404
    else:
        return "forbidden", 403


@app.route("/<shorturl>", methods=["PUT"])
def update(shorturl):
    if 'alg' in request.headers:
        token = request.headers.get('alg')

    if (user_valid(token)):
        # change actual url for a given short url
        # long url is in the request body.

        longurl = request.json['longurl']
        if url_valid(longurl) == False:
            return "URL to be shortened is invalid. ", 400
        for Sshort, Slong in user_url_storage.items():
            if shorturl == Sshort and url_valid(longurl):
                user_url_storage[Sshort] = longurl
                return "successful updation.", 200
        return "shortend url not found", 404
    else:
        return "forbidden", 403
