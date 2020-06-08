from ubuntu:18.04

ADD installCppLibs.sh /client/

WORKDIR /client

RUN apt update && apt -y install sudo git cmake g++

RUN ./installCppLibs.sh

RUN apt -y install python3-pip xsel

COPY . /client

RUN pip3 install -r requirements.txt

ENTRYPOINT python3 run.py
