FROM python:3.9-alpine3.15

WORKDIR /usr/src/app

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache libsqlite3-dev \

COPY requirements.txt ./

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5500

CMD [ "python", "./shortner.py" ]