FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
COPY requirements.txt /tmp/

RUN apt update && apt upgrade


# # mondodbインストール
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.0.list
RUN apt-get update && apt-get install -y mongodb-org

RUN mkdir -p /data/db
EXPOSE 27017
ENTRYPOINT ["/usr/bin/mongod"]

# RUN apt-get -y update \
#     && apt-get install -y software-properties-common build-essential git cmake\
#     && add-apt-repository universe 

RUN apt-get install -y python3 python3-pip
RUN apt-get install -y git python-is-python3
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt


# docker run -it --rm --mount type=bind,source=/Users/goodapple/Documents/卒論/実装,target=/project atsuki-test 

#cd /project/

