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


def parse_input_args(argv):
    ''' Parses command line arguments '''

    parser = argparse.ArgumentParser(
        description='''This app is made to allow old people to have an easy access to books of the Gutenberg library. 
        It is especially made for people with sight disabilities. ''')
    parser.add_argument('--test', help="Test the app.", action='store_true')
    parser.add_argument('--start', help="Start the app.", action='store_true')
    parser.add_argument('--stop', help="Stop the app.", action='store_true')
    parser.add_argument('--skip', help="Stop the app.", action='store_true')
    parser.add_argument('--offline', help="Download all the books of the gutenberg library for the selected language, so that the app can work offline", action='store_true')
    parser.add_argument('--language', help="set the language of the books that are read",
                        choices=['fr', 'en'], action='store')
    parser.add_argument(
        '--rate', help="the number of words per minute", action='store')
    parser.add_argument(
        '--volume', help="the volume between 0.0 and 1.0", action='store')
    return parser.parse_args()


def execute_script(input_args):
    config_file = "{}/config.yaml".format(project_root.path())
    parsed_args = parse_input_args(input_args)

    if parsed_args.test:
        db = DB()
        db.test()
        
    if parsed_args.start or parsed_args.test:
        print("Starting the app.")
        print("language:", parsed_args.language)
        print("rate:", parsed_args.rate)
        print("volume:", parsed_args.volume)
        if parsed_args.language is None:
            raise ValueError("Language is mandatory with value error")
        library = Library(configFile=config_file, language=parsed_args.language,
                          rate=parsed_args.rate, volume=parsed_args.volume)
        library.run()

    if parsed_args.stop:
        print("Stopping the app.")
        db = DB()
        lastBook: Book = db.lastBook()
        if lastBook is None:
            raise ValueError("Impossible to stop as books where never read")
        db.updateContinueReading(False, db.lastBook().identifier)
        print("Reader will continue running : {}".format(
            bool(db.isContinueReading())))

    if parsed_args.skip:
        db = DB()
        db.skip()

    if parsed_args.offline:
        print("Downloading the books. ")
        print("language:", parsed_args.language)
        if parsed_args.language is None:
            raise ValueError("Language is mandatory with value error")
        library = Library(configFile=config_file, language=parsed_args.language,
                          rate=parsed_args.rate, volume=parsed_args.volume)
        library.downloadBooksForAppToWorkOffline()
        print("All books have been downloaded. ")

def main():
    # Entry point to the app. Call in test method
    execute_script(sys.argv[1:])


if __name__ == "__main__":
    main()
