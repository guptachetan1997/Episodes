FROM ubuntu:bionic

RUN mkdir /episodes /data
WORKDIR /episodes


RUN set -ex && export DEBIAN_FRONTEND=noninteractive && apt update && apt install -yqq git python3 python3-pip python3-numpy python3-scipy python3-pandas

RUN git clone https://github.com/guptachetan1997/Episodes.git /episodes
RUN pip3 install -r requirements.txt

EXPOSE 8000
VOLUME /data
ENV DATA_DIR /data

ENTRYPOINT bin/server.sh


