# UI tests for Foundries Factory

## Installation

### Local installation

Local installation requires Chrome browser and Selenium driver.
Instructions assume running on Ubuntu

    apt-get -y update
    apt-get install -y wget libglib2.0-0 libnss3 python3-pip
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install google-chrome-stable
    pip install -r /home/requirements.txt

### Docker

Dockerfile contains all required dependencies

    docker build -t uitests .

## Running


### From repository

    python3 uitests.py --username <username> --password <password> createfactory --factory-name <name> --factory-machine <name from Foundries Factory dropdown>

### From container

    uitests --username <username> --password <password> createfactory --factory-name <name> --factory-machine <name from Foundries Factory dropdown>

