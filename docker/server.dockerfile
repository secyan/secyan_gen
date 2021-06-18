FROM ubuntu:20.04
# Install build dependencies

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install -y build-essential \
    gcc \
    g++ \
    gdb \
    clang \
    cmake \
    rsync \
    tar \
    python \
  && apt-get clean

RUN apt install cmake
RUN apt install -y libssl-dev
RUN apt install -y libgmp-dev
RUN apt install -y libboost-all-dev
RUN apt install -y ninja-build
RUN apt install --no-install-recommends -y python3 python3-pip python3-dev
RUN apt install -y git
# Build pybind11
WORKDIR /usr/local/build
RUN git clone https://github.com/pybind/pybind11.git
WORKDIR /usr/local/build/pybind11
RUN mkdir build
WORKDIR /usr/local/build/pybind11/build
RUN cmake ..
RUN make install -j8
# Install Python dependencies
WORKDIR /app
RUN pip install pipenv
COPY Pipfile Pipfile
RUN pipenv install --skip-lock
# Install secyan_python
RUN git clone --recurse-submodules https://github.com/sirily11/SECYAN
WORKDIR /app/SECYAN
RUN pipenv run python3 setup.py install
WORKDIR /app/codegen

