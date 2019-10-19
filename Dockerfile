# Pulling python from the official image 
FROM python:3.7.3

# Updating apt and installing necesary packages
RUN apt-get update && apt-get install -y \
    binutils \
    python3-dev \
    pkg-config \
    libghc-hdbc-postgresql-dev

# Installing python package manager 'pip'
RUN pip3 install --upgrade pip   

# Installing pipenv to manage the virtual environment
RUN pip3 install pipenv==2018.11.26

# Making a directory to store the back end code 
RUN mkdir -p /src/
WORKDIR /src/

# Copying all the files from the current directory (local machine) to the container 
# that is created by docker 
COPY . /src/

# Installing all the packages from the pipfile to the virtual environment
RUN pipenv install --system --dev --deploy
