FROM ubuntu:22.04
RUN DEBIAN_FRONTEND=noninteractive apt-get -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y wget libglib2.0-0 libnss3 python3-pip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install google-chrome-stable
COPY requirements.txt /home/
RUN pip install -r /home/requirements.txt

COPY uitests.py /usr/bin/uitests
