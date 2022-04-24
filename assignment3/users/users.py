import uuid
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
from auth import Token

app_db = Flask(__name__)

# hold location of sqlite database
app_db.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app_db.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app_db)
newToken = Token()


class User(db.Model):
    user_id = db.Column("user_id", db.String(), primary_key=True)
    user = db.Column("user", db.String())
    password = db.Column("password", db.String())
    token = db.Column("token", db.String())

    def __init__(self, user_id, user, password, token):
        self.user_id = user_id
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
    user_id = str(uuid.uuid4())

    # check for duplicate user before adding
    if User.query.filter_by(user=user).first() is None:
        new_user = User(user_id, user, password, None)
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

        # create token for login
        print('user=', user)
        print('password=', password)
        token = newToken.createToken(user)
        print('token=', token)
        user_record.token = token
        db.session.commit()

        return token, 200


@app_db.route('/users/logout', methods=['POST'])
def logout():
    if "Authorization" in request.headers.keys():
        token = request.headers['Authorization']
    else:
        token = None

    user_record = User.query.filter_by(token=token).first()
    if user_record is not None:
        user_record.token = None
        db.session.commit()
        return "user successfully logged out", 200
    # we can also redirect to homepage or login page but we do not have UI here
    else:
        return "User is not logged in", 401


def logoutDB(token):
    if "Authorization" in request.headers.keys():
        token = request.headers['Authorization']
    else:
        token = None

    user_record = User.query.filter_by(token=token).first()
    if user_record is not None:
        user_record.token = None
        db.session.commit()
        
if __name__ == "__main__":
    app_db.run(host="0.0.0.0", port=5501, debug=True)
