# For more information, please refer to https://aka.ms/vscode-docker-python
FROM ubuntu:21.10

# set version label
ARG BUILD_DATE
ARG VERSION
ARG FIREWALLUI_RELEASE
LABEL build_version="version:- ${VERSION} Build-date:- ${BUILD_DATE}"
LABEL maintainer="cyr-ius"

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y python3 python3-venv python3-systemd python3-dbus python3-firewall

# Install pip requirements
COPY requirements.txt .
RUN python3 -m venv --system-site-packages /env \
    && /env/bin/pip3 install --upgrade pip \
    && /env/bin/pip3 install --no-cache-dir -r requirements.txt 

# clean content
RUN rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

WORKDIR /app
COPY ./fwui /app/fwui
COPY ./static /app/static

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ENV FLASK_APP=fwui

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]