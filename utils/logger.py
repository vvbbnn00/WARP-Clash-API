import logging
import os
from logging.handlers import TimedRotatingFileHandler


def createLogger(filename, level=logging.INFO):
    """
    Create logger with TimedRotatingFileHandler
    :param filename: filename
    :param level: logging level
    :return: logger
    """
    # Create logs directory
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Create logger
    logger = logging.getLogger(filename)
    logger.setLevel(level)

    # Create TimedRotatingFileHandler to rotate log file
    log_filename = os.path.join("logs", filename + ".log")
    file_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7)

    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Create StreamHandler to output to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
