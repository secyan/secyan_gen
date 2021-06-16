# [Choice] Debian / Ubuntu version: debian-10, debian-9, ubuntu-20.04, ubuntu-18.04
ARG VARIANT=buster
FROM mcr.microsoft.com/vscode/devcontainers/cpp:0-${VARIANT}

# [Optional] Uncomment this section to install additional packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
ENV TZ=Europe/Minsk
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install -y ssh \
    build-essential \
    gcc \
    g++ \
    gdb \
    clang \
    cmake \
    rsync \
    tar \
    python \
  && apt-get clean

RUN useradd -m user \
  && yes password | passwd user

RUN apt install cmake
RUN apt install -y libssl-dev
RUN apt install -y libgmp-dev
RUN apt install -y libboost-all-dev
# Required for python binding
RUN apt install -y ninja-build
RUN apt install --no-install-recommends -y python3 python3-pip python3-dev
RUN apt install -y git
WORKDIR /usr/local/project
RUN git clone https://github.com/pybind/pybind11.git
WORKDIR /usr/local/project/pybind11
RUN mkdir build
WORKDIR /usr/local/project/pybind11/build
RUN cmake ..
RUN make install -j8
# Install node js
RUN apt install -y nodejs
WORKDIR /usr/local/project