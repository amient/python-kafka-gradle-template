#!/usr/bin/env bash

DIR="$( cd $(dirname ${BASH_SOURCE[0]}) && pwd )"

if [ -z "$(brew ls --versions python3)" ]; then
    brew install python3
fi

if [ -z "$(brew ls --versions librdkafka)" ]; then
    brew install librdkafka
fi

if [ -z "$(brew ls --versions openssl)" ]; then
    brew install openssl
fi

source $DIR/python-setup.sh