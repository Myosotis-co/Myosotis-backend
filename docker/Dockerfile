# Dockerfile

# pull the official docker image
FROM python:3.9-slim



# set work directory
WORKDIR /deletemehere

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements/base.txt .
RUN pip install -r base.txt

# copy project
COPY . .


