# this is the parent image we are using for our docker. every docker project must have parent image.
# for example someone that was mysql and python, installs another parent image which has python and mysql installed
FROM python:3.9-alpine3.15

#defining work directory of Docker container (we arbitrarily chose path in good manner)
WORKDIR /usr/src/app

#installment & update of packages using alpine package manager
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache sqlite-libs \
    && apk add --no-cache libffi-dev

#copies text file over into filesystem at path ./
#requirements.txt is list of python packages needs to be installed for our project
COPY requirements.txt ./

#installment of packages which are written inside requirements file
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

#copy everything from the same place as the dockerfile, to current directory in the container
COPY . .

# port for our users service (--host 0.0.0.0 --port 5500)
# we ran our code also on that port
EXPOSE 5500

# command simply to tell python which python file it must run when executed by the docker
CMD [ "python", "./shortner.py" ]
