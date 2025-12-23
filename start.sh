#!/bin/bash

# shellcheck source=/dev/null
source venv/bin/activate

pip install -r requirements.txt
python -m build
#pip install -e
pip install dist/audiobook_for_grandma-0.21.tar.gz

./read-8BitDo-usb-input.sh >> log/8BitDo.log;
echo "App has been launched"