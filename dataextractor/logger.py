# System Imports
import logging

# Global Parameters
LOGS_DIR = 'logs'


def get_logger(logger_name):

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s.%(funcName)s: %(message)s')

    file_handler = logging.FileHandler(LOGS_DIR+'/app_debug.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    info_handler = logging.FileHandler(LOGS_DIR+'/app_info.log')
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    error_handler = logging.FileHandler(LOGS_DIR+'/app_error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    return logger
