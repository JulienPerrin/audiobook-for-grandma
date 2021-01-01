#!/bin/bash

source venv/bin/activate
make develop > make.log
./read-8BitDo-usb-input.sh > 8BitDo.log &
audiobook-for-grandma --test --language fr --rate 450 --volume 0.1 
