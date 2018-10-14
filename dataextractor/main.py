# System Imports
import argparse

# Local Imports
from facade import Facade
from logger import get_logger

log = get_logger(__name__)

def parse_args():
    """
    Argument Parser
    """
    parser = argparse.ArgumentParser(
        'main.py',
        )
    parser.add_argument(
        '-f', '--file_name',
        metavar='FILE_NAME',
        required=True,
        help='Specify file name'
        )
    args = parser.parse_args()
    return args

def main():
    """Main function"""
    args = parse_args()
    obj = Facade(args.file_name)
    obj.get_page_contents_with_page_num(1)
    tables = obj.show_tables()
    print("Tables are: %s" % tables)

# Main function
if __name__ == '__main__':
    main()
