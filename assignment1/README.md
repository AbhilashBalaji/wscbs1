# SETUP

* Setup a Virtual environment\
    `python3 -m venv venv`

* run\
`pip[3] install -r requirements.txt`

* export FLASKAPP (look at flask docs)

* flask run


# RUN methods

* /:id - POST : give body {"url": <some url>}, port
    201: returns shorturl created for <some url>
    400: invalid <some url>
* /:id - GET => no body, port/shorturl 
      301: redirects to to url 
      404: invalid shorturl
* / - GET : port, returns list of ID's (short urls)
* /:id - PUT: give body {"longurl": <some url>} , port/shorturl
    400: give invalid <some url>
    404: give invalid shorturl
    
* /:id - DELETE: port/shorturl
    204: deletes that entry 
    404: shorturl that was never stored/created
    
* / - DELETE: port
    404
