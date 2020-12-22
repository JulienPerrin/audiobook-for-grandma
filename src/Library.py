import logging.config
import os
import yaml

from .BookFinder import BookFinder
from .BookReader import BookReader

from .model import Book

class Library():
    finder: BookFinder
    reader: BookReader
    
    def __init__(self, config_file, language):

        self.config = self.load_config(config_file)
        self.finder = BookFinder()
        test = self.config['test_language']
        self.reader = BookReader(test[language])

        # DO this once, in the top level class.
        logging.config.dictConfig(self.config['logging'])

    def run(self):
        # self.reader.readText(self.finder.findBook())
        self.reader.book = self.finder.findBook()
        self.reader.readBook() 

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def load_config(self, config_file):

        try:
            with open(config_file, 'r') as stream:
                config = yaml.load(stream)

        except yaml.YAMLError as e:
            print("Could not load configuration file. Error: {}".format(e))
            exit(1)
        except FileNotFoundError as e:
            print('Configuration file full path: {}'.format(
                os.path.abspath(config_file)))
            print("Configuration file {} could not be found. Error: {}".format(
                config_file, e))
            exit(1)
        except Exception as msg:
            print("Error while loading configuration file {}. Error: {}".format(
                config_file, msg))
            exit(1)

        logging.info(
            "Configuration file was successfully loaded. File name: {}".format(config_file))

        return config
