#!/bin/bash

# shellcheck source=/dev/null
source venv/bin/activate

echo "============== pip install requirements =================="
pip install  --upgrade -r requirements.txt
echo "============== python -m pip install . =================="
python -m pip install .
echo "============== python -m build =================="
python -m build
#pip install -e
echo "============== pip install dist/audiobook_for_grandma-0.21.tar.gz =================="
pip install dist/audiobook_for_grandma-0.21.tar.gz

./read-8BitDo-usb-input.sh > log/8BitDo.log &
audiobook-for-grandma --test --language fr --rate 450 --volume 0.1  --voice mbrola-fr1