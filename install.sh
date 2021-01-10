sudo apt update

sudo apt install make

# install espeak (TTS reader)
sudo apt install espeak -y
# add MBrola voice to espeak
cd ~/Downloads/
wget https://raspberry-pi.fr/download/espeak/mbrola3.0.1h_armhf.deb -O mbrola.deb
# install the voice that you like
sudo apt install mbrola-fr4 -y

# use python3 as default
sudo apt install python3 -y

# install python dependancies
pip install wheel setuptools
sudo -H pip install virtualenv

#install project audiobook-for-grandma
cd
git clone https://github.com/JulienPerrin/audiobook-for-grandma
cd audiobook-for-grandma
virtualenv venv
easy_install PyYAML
/home/pi/audiobook-for-grandma/venv/bin/python -m pip install --upgrade pip
sudo cp afg.service /lib/systemd/system/afg.service
sudo chmod 644 /lib/systemd/system/afg.service
sudo systemctl daemon-reload
sudo systemctl enable afg.service
sudo systemctl start afg.service