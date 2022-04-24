# HOW TO
* run pip3 install -r requirements.txt
* 
* set ``FLASK_APP=hello ``\
* `` flask run --port 6000``

* on a new terminal 

* set ``FLASK_APP=behnam``\
* ``flask run --port 6001``
* Token will be in the Authorization header \
* CREATE USER: @app_db.route('/users', methods=['POST']): Body needs {user: "user1", password: "password1"} \
* LOGIN USER: @app_db.route('/users/login', methods=['POST']) : Body needs {user: "user1", password: "password1"} -> returns Authorization Key (in header) \
* 
