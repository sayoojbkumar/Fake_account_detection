FROM python:3.9

ADD . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN pip3 install pandas

CMD [ "python3", "server.py"]