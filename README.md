# Audiobook for Grandma

This is a Raspberry Pi project for my blind grandmother, so that she can have an easy access to audiobooks online.

# Dev

## Installation

Tested on Linux running Ubuntu Server 24.04.3 LTS on a Raspberry 3 :

```bash
./install.sh
sudo reboot
```

For testing purpose the program will run on any Linux in theory. 

Also Mbrola is a nice voice on Linux.

The following command will download books to read : 

```bash
cd audiobook-for-grandma
#works if your language is french
#only tested in french, the download book solution would need some work in english
audiobook-for-grandma --offline --language fr
```

# Use

On the server has rebooted, you can connect the controller and type : 
  * B to start reading a book
  * A to stop reading
  * UP/DOWN to increase/decrease volume
  * LEFT/RIGHT to decrease/increase reading speed
  * SELECT to skip to the next book if grandma does not like the book that is currently read. Then an algorithm select a book based on her preferences (see select.sql file)
