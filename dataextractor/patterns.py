# The idea is to have generic patterns for all the useful PDF file attributes
# like table of contents and etc.
#  1. List of Participating Political Parties             1-2
CONTENTS = ['CONTENTS', '^(\s+)?\d+(.|\))?\s+(\w+.*\w+)\s+((\d+\s*(-)?\s*(\d+)?))$']
PAGE_NO = ['Page\s+(\d+)']
POI = ['TABLES']
