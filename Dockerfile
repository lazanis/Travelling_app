FROM python:3.8

WORKDIR /Travelling_companion
ADD . /Travelling_companion

RUN pip3 install pip --upgrade
RUN pip3 install -r requirements.txt
