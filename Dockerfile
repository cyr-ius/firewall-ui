# For more information, please refer to https://aka.ms/vscode-docker-python
FROM ubuntu:22.04
LABEL maintainer="cyr-ius"
LABEL org.opencontainers.image.description "Firewall-UI is a webinterface for firewalld"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install dependencies
RUN apt-get update && apt-get install -y python3 python3-dev python3-venv python3-systemd python3-dbus python3-firewall build-essential tzdata

# Install pip requirements
ADD requirements.txt .
RUN python3 -m venv --system-site-packages /env 
RUN /env/bin/pip3 install --upgrade pip
RUN /env/bin/pip3 install --no-cache-dir -r requirements.txt 

# clean content
RUN rm -rf /var/lib/apt/lists/*

ADD docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

RUN mkdir /app
WORKDIR /app
ADD ./src ./src
ADD ./migrations ./migrations

VOLUME /app/static
VOLUME /app/database

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]