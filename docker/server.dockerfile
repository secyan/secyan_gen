FROM sirily11/secyan_python

WORKDIR /app
RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install setuptools
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN python3 -c "from flask import Flask"
EXPOSE 5000
