#mandatory in Dockerfile for building parent image while also specifying version
FROM python:3.9-alpine3.15

#defining work directory of Docker container (we arbitrarily chose path in good manner)
WORKDIR /usr/src/app

#installment & update of packages using alpine package manager
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    #line 12 & 13 are needed because we use sqlite database
    && apk add --no-cache sqlite-libs \
    && apk add --update sqlite \
    && apk add --no-cache libffi-dev

#copies text file over into filesystem at path ./
#requirements.txt is list of python packages needs to be installed for our project
COPY requirements.txt ./
    
#installment of packages
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

#copy everything from the same place as the dockerfile, to current directory in the container
COPY . .

#port for our users service (--host 0.0.0.0 --port 5501)
EXPOSE 5501

#runs command to set up users database, as it needs to be created before it can be referred to 
CMD [ "python", "-u", "./users.py", "users.db"]
