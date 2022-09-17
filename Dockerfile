# For more information, please refer to https://aka.ms/vscode-docker-python
FROM ubuntu:22.04
LABEL maintainer="cyr-ius"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y python3 python3-dev python3-venv python3-systemd python3-dbus python3-firewall build-essential

# Install pip requirements
COPY requirements.txt .
RUN python3 -m venv --system-site-packages /env 
RUN /env/bin/pip3 install --upgrade pip
RUN /env/bin/pip3 install --no-cache-dir -r requirements.txt 

# clean content
RUN rm -rf /var/lib/apt/lists/*

COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

WORKDIR /opt
COPY ./app ./app
COPY ./migrations ./migrations

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]