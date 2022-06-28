FROM sirily11/secyan_python

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install setuptools
RUN pip3 install pipenv
RUN pip3 install pytest
WORKDIR /app
COPY . .
RUN pipenv install --skip-lock
WORKDIR /app/codegen

