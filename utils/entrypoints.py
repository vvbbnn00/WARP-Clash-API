import csv

from models import Entrypoint
from config import *
from flask import current_app

ENTRYPOINTS = []
ENTRYPOINT_SCRIPT_PATH = './scripts/get_entrypoints.sh'
RESULT_LAST_MODIFIED = 0
RESULT_PATH = './config/result.csv'


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


def reloadEntrypoints():
    """
    Reload entrypoints from csv file
    :return: list of entrypoints
    """
    current_app.logger.info(f"Reload entrypoints from {RESULT_PATH}")
    global ENTRYPOINTS, RESULT_LAST_MODIFIED
    RESULT_LAST_MODIFIED = os.path.getmtime(RESULT_PATH)
    ENTRYPOINTS = []
    for row in readCsv(RESULT_PATH):
        try:
            if row[0].lower() == 'ip:port':
                continue
            ip, port = row[0].split(':')
            loss = float(row[1].replace('%', ''))
            delay = int(row[2].replace('ms', ''))

            if loss > LOSS_THRESHOLD or delay > DELAY_THRESHOLD:
                continue

            entrypoint = Entrypoint()
            entrypoint.ip = ip
            entrypoint.port = port
            entrypoint.loss = loss
            entrypoint.delay = delay

            ENTRYPOINTS.append(entrypoint)
        except Exception as e:
            current_app.logger.error(f"Error when reading row: {row}, error: {e}")

    return ENTRYPOINTS


def getEntrypoints():
    """
    Get entrypoints
    :return: list of entrypoints
    """
    if not ENTRYPOINTS:
        reloadEntrypoints()

    # Check if file has been modified
    if RESULT_LAST_MODIFIED != os.path.getmtime(RESULT_PATH):
        current_app.logger.info(f"File {RESULT_PATH} has been modified, will reload entrypoints.")
        reloadEntrypoints()

    return ENTRYPOINTS


def getBestEntrypoints(num=1):
    """
    Get best entrypoints
    :param num: number of entrypoints
    :return: list of entrypoints
    """
    # sort by loss and delay
    returnEntryPoints = sorted(getEntrypoints(), key=lambda x: (x.loss, x.delay))[:num]
    return returnEntryPoints


def optimizeEntrypoints():
    """
    Optimize entrypoints
    :return:
    """
    # Check current path
    if not os.path.exists(ENTRYPOINT_SCRIPT_PATH):
        current_app.logger.error(f"File {ENTRYPOINT_SCRIPT_PATH} does not exist.")
        return

    # Fix ./scripts/get_entrypoint.sh if it has CRLF
    file = open(ENTRYPOINT_SCRIPT_PATH, 'r')
    data = file.read().replace('\r\n', '\n')
    file.close()
    file = open(ENTRYPOINT_SCRIPT_PATH, 'w')
    file.write(data)
    file.close()

    # Run ./scripts/get_entrypoint.sh
    os.system("bash ./scripts/get_entrypoints.sh")

# if __name__ == '__main__':
#     reloadEntrypoints()
#     print(ENTRYPOINTS)
#     print(len(ENTRYPOINTS))
