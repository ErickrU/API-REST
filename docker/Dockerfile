FROM ubuntu:20.04
RUN apt update
RUN apt upgrade -y
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y sqlite3

ENV requirements /home/requirements.txt 

COPY requirements.txt ${requirements}

RUN pip install -r /home/requirements.txt

WORKDIR /home/