
import logging


def create_logger_by_filename(name):
    """Return a logger for with passed name."""

    # create log
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create handler for terminal
    terminalHandler = logging.StreamHandler()

    # set level messages for handler
    terminalHandler.setLevel(logging.DEBUG)

    # create formatter for handler
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter for handler
    terminalHandler.setFormatter(fmt)

    # add handler to logger
    logger.addHandler(terminalHandler)

    return logger
