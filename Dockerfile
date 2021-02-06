FROM python:3

ADD . /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./run.py" ]