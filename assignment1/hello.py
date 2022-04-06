from crypt import methods
import hashlib
from os import strerror
import random
import re
from flask import Flask, request, abort, jsonify, redirect , url_for
import time

app = Flask(__name__)
# storage 1: {guid:url} -> POST {1:google.com} -> PUT {1:google.com}

storage = {"1":"google"} #id&url

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
		hash_url  = str(hashlib.shake_256(str(url + str(time.time())).encode("UTF-8")).hexdigest(length=3))
		#hash_url = hashlib.shake_256(url.encode()).hexdigest() #add size of hash 
		storage[hash_url] = url
		return str(hash_url), 201
	else:
		# url entered is not valid. TEST
		return "URL Not valid format.", 400

@app.route("/<potato_id>", methods=['GET'])
def potato(potato_id):
	if potato_id in storage.keys():
		return redirect(storage[potato_id]) , 301
	else:
		return "",404

@app.route("/",methods=["GET"])
def getAllPotatoes():
	return jsonify({"IDs":list(storage.keys())})

@app.route("/<id>", methods=['DELETE'])
def potatodelete(id):
	if id in storage.keys():
		del storage[id]
		return "",204
	else:
		return "Shortened URL not found",404

@app.route("/",methods=['DELETE'])
def potatodontdelete():
	return "",404


def bad_request(message):

	response = jsonify({'message': message})
	response.status_code = 400
	return response


