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
        description="Description of the app that will be displayed when the script is executed.")
    parser.add_argument('--test', help="Test the app.", dest="test",
                        action='store_true', required=False)
    return parser.parse_args()


def execute_script(input_args):
    config_file = "{}/config.yaml".format(project_root.path())
    parsed_args = parse_input_args(input_args)

    if parsed_args.test:
        print("Testing the app.")
        classObject = Library(config_file)
        classObject.run()


def main():
    # Entry point to the app. Call in test method
    execute_script(sys.argv[1:])


if __name__ == "__main__":
    main()
