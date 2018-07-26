#!/usr/bin/env bash

DIR="$( cd $(dirname ${BASH_SOURCE[0]}) && pwd )"

#wget -qO - https://packages.confluent.io/deb/4.0/archive.key | sudo apt-key add -
#sudo add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/4.0 stable main"
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get -y update
sudo apt-get -y install python3.6 python3.6-dev
#sudo apt-get -y install librdkafka-dev
sudo apt-get -y install openssl

LIB_RD_KAFKA_VERISON="0.11.5-PRE1"
echo "Building librdkafka $LIB_RD_KAFKA_VERISON from sources.."
cd ~
curl --silent https://codeload.github.com/edenhill/librdkafka/tar.gz/v$LIB_RD_KAFKA_VERISON | tar xzf -
cd ~/librdkafka-$LIB_RD_KAFKA_VERISON
./configure --prefix=/usr 1>/dev/null
make -j 1>/dev/null
sudo make install 1>/dev/null
rm -fr ~/librdkafka-$LIB_RD_KAFKA_VERISON

cd $DIR
source $DIR/python-setup.sh

source $DIR/python-setup.sh
