from crypt import methods
import os
import uuid
from flask_sqlalchemy import SQLAlchemy
import hashlib
from os import strerror
import random
import re
from flask import Flask, request, abort, jsonify, redirect , url_for
import time

app = Flask(__name__)

#hold location of sqlite database
app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
	db.create_all()

#clear database
@app.route
class Urls(db.Model):
	id = db.Column("id_", db.Integer, primary_key = True)
	long = db.Column("long", db.String())
	short = db.Column("short", db.String(8))

	def __init__(self, long,short,id):
		self.long = long
		self.short = short
		self.id = id




#---------------------------------------------------------------
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
		
		#id		
		myUUID = uuid.uuid4()

		#short url	
		#hash_url  = str(hashlib.shake_256(str(url + str(time.time())).encode("UTF-8")).hexdigest(length=3))
		#hash_url = hashlib.shake_256(url.encode()).hexdigest() #add size of hash 

		new_url = Urls(url, "abcdefg" , myUUID)

		#add new row to database
		db.session.add(new_url)

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


