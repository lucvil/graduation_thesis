FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
COPY requirements.txt /tmp/

RUN apt-get update && apt-get -y upgrade

# RUN apt-get -y update \
#     && apt-get install -y software-properties-common build-essential git cmake\
#     && add-apt-repository universe 

RUN apt-get install -y python3 python3-pip
RUN apt-get install -y git python-is-python3
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

#mongodb
RUN apt-get update && apt-get install -y gnupg2
RUN apt-get update && apt-get install -y wget
RUN wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
RUN apt-get update && apt-get install -y mongodb-org

#イメージを作る
#docker build -t atsuki-test .

#普段はここから
# 自宅mac
# docker run -it --rm --mount type=bind,source=/Users/goodapple/Documents/卒論/実装,target=/project atsuki-test 
# lab mac
# docker run -it --rm --mount type=bind,source=/Users/sail/Documents/吉村/卒論/graduation_thesis,target=/project atsuki-test
#cd /project/

#入った後
#backでmongodbを起動
#mongod --fork --config /etc/mongod.conf
#mongoshで入れるようになる

#コンテナに入るには
#docker ps でコンテナIDをみる
#docker container exec -it コンテナID bash

