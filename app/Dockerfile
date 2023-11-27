FROM postgres:bookworm

RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

COPY init.sql /docker-entrypoint-initdb.d/

COPY . itudb2319
WORKDIR /itudb2319/app
RUN pip3 install -r requirements.txt --break-system-packages

# ENTRYPOINT ["python3"]
# CMD ["app.py", "init-db"]