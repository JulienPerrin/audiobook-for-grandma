#!/bin/bash

source venv/bin/activate
make develop > make.log
./read-8BitDo-usb-input.sh > 8BitDo.log;
