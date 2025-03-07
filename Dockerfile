#Docker Image
FROM debian:latest

RUN apt update && apt upgrade -y

#Installing Requirements
RUN apt install git curl python3-pip ffmpeg -y

#Updating Pip
RUN pip3 install -U pip

#Copying Requirements
COPY requirements.txt /requirements.txt
RUN cd /
RUN pip3 install -U -r requirements.txt
RUN mkdir /RadioPlayer
WORKDIR /RadioPlayer
COPY start.sh /start.sh

#Running Radio Player Bot
CMD ["/bin/bash", "/start.sh"]
