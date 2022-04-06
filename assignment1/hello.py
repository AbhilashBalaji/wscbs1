from crypt import methods
import hashlib
import random
import re
from flask import Flask, request, abort, jsonify, redirect , url_for


app = Flask(__name__)
storage = {"1":"2"}
regex = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def url_valid(url):
	return re.match(regex,url) is not None



@app.route("/", methods=['POST'])
def shorten():
#  create KV pair 
	url = request.json['url']
	if url_valid(url):
		hash_url  = str(hashlib.shake_256(url.encode("UTF-8")).hexdigest(length=3))
		storage[hash_url] = url
		return str(hash_url), 201
	else:
		# url entered is not valid. TEST
		return "URL Not valid format.", 400

@app.route("/<int:potato_id>", methods=['GET'])
def potato(potato_id):

	'''
	id handling.
	'''
	# return 'potato there'
	return jsonify({"POTATO ID":potato_id})


@app.route("/",methods=["GET"])
def getAllPotatoes():
	return jsonify({"IDs":list(storage.keys())})

@app.route("/<int:delete_potato>", methods=['DELETE'])
def potatodelete(delete_potato):
	if delete_potato is None:
		'''
		/ endpoint.
		'''
	else:
		'''
		id handling.
		'''







def bad_request(message):

	response = jsonify({'message': message})
	response.status_code = 400
	return response


