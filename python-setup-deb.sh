#!/usr/bin/env bash

DIR="$( cd $(dirname ${BASH_SOURCE[0]}) && pwd )"

wget -qO - https://packages.confluent.io/deb/4.0/archive.key | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/4.0 stable main"
sudo add-apt-repository ppa:jonathonf/python-3.6
apt-get -y update
apt-get -y install python3.6
apt-get -y install librdkafka-dev python3.6-dev
apt-get -y install openssl

source $DIR/python-setup.sh
