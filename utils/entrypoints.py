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
import copy
import csv
import logging
import os

from flask import current_app

from config import DELAY_THRESHOLD, LOSS_THRESHOLD
from models import Entrypoint

ENTRYPOINT_SCRIPT_PATH = './scripts/get_entrypoints.sh'

RESULT_PATH = './config/result.csv'
RESULT_LAST_MODIFIED = 0

RESULT_PATH_V6 = './config/result_v6.csv'
RESULT_LAST_MODIFIED_V6 = 0

ENTRYPOINTS = []
ENTRYPOINTS_V6 = []


def _getLogger():
    """
    Get logger
    :return: logger
    """
    try:
        if hasattr(current_app, 'logger'):
            return current_app.logger
        else:
            return logging.getLogger(__name__)
    except RuntimeError:
        return logging.getLogger(__name__)


def readCsv(file_path):
    """
    Read csv file
    :param file_path: file path
    :return: generator
    """
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row


def reloadEntrypoints(ipv6=False):
    """
    Reload entrypoints from csv file

    :param ipv6: if load ipv6 entrypoints
    :return: list of entrypoints
    """
    global ENTRYPOINTS, ENTRYPOINTS_V6, RESULT_LAST_MODIFIED, RESULT_LAST_MODIFIED_V6

    # Get logger
    logger = _getLogger()

    result_file = RESULT_PATH_V6 if ipv6 else RESULT_PATH
    logger.info(f"Reload entrypoints from {result_file}")

    if ipv6:
        RESULT_LAST_MODIFIED_V6 = os.path.getmtime(result_file)
        ENTRYPOINTS_V6 = []
    else:
        RESULT_LAST_MODIFIED = os.path.getmtime(result_file)
        ENTRYPOINTS = []

    entrypoints = copy.copy(ENTRYPOINTS_V6 if ipv6 else ENTRYPOINTS)

    for row in readCsv(result_file):
        try:
            if row[0].lower() == 'ip:port':
                continue
            ip, port = row[0].split(':') if not ipv6 else (row[0].split("]:"))
            ip = ip.replace('[', '') if ipv6 else ip
            loss = float(row[1].replace('%', ''))
            delay = int(row[2].replace('ms', ''))

            if loss > LOSS_THRESHOLD or delay > DELAY_THRESHOLD:
                continue

            entrypoint = Entrypoint()
            entrypoint.ip = ip
            entrypoint.port = int(port)
            entrypoint.loss = loss
            entrypoint.delay = delay

            entrypoints.append(entrypoint)
        except Exception as e:
            logger.error(f"Error when reading row: {row}, error: {e}")

    return entrypoints


def getEntrypoints(ipv6=False):
    """
    Get entrypoints

    :param ipv6: if get ipv6 entrypoints
    :return: list of entrypoints
    """
    entrypoints = copy.copy(ENTRYPOINTS_V6 if ipv6 else ENTRYPOINTS)

    # Get logger
    logger = _getLogger()

    if not entrypoints or len(entrypoints) == 0:
        return reloadEntrypoints(ipv6)

    last_modified = RESULT_LAST_MODIFIED_V6 if ipv6 else RESULT_LAST_MODIFIED
    result_file = RESULT_PATH_V6 if ipv6 else RESULT_PATH

    # Check if file has been modified
    if last_modified != os.path.getmtime(result_file):
        logger.info(f"File {last_modified} has been modified, will reload entrypoints.")
        return reloadEntrypoints(ipv6)

    return entrypoints


def getBestEntrypoints(num=1, ipv6=False):
    """
    Get best entrypoints
    :param num: number of entrypoints
    :param ipv6: if get ipv6 entrypoints
    :return: list of entrypoints
    """
    # sort by loss and delay
    returnEntryPoints = sorted(getEntrypoints(ipv6), key=lambda x: (x.loss, x.delay))[:num]
    return returnEntryPoints


def optimizeEntrypoints():
    """
    Optimize entrypoints
    :return:
    """
    # Get logger
    logger = _getLogger()

    # Check current path
    if not os.path.exists(ENTRYPOINT_SCRIPT_PATH):
        logger.error(f"File {ENTRYPOINT_SCRIPT_PATH} does not exist.")
        return

    # Fix ./scripts/get_entrypoint.sh if it has CRLF
    file = open(ENTRYPOINT_SCRIPT_PATH, 'r')
    data = file.read().replace('\r\n', '\n')
    file.close()
    file = open(ENTRYPOINT_SCRIPT_PATH, 'w')
    file.write(data)
    file.close()

    # Get ipv4 entrypoints
    print("Getting IPv4 entrypoints")
    os.system(f"bash {ENTRYPOINT_SCRIPT_PATH} -4")

    # Get ipv6 entrypoints
    print("Getting IPv6 entrypoints")
    os.system(f"bash {ENTRYPOINT_SCRIPT_PATH} -6")

# if __name__ == '__main__':
#     reloadEntrypoints()
#     print(ENTRYPOINTS)
#     print(len(ENTRYPOINTS))
