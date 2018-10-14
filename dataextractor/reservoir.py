# System Imports
import re

# Local Imports
from logger import get_logger
import patterns
import utils

# Global Variables
log = get_logger(__name__)


def prune_data(data, ignore_patterns):
    """Prunes the data so that the complete data is cleaned of all the
    unwanted and other patterns"""
    log.debug("Starting to prune the data: %s ..." % data)
    pruned_data = []
    ignore_patterns = utils.generate_possible_patterns(ignore_patterns)
    patterns = utils.construct_pattern_from_list(ignore_patterns)
    for line in data:
        if line.strip():
            matches = re.search(patterns, line)
            if matches:
                log.debug("Ignoring line: %s due to ignore patterns"
                          % line)
            else:
                pruned_data.append(line.strip())

    log.debug("Returing the pruned data: %s" % pruned_data)
    return pruned_data


class Excavator():
    """
    A class to excavate the input data and return the POI(Point of interest)
    as requested
    """
    def __init__(cls, data, poi=None, ignore_patterns=None):
        if poi is None:
            cls.poi = patterns.POI
        cls.data = prune_data(data, ignore_patterns)

    def __create_poi_string(cls, string):
        """Fetch the POI string"""
        for poi in cls.poi:
            if poi == 'TABLES':
                log.debug("POI: %s" % cls.poi)
                # We are interested in columns hence split the pattern with
                # \s+
                splits = ['(' + x + ')' for x in string.split('\s+')]
                return '^' + '\s+'.join(splits) + '$'

    def __generate_pattern_from_line(cls, line):
        """Generates a pattern from the input string"""
        string_list = list(line)
        log.debug("Generating pattern for: %s, length: %s" % (line,
                  len(string_list)))
        for i, char in enumerate(string_list):
            if re.match('\s', char):
                string_list[i] = 's'
            elif re.match('\d', char):
                string_list[i] = 'd'
            elif re.match('[a-zA-Z]', char):
                string_list[i] = 'w'
            else:
                string_list[i] = 'W'

        log.debug("Intermediate pattern: %s" % string_list)
        regex = []
        flag = False
        addRegex = False
        for index in range(0, len(string_list)):
            start_char = string_list[index]
            if index == (len(string_list) - 1):
                addRegex = True
            elif start_char == string_list[index + 1]:
                flag = True
                addRegex = False
            else:
                addRegex = True

            if addRegex:
                if flag:
                    regex.append('\\' + start_char + '+')
                else:
                    regex.append('\\' + start_char)
                flag = False

        regex_str = cls.__create_poi_string(''.join(regex))
        log.debug("Regex for: %s is: %s" % (line, regex_str))
        return regex_str

    def __excavate_tables(cls):
        """Excavates tables from the data"""
        pattern_gen = None
        add_table_flag = False
        table_title = None
        master_table = []
        cache = []
        table = []
        for line_no, line in enumerate(cls.data):
            if pattern_gen is None:
                pattern_gen = cls.__generate_pattern_from_line(line)
                log.debug("Title is: %s" % line)
                table_title = line
            else:
                line_pattern = cls.__generate_pattern_from_line(line)
                pattern_gen_col_count = len(pattern_gen.split('\s+'))
                line_pattern_col_count = len(line_pattern.split('\s+'))
                if (pattern_gen_col_count == line_pattern_col_count):
                    log.debug("Adding line: %s to %s" % (line, table))
                    matches = re.search(line_pattern, line)
                    table.append(tuple(matches.groups()))
                    add_table_flag = False
                else:
                    log.debug("Adding line to cache due to mismatch: %s"
                              % line)
                    cache.append(line)
                    add_table_flag = True

                if (add_table_flag or line_no == len(cls.data) - 1) and table:
                    log.debug("Adding table: %s to master table: %s" % (table,
                              master_table))
                    if cache:
                        # Let's assume cache contains last parsed sub-heading
                        header = cache.pop(0)
                        temp_table_dict = {header: table}
                        log.debug("Adding: %s to master_table"
                                  % temp_table_dict)
                        master_table.append(temp_table_dict)
                    else:
                        # Nothing available in cache, Proceed with adding table
                        # entries directly
                        master_table.append(table)
                    table = []
                    add_table_flag = False

        log.info("Returning: %s as the master table" % master_table)
        return {table_title: master_table}

    def excavate_data(cls):
        """Main function to excavate data and return tables"""
        refined_data = {}
        refined_data.update({'tables': cls.__excavate_tables()})
        return refined_data
