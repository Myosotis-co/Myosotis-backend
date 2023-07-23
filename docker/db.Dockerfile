FROM postgres:15

RUN apt-get update -y -q && \
    apt-get install git -y -q && \
    apt-get install dos2unix

COPY ./scripts/init-db.sh /docker-entrypoint-initdb.d/init-db.sh
RUN chmod u+x /docker-entrypoint-initdb.d/init-db.sh

RUN dos2unix /docker-entrypoint-initdb.d/init-db.sh