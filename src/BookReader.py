from gtts import gTTS
import logging.config
import os
import yaml

# import vlc
# import time

import playsound


class BookReader():

    def readText(self, text: str) -> ():
        self.text = text
        self.read()

    def read(self) -> (): 
        tts = gTTS(text=self.text, lang="fr")
        path = 'out/mp3/hello.mp3'
        tts.save(path)
        # player = vlc.MediaPlayer(path)
        # player.play()
        # time.sleep(10)
        playsound.playsound(path)

    def __init__(self):
        self.text = ""
