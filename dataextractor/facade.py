# System Imports

# Local Imports
from logger import get_logger
from parser import Parser
from ProspectExceptions import *

# Some Global Parameters
log = get_logger(__name__)


class Facade(object):
    """
    Main class which contains all the file related operations
    """
    def __init__(self, file_name):
        """Constructor to set file fd and analyze other generic patterns from
        the file"""
        self.file_name = file_name
        self.parser = Parser(file_name)

    def get_page_contents_with_page_num(self, page_num):
        """Returns page contents from the file"""
        content = self.parser.return_page_contents_from_file(page_num)
        if content:
            return content
        else:
            raise PageNotFoundException()

    def show_tables(self):
        """Returns all the tables available in the file"""
        tables = self.parser.extract_all_tables_from_file()
        if tables:
            return tables
        else:
            raise CannotFetchTablesException()
