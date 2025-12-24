#!/bin/bash

sudo apt update

sudo apt install python3 python3-venv -y
sudo apt install espeak espeak-ng alsa-utils ffmpeg libespeak1 joystick -y

sudo apt install python3 python3-venv -y

# install the voice that you like
# add MBrola voice to espeak
sudo apt install mbrola mbrola-fr1 mbrola-fr4 -y

# install python dependancies
python3 -m venv venv
# shellcheck source=/dev/null
source venv/bin/activate

pip install -r requirements.txt
python -m build
pip install dist/audiobook_for_grandma-0.21.tar.gz

#launch audiobook-for-grandma at startup
sudo cp afg.service /lib/systemd/system/afg.service
sudo chmod 644 /lib/systemd/system/afg.service
sudo systemctl daemon-reload
sudo systemctl enable afg.service
sudo systemctl start afg.service
