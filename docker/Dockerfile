FROM ubuntu:20.04
LABEL description = "API RESTFUL with FAST API"
RUN apt update
RUN apt upgrade -y
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y sqlite3
RUN apt install -y tree
RUN apt install -y nano

# This section load the requirements in a variable to be installed in the current image
ENV requirements /home/requirements.txt 

COPY requirements.txt ${requirements}

RUN pip install -r /home/requirements.txt

WORKDIR /home/