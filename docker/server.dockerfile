FROM sirily11/secyan_python

WORKDIR /app
RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install setuptools
RUN pip3 install pipenv
COPY . .
RUN pipenv install --skip-lock

