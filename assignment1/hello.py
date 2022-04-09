import os
import uuid
from flask_sqlalchemy import SQLAlchemy
import hashlib
from os import strerror
import random
import re
from flask import Flask, request, abort, jsonify, redirect, url_for
import time

app = Flask(__name__)

# hold location of sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Urls(db.Model):
    guid = db.Column("guid", db.String(), primary_key=True)
    long = db.Column("long", db.String())
    short = db.Column("short", db.String())

    def __init__(self, long, short, identifier):
        self.long = long
        self.short = short
        self.guid = identifier


@app.before_first_request
def create_tables():
    db.create_all()


# ---------------------------------------------------------------
regex = re.compile(
    r'^(?:http)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def url_valid(url):
    return re.match(regex, url) is not None


@app.route("/", methods=['POST'])
def shorten():

    url = request.json['url']
    found_url = Urls.query.filter_by(long=url).first()
    print(url)
    print(found_url)
    if found_url:
        return f"{found_url.short}"
        # return redirect(url_for("display_short_url", url=found_url.short))
    if url_valid(url):

        # id
        myUUID = str(uuid.uuid4())
        print(myUUID)
        # short url
        # hash_url  = str(hashlib.shake_256(str(url + str(time.time())).encode("UTF-8")).hexdigest(3))
        # hash_url = hashlib.shake_256(url.encode()).hexdigest() #add size of hash
        hash_url = hash_generator(url)

        new_url = Urls(url, hash_url, myUUID)

        # add new row to database
        db.session.add(new_url)
        db.session.commit()

        return str(hash_url), 201
    else:
        # url entered is not valid. TEST
        return "URL Not valid format.", 400


def hash_generator(url):
    return str(hashlib.shake_256(str(url + str(time.time())).encode("UTF-8")).hexdigest(3))


@app.route("/<potato_id>", methods=['GET'])
def potato(potato_id):
    url_record = Urls.query.filter_by(short=potato_id).first()
    if url_record:
        return redirect(url_record.long)
    else:
        return "URL does not exist", 404


@app.route("/", methods=["GET"])
def getAllPotatoes():
    return ''  # jsonify({"IDs":list(storage.keys())})


@app.route("/<id>", methods=['DELETE'])
def potatodelete(id):
    # if id in storage.keys():
    #	del storage[id]
    #	return "",204
    # else:
    return "Shortened URL not found", 404


@app.route("/", methods=['DELETE'])
def potatodontdelete():
    return "", 404


def bad_request(message):
    response = jsonify({'message': message})
    response.status_code = 400
    return response
