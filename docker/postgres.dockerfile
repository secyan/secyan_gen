FROM sirily11/secyan_python

WORKDIR /app/SECYAN-GEN
COPY . .
COPY setup.py setup.py
RUN python3 setup.py install
RUN python3 -c 'import codegen'