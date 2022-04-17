from urllib import response
from auth import Token, tokens_status
import hashlib
from os import strerror
import random
import re
from flask import Flask, request, abort, jsonify, redirect, url_for
import requests

app = Flask(__name__)

# storage = {}
user_url_storage = {}  # {'user_id': {'short': long}}
newToken = Token()
ROUTE_HOST="http://127.0.0.1:6000/"
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
	status = newToken.verifyToken(token, user_id)['status']
	if status == tokens_status.verified:
		return {'status': 200, 'user_id': user_id}
	elif status == tokens_status.time_expired:
		response = requests.post(ROUTE_HOST+"logout", params=token)
		print(response)
		return {'status': 403, 'user_id': None}
	else:
		return {'status': 403, 'user_id': None}


@app.route("/", methods=['POST'])
def shorten():
	url = request.json['url']

	# get token
	if "Authorization" in request.headers:
		token = request.headers['Authorization']
	else:
		token = None

	# get user from DB based on token
	user_id = get_user_id(token)

	login_status = user_valid(token, user_id)

	if login_status['status'] == 200:
		if url_valid(url):
			# check if url valid

			if user_id not in user_url_storage.keys():
				user_url_storage[user_id] = {}

			hash_url = str(hashlib.shake_256(str(url+request.headers["Authorization"]).encode("UTF-8")).hexdigest(3))
			user_url_storage[user_id][hash_url] = url

			return str(hash_url), 201

		else:
			return "URL Not valid format.", 400

#	elif login_status['status'] == 208:
#		return "Invalid User", login_status['status']
	else:
		return "User not logged in or doesnt exist", login_status['status']


@app.route("/<potato_id>", methods=['GET'])
def potato(potato_id):
	if "Authorization" in request.headers.keys():
		token = request.headers['Authorization']
	else:
		token = None

	# get user from DB based on token
	user_id = get_user_id(token)

	# check if user is valid
	login_status = user_valid(token, user_id)

	if login_status['status'] == 200:
		# check if user is logged in
		if user_id not in user_url_storage.keys():
				user_url_storage[user_id] = {}
		user_storage = user_url_storage[user_id]
		if potato_id in user_storage.keys():
			return redirect(user_storage[potato_id]), 301
		else:
			return "short url not found.", 404

	#elif login_status['status'] == 208:
	#	return "Invalid User", login_status['status']
	else:
		return "User not logged in or doesnt exist", login_status['status']


@app.route("/", methods=["GET"])
def getAllPotatoes():
	if "Authorization" in request.headers.keys():
		token = request.headers['Authorization']
	else:
		token = None

	# get user from DB based on token
	user_id = get_user_id(token)

	login_status = user_valid(token, user_id)

	if login_status['status'] == 200:
		user_storage = user_url_storage[user_id]
		return jsonify({"IDs": list(user_storage.keys())})
	#elif login_status['status'] == 208:
	#	return "Invalid User", login_status['status']
	else:
		return "User not logged in or doesnt exist", login_status['status']


@app.route("/<short_url_id>", methods=['DELETE'])
def potatodelete(short_url_id):
	if "Authorization" in request.headers.keys():
		token = request.headers['Authorization']
	else:
		token = None

	# get user from DB based on token
	user_id = get_user_id(token)

	# user_storage = user_url_storage[user_id]
	login_status = user_valid(token, user_id)

	if login_status['status'] == 200:
		if user_id not in user_url_storage.keys():
			user_url_storage[user_id] = {}

		user_storage = user_url_storage[user_id]
		if short_url_id in user_storage.keys():
			del user_storage[short_url_id]
			return "successfully deleted", 204
		else:
			return "shortened url not found", 404
	else:
		return "forbidden", 403


@app.route("/", methods=['DELETE'])
def potatodontdelete():
	if "Authorization" in request.headers.keys():
		token = request.headers['Authorization']
	else:
		token = None

	# get user from DB based on token
	user_id = get_user_id(token)

	login_status = user_valid(token, user_id)

	if login_status['status'] == 200:
		return "", 404
#	elif login_status['status'] == 208:
#		return "Invalid User", login_status['status']
	else:
		return "User not logged in or doesnt exist", login_status['status']


@app.route("/<shorturl>", methods=["PUT"])
def update(shorturl):
	if "Authorization" in request.headers.keys():
		token = request.headers['Authorization']
	else:
		token = None

	# get user from DB based on token
	user_id = get_user_id(token)

	login_status = user_valid(token, user_id)

	if login_status['status'] == 200:
		# change actual url for a given short url
		# long url is in the request body.

		longurl = request.json['longurl']
		if url_valid(longurl) == False:
			return "URL to be shortened is invalid. ", 400
		# for Sshort, Slong in user_url_storage.items():
		#    if shorturl == Sshort and url_valid(longurl):
		user_storage = user_url_storage[user_id]

		if shorturl in user_storage.keys():
			user_storage[shorturl] = longurl
			return "successful updated.", 200

		return "shortend url not found", 404
	#elif login_status['status'] == 208:
	#	return "Invalid User", login_status['status']
	else:
		return "User not logged in or doesnt exist", login_status['status']


def get_user_id(token):
	return newToken.getUserIdfromToken(token)
