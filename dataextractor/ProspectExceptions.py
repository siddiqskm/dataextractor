class ProspectExceptions(Exception):
    def __init__(self, message):
        self.message = message


class PageNotFoundException(ProspectExceptions):
    def __init__(self, message="Cannot read page content"):
        self.message = message


class CannotFetchTablesException(ProspectExceptions):
    def __init__(self, message="Cannot read page tables"):
        self.message = message
