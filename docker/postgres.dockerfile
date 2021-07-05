FROM ubuntu:20.04

ENV TZ=Europe/Minsk
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y python3-pip
RUN apt install -y libssl-dev
RUN apt install -y libgmp-dev
RUN apt install -y libboost-all-dev
RUN apt install -y cmake

# Required for python binding
RUN apt install -y ninja-build
RUN apt install --no-install-recommends -y python3-dev
RUN apt-get install -y build-essential \
    gcc \
    g++ \
    gdb \
    clang \
    cmake \
    rsync \
    tar \
    python \
  && apt-get clean

RUN apt install -y git

# Build pybind11
WORKDIR /usr/local/build
RUN git clone https://github.com/pybind/pybind11.git
WORKDIR /usr/local/build/pybind11
RUN mkdir build
WORKDIR /usr/local/build/pybind11/build
RUN cmake ..
RUN make install -j8

WORKDIR /app
# Install secyan_python
RUN git clone --recurse-submodules https://github.com/sirily11/SECYAN
WORKDIR /app/SECYAN
RUN python3 setup.py install