FROM sirily11/secyan_python

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install setuptools
RUN pip3 install secyan_python
COPY . .
RUN python3 setup.py install
RUN python3 -c "import codegen"

RUN apt-get install -y postgresql-plpython3-12