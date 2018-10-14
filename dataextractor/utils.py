# System Imports

# Local imports
from logger import get_logger
import patterns


log = get_logger(__name__)


def get_file_descriptor(file_name, mode):
    """Returns back file descriptor"""
    try:
        return open(file_name, mode)
    except Exception as e:
        log.exception("Issue opening file: %s, %s" % (file_name, e))
        return None


def get_file_read_descriptor(file_name):
    """Returns back read fd for the file specified"""
    return get_file_descriptor(file_name, 'r')


def construct_pattern_from_list(input_list):
    """Constructs a pattern from the list specified"""
    return '(' + '|'.join(input_list) + ')'


def remove_all_white_spaces(string):
    """Removes all the white spaces available in the string"""
    stripped_str = string.strip()
    return stripped_str.replace(" ", "")


def construct_page_numbers(page_str):
    """Returns the list of page numbers available in the input page_details"""
    # For now let's just get the ball rolling by assuming separator is '-' for
    # now. But the idea is to find out the seperator from the string and then
    # split it based on the sep to fetch the page numbers range
    page_seperator = '-'
    indices = page_str.split(page_seperator)
    if len(indices) == 1:
        return [int(iter) for iter in indices]
    elif len(indices) == 2:
        # Assuming we got a range
        return range(int(indices[0]), int(indices[1]) + 1)
    else:
        return None


def construct_header_from_name(name_str):
    """Returns a header format string from the input string"""
    header_name = name_str.upper()
    return header_name.replace(" ", "_")


def generate_possible_patterns(list_of_strings):
    """Returns all the possible patterns that can be derived from the input
    string"""
    recorder = []
    recorder.extend(patterns.PAGE_NO)
    for string in list_of_strings:
        recorder.append(string)
        recorder.append(string.lower())
        recorder.append(string.upper())
        recorder.append(string.title())

    log.debug("Possible patterns recorded for: %s are: %s" % (list_of_strings,
                                                              recorder))
    return recorder
