#!/bin/bash

cd
cd audiobook-for-grandma
source venv/bin/activate
make develop > log/make.log
./read-8BitDo-usb-input.sh >> log/8BitDo.log;
