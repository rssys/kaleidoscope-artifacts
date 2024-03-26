# Use the official Ubuntu 22.04 LTS base image
FROM ubuntu:22.04

# Set noninteractive installation to avoid user interaction during build
ENV DEBIAN_FRONTEND=noninteractive

# Update the package repository and install packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
		libedit-dev swig libncurses5-dev python-dev-is-python3 cmake build-essential \
		swig libncurses5-dev \
		libgmp-dev libmpfr-dev git ssh vim texinfo flex bison
# Set the default command for the container

RUN apt-get install --reinstall -y ca-certificates

RUN git clone https://github.com/rssys/kaleidoscope-artifacts.git
WORKDIR /kaleidoscope-artifacts

RUN ./llvm-setup.sh

CMD ["bash"]
