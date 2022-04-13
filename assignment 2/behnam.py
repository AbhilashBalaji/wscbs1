import os
import uuid
from flask_sqlalchemy import SQLAlchemy
import hashlib
from os import strerror
import random
import re
from flask import Flask, request, abort, jsonify, redirect, url_for
import time
from auth import Token


app_db = Flask(__name__)

# hold location of sqlite database
app_db.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app_db.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app_db)
newToken = Token()

class User(db.Model):
    user = db.Column("user", db.String(), primary_key=True)
    password = db.Column("password", db.String())
    token = db.Column("token", db.String())

    def __init__(self, user, password, token):
        self.user = user
        self.password = password
        self.token = token


@app_db.before_first_request
def create_tables():
    db.create_all()


@app_db.route('/users', methods=['POST'])
def create_user():
    user = request.json['user']
    password = request.json['password']

    # check for duplicate user before adding
    if User.query.filter_by(user=user).first() is None:
        new_user = User(user, password, "")
        db.session.add(new_user)
        db.session.commit()


        return "user created successfully", 200
    else:
        return "user name already exists", 409


@app_db.route('/users/login', methods=['POST'])
def login():
    # check if user exists
    user = request.json['user']
    password = request.json['password']
    user_record = User.query.filter_by(user=user, password=password).first()

    if user_record is None:
        return "forbidden", 403
    else:

	#create token for login	
	token = newToken.createToken(user)
        user_record.token = token
        db.session.commit()

        return token, 200
