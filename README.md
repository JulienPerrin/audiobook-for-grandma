# Audiobook for Grandma

This is a Raspberry Pi project for my blind grandmother, so that she can have an easy access to audiobooks online.

# Dev

## Installation

On Linux, you additionally need to install espeak , ffmpeg and libespeak1 as shown below: :

```bash
sudo apt update
sudo apt install python3 python3-venv
sudo apt install espeak ffmpeg libespeak1

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py sdist bdist_wheel
python setup.py develop
pip install dist/audiobook_for_grandma-0.21.tar.gz
```

Also Mbrola is a nice voice on Linux.

# Use

```bash
./start.sh
```