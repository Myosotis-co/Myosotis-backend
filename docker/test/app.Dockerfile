# Dockerfile

# pull the official docker image
FROM python:3.9-slim

# set work directory
WORKDIR /deletemehere

RUN apt-get update -y -q && \
    apt-get upgrade -y -q && apt-get install git -y -q && apt-get install dos2unix
    
# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements/base.txt .
RUN pip install -r base.txt

# copy project
COPY . .


COPY test/scripts/wait-for-it.sh /bin/wait-for-it.sh
RUN ["chmod", "u+x", "/bin/wait-for-it.sh"]
RUN ["dos2unix", "/bin/wait-for-it.sh"]