'''
This is a scrip that will be used in the setup.py as an entry point.
Instantiate all your classes here.
'''
import argparse
import sys
from src import project_root
from src.Library import Library


def parse_input_args(argv):
    ''' Parses command line arguments '''

    parser = argparse.ArgumentParser(
        description='''This app is made to allow old people to have an easy access to books of the Gutenberg library. 
        It is especially made for people with sight disabilities. ''')
    parser.add_argument('--test', help="Test the app.", action='store_true')
    parser.add_argument('--start', help="Start the app.", action='store_true')
    parser.add_argument('--stop', help="Stop the app.", action='store_true')
    parser.add_argument('--language', help="set the language of the books that are read", choices=['fr', 'en'], action='store')
    return parser.parse_args()


def execute_script(input_args):
    config_file = "{}/config.yaml".format(project_root.path())
    parsed_args = parse_input_args(input_args)

    library = Library(config_file, parsed_args.language)

    if parsed_args.start or parsed_args.test:
        print("Starting the app.")
        library = Library(config_file, parsed_args.language)
        library.run()

    if parsed_args.stop:
        if not library:
            raise ValueError('The app has not started. ')
        print("Stopping the app.")
        library.stopReading()


def main():
    # Entry point to the app. Call in test method
    execute_script(sys.argv[1:])


if __name__ == "__main__":
    main()
