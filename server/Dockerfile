FROM python:3.6-alpine

LABEL maintainer="ro6ley <robleyadrian@gmail.com>"

EXPOSE 8000

RUN apk --update add ${packages} && rm -rf /var/cache/apk/*

RUN pip3 install pipenv gunicorn

ADD . /lace

WORKDIR /lace

RUN pip install -r requirements.txt

RUN python lace/manage.py makemigrations

RUN python lace/manage.py migrate

CMD [ "python", "lace/manage.py", "runserver", "0.0.0.0:8000" ]
