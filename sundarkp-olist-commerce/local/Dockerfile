FROM mageai/mageai:latest
ARG PIP=pip3
    
# Add Debian Bullseye repository
RUN echo 'deb http://deb.debian.org/debian bullseye main' > /etc/apt/sources.list.d/bullseye.list
    
RUN apt-get update -y && \
    apt-get install -y default-jdk && \
    apt-get install -y default-jre && \
    apt-get install -y scala
    
# Remove Debian Bullseye repository
RUN rm /etc/apt/sources.list.d/bullseye.list

RUN ${PIP} install --no-cache-dir --upgrade pip 
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install  -r /tmp/requirements.txt

WORKDIR /home/src

ENV MAGE_DATA_DIR=${PWD}/mage_data