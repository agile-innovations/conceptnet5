# This Dockerfile doesn't do anything with ConceptNet itself, but creates
# the kind of Python environment that ConceptNet runs best in. This is
# an environment with:
#
# - Python 3.4
# - a locale that supports Unicode
# - NumPy and SciPy
# - APSW
FROM python:3.4
MAINTAINER Rob Speer <rob@luminoso.com>

# Install Python dependencies
RUN apt-get update
RUN apt-get install -y build-essential python3-pip libatlas-dev liblapack-dev
RUN apt-get install -y gfortran

# set up Unicode in case Docker hasn't fixed this yet
ENV LANG C.UTF-8

# Install Python dependencies using pip
RUN pip install numpy scipy

# Install Ninja, a build dependency
RUN apt-get install -y ninja-build

# Install APSW
ADD apsw-3.8.5-r1.tar.gz /src/apsw
RUN cd /src/apsw/apsw-3.8.5-r1 && python3 setup.py fetch --sqlite --version=3.8.5 install
