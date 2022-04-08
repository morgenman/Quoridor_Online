# Base image
FROM python:latest
# update pip
ENV PYTHONUNBUFFERED=1
RUN pip3 install --upgrade pip & \
  pip3 install django mysqlclient requests django-compressor django-compressor-toolkit
ENV MYSQL_MAJOR 8.0
RUN apt-get update
RUN echo "deb http://repo.mysql.com/apt/debian/ buster mysql-${MYSQL_MAJOR}" > /etc/apt/sources.list.d/mysql.list & apt-get update & \
  apt-get -y --no-install-recommends install default-libmysqlclient-dev nodejs npm
RUN npm install -g yarn
WORKDIR /src