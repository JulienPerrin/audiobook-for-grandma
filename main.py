'''
This is a scrip that will be used in the setup.py as an entry point.
Instantiate all your classes here.
'''
import argparse
import sys

from src import project_root
from src.DB import DB
from src.Library import Library
from src.model.Book import Book

VOLUME_CHANGE: float = 0.05
RATE_CHANGE: int = 10


def parse_input_args(argv):
    ''' Parses command line arguments '''

    parser = argparse.ArgumentParser(
        description='''This app is made to allow old people to have an easy access to books of the Gutenberg library.
        It is especially made for people with sight disabilities. ''')
    parser.add_argument('--test', help="Test the app.", action='store_true')
    parser.add_argument('--start', help="Start the app.", action='store_true')
    parser.add_argument('--stop', help="Stop the app.", action='store_true')
    parser.add_argument('--skip', help="Stop the app.", action='store_true')
    parser.add_argument(
        '--offline', help="Download all the books of the gutenberg library for the selected language, so that the app can work offline", action='store_true')
    parser.add_argument(
        '--language', help="set the language of the books that are read", action='store')
    parser.add_argument('--voice', help="Set the voice that pyttsx3 will use to make sound. On Linux, MBrola voices work too (see https://github.com/numediart/MBROLA-voices to install an MBrola voice). ", action='store')
    parser.add_argument(
        '--rate', help="the number of words per minute", action='store')
    parser.add_argument(
        '--volume', help="the volume between 0.0 and 1.0", action='store')
    parser.add_argument(
        '--lower', help="Lower reader voice.", action='store_true')
    parser.add_argument(
        '--higher', help="Raise reader voice.", action='store_true')
    parser.add_argument(
        '--slower', help="Slow reader voice.", action='store_true')
    parser.add_argument(
        '--faster', help="Raise reader voice.", action='store_true')
    return parser.parse_args()


def start(config_file, parsed_args):
    print("Starting the app.")
    print("language:", parsed_args.language)
    print("rate:", parsed_args.rate)
    print("volume:", parsed_args.volume)
    print("voice: ", parsed_args.voice)
    if parsed_args.language is None:
        raise ValueError("Language is mandatory with value error")
    library = Library(configFile=config_file, language=parsed_args.language,
                      defaultRate=parsed_args.rate, defaultVolume=parsed_args.volume, voice=parsed_args.voice)
    library.run()


def stop(config_file, parsed_args):
    print("Stopping the app.")
    db = DB()
    lastBook: Book = db.lastBook()
    if lastBook is None:
        raise ValueError("Impossible to stop as books where never read")
    db.updateContinueReading(False, db.lastBook().identifier)
    print("Reader will continue running : {}".format(
        bool(db.isContinueReading())))


def offline(config_file, parsed_args):
    print("Downloading the books. ")
    print("language:", parsed_args.language)
    if parsed_args.language is None:
        raise ValueError("Language is mandatory with value error")
    library = Library(configFile=config_file,
                      language=parsed_args.language, defaultRate=115, defaultVolume=0.5, voice='en1')
    library.downloadBooksForAppToWorkOffline()
    print("All books have been downloaded. ")


def execute_script(input_args):
    config_file = "{}/config.yaml".format(project_root.path())
    parsed_args = parse_input_args(input_args)

    if parsed_args.test:
        db = DB()
        db.test()

    if parsed_args.start or parsed_args.test:
        start(config_file, parsed_args)

    if parsed_args.stop:
        stop(config_file, parsed_args)

    if parsed_args.skip:
        db = DB()
        db.skip()
        print("Reader will skip to next book. ")

    # download all books of a certain language
    if parsed_args.offline:
        offline(config_file, parsed_args)

    # increase/decrease volume
    if parsed_args.lower:
        print("Lower volume. ")
        db = DB()
        db.setVolume(max(0.0, db.getVolume() - VOLUME_CHANGE))
        print("New volume: ", db.getVolume())
    if parsed_args.higher:
        print("Raise volume. ")
        db = DB()
        db.setVolume(min(1.0, db.getVolume() + VOLUME_CHANGE))
        print("New volume: ", db.getVolume())

    # increase/decrease rate of speech
    if parsed_args.slower:
        print("Lower speech rate. ")
        db = DB()
        db.setRate(max(10, db.getRate() - RATE_CHANGE))
        print("New rate: ", db.getRate())
    if parsed_args.faster:
        print("Raise speech rate. ")
        db = DB()
        db.setRate(min(1000, db.getRate() + RATE_CHANGE))
        print("New rate: ", db.getRate())


def main():
    # Entry point to the app. Call in test method
    execute_script(sys.argv[1:])


if __name__ == "__main__":
    main()
