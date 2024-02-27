"""

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.

"""
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
