# Larger, more convenient for development
FROM --platform=linux/arm64 ubuntu:22.04 AS dev 

RUN apt-get -y update &&\
 apt-get -y upgrade

RUN  apt-get install -y \
 software-properties-common  #For add-apt-repository

# Prompts for user input, send empty string to accept default
RUN echo "" | add-apt-repository ppa:deadsnakes/ppa 

RUN apt-get -y update
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York

RUN apt-get install -y \
    python3.12 python3.12-venv
    # python3.12-dev python3.12-distutils # Not strictly necessary

# Install pip
RUN python3.12 -m ensurepip --upgrade
# 3.10 is the default. We want 3.12
RUN rm /usr/bin/python3 
RUN ln -s /usr/bin/python3.12 /usr/bin/python3
RUN ln -s /usr/bin/python3.12 /usr/bin/python

COPY requirements.txt /tmp
RUN python -m pip install -r /tmp/requirements.txt

# TODO: Define code that runs the backend (currently its scripts expected to be run 1 after another manually)
CMD ["sleep", "infinity"]

#Leaner image
FROM python:3.12.8-bullseye AS prod 

COPY requirements.txt /tmp
# Use 3.12 for all the stuff we care about (older versions for attempting remediating builds)
RUN python -m pip install -r /tmp/requirements.txt

# TODO: Define code that runs the backend (currently its scripts expected to be run 1 after another manually)
CMD ["sleep", "infinity"]