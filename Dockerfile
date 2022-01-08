# Using Python 3.8 NodeJS 12 (Base Image)
FROM python:3.9

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Gets the gpg signature of the psql repo
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

#installs lsb-release
RUN apt-get update && apt-get -y install lsb-release

# Add psql source
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster"-pgdg main | tee  /etc/apt/sources.list.d/pgdg.list

# Install psql
RUN apt-get update && apt-get -y install postgresql-client-12

# create root directory for our project in the container
RUN mkdir /app

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents isnto the container at /app
COPY . /app/

# Upgrades pip
RUN pip install --upgrade pip

# Installs poetry
RUN pip install poetry

# Disable virtual env creation
RUN poetry config virtualenvs.create false --local

# Install any needed packages
RUN poetry install --no-root --no-dev -n

# Maintainer => Dimitrios Strantsalis
LABEL maintainer="dstrants@gmail.com"
