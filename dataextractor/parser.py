# System Imports
# import re

# Local Imports
from analyze import DigestFile
from logger import get_logger
from reservoir import Excavator
import utils

# Global Parameters
log = get_logger(__name__)


class Parser(DigestFile):
    """This class does the following:
    Input: Text file to parse(file_name)
    Operations: Constructs data structures associated with the text file data
    based on the text patterns"""
    def __init__(cls, file_name):
        """Constructor"""
        cls.file_name = file_name
        DigestFile.__init__(cls, file_name)

    def __get_excavated_data(cls, data, ignore_patterns_list):
        """The idea here is that the object scope of the Excavator object
        should be specific to the input data. So, this is a Wrapper function
        to excavate data"""
        ex_obj = Excavator(data, ignore_patterns=ignore_patterns_list)
        return ex_obj.excavate_data()

    def extract_all_tables_from_file(cls):
        """Extracts all the tables from the text file and returns them"""
        contents = cls.get_table_of_contents()
        master_tables = []
        for iter in contents:
            (section_name, page_details) = iter
            section_header = utils.construct_header_from_name(section_name)
            master_tables.append({section_header: None})
            pages_to_read = utils.construct_page_numbers(page_details)
            # Start reading the pages and construct a DS based on patterns
            log.debug("Pages to read: %s for the section: %s" % (pages_to_read,
                                                                 section_name))
            content = []
            for page_num in pages_to_read:
                page_content = cls.return_page_contents_from_file(page_num)
                log.debug("The page content is: %s" % page_content)
                content.extend(page_content)

            if content:
                section_tables = cls.__get_excavated_data(
                        content,
                        ignore_patterns_list=[section_name]
                        )
                master_tables.append({section_header: section_tables})

            # Break here if you wanna check the table extraction for the 
            # first section
            # break

        return master_tables
