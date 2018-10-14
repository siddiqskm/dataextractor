# System Imports
import re

# Local Imports
from logger import get_logger
from itertools import islice
import patterns
import utils

# Global Parameters
page_limit = 10
lines_per_read = 50
log = get_logger(__name__)


class DigestFile(object):
    """Digests the input file and generates various patterns for usage"""
    def __init__(cls, file_name):
        """Constructor"""
        cls.file_name = file_name
        cls.start_line_of_page = None
        cls.total_pages = None
        cls.patterns = cls.digest_file_to_generate_patterns()

    def __analyze_table_of_contents(cls):
        """Fetch the table of contents from the file specified"""
        contents_pattern = utils.construct_pattern_from_list(patterns.CONTENTS)
        log.debug("Contents pattern is: %s" % contents_pattern)
        contents = []
        start_breakpoint = False
        analyze_counter = 0
        with open(cls.file_name, 'r') as content:
            for line_no, line in enumerate(content, start=1):
                if line.strip():
                    matches = re.search(contents_pattern, line)
                    if matches and not start_breakpoint:
                        # Assuming we hit the 'contents' line let's enable
                        # breakpoint
                        log.debug("Pattern matches: %s, Setting the breakpoint" % line)
                        start_breakpoint = True
                    elif matches and len(matches.groups()) > 2 and \
                            start_breakpoint:
                        log.debug("Adding line: %s to the contents" % line)
                        analyze_counter = 0
                        col1 = matches.group(4).strip()
                        col2 = utils.remove_all_white_spaces(matches.group(5))
                        contents.append((col1, col2))
                        cls.start_line_of_page = line_no + 1
                    elif start_breakpoint and analyze_counter <= 5:
                        analyze_counter += 1
                    elif analyze_counter > 5:
                        # If we hit more than 5 lines successively that
                        # doesn't match any pattern in relation to the table
                        # of contents better to exit for now
                        break

        log.debug("Returning contents: %s" % contents)
        return contents

    def __analyze_page_patterns(cls):
        """Returns a dict with page numbers and range of line numbers (start,
        end) Format:
        Key: PageNumber
        Value: {start:end}
        """
        page_brk_pattern = utils.construct_pattern_from_list(patterns.PAGE_NO)
        pages = []
        with open(cls.file_name, 'r') as fd:
            start_index = cls.start_line_of_page
            for line_no, line in enumerate(fd, start=1):
                # log.debug('{} = {}'.format(line_no, line.strip()))
                matches = re.search(page_brk_pattern, line)
                if matches and matches.groups():
                    log.debug("pattern matched at: %s with %s"
                              % (line_no, matches.group(1)))
                    page_dict = {matches.group(2): (start_index, line_no)}
                    pages.append(page_dict)
                    start_index = line_no + 1

        log.debug("Returning pages: %s" % pages)
        return pages

    def digest_file_to_generate_patterns(cls):
        """Digest input file to generate several generic patterns"""
        resp_dict = {}
        resp_dict.update({'contents': cls.__analyze_table_of_contents()})
        resp_dict.update({'pages': cls.__analyze_page_patterns()})
        return resp_dict

    def get_total_num_of_pages_in_file(cls):
        """Returns total number of pages available in the file"""
        return len(cls.patterns.get('pages'))

    def return_page_contents_from_file(cls, input_page_num):
        """Returns the contents of the page from the file"""
        page_details = cls.patterns.get('pages')[input_page_num - 1]

        if page_details.get(str(input_page_num), None) is not None:
            (start, end) = page_details.get(str(input_page_num))
            log.debug("Start and end are: %s and %s" % (start, end))
            with open(cls.file_name, 'r') as content:
                lines_gen = list(islice(content, start, end))
            if lines_gen:
                log.debug("Lines read in the range: (%s, %s) are: %s"
                          % (start, end, lines_gen))
                return lines_gen
            else:
                return False
        else:
            log.error("Issue in retrieving page details")
            return False

    def get_table_of_contents(cls):
        """Returns the contents of the file in a structured format"""
        return cls.patterns.get('contents', None)
