#!/bin/bash

# shellcheck disable=SC1091
source venv/bin/activate
make develop > log/make.log
./read-8BitDo-usb-input.sh > log/8BitDo.log &
audiobook-for-grandma --test --language fr --rate 450 --volume 0.1 
