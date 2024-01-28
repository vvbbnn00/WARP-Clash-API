import csv

from models import Entrypoint
from config import *

ENTRYPOINTS = []
FILE_PATH = './config/result.csv'


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
    global ENTRYPOINTS
    ENTRYPOINTS = []
    for row in readCsv(FILE_PATH):
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

    return ENTRYPOINTS


def getEntrypoints():
    """
    Get entrypoints
    :return: list of entrypoints
    """
    if not ENTRYPOINTS:
        reloadEntrypoints()
    return ENTRYPOINTS


def getBestEntrypoints(num=1):
    """
    Get best entrypoints
    :param num: number of entrypoints
    :return: list of entrypoints
    """
    if not ENTRYPOINTS:
        reloadEntrypoints()

    # sort by loss and delay
    returnEntryPoints = sorted(ENTRYPOINTS, key=lambda x: (x.loss, x.delay))[:num]
    return returnEntryPoints


# if __name__ == '__main__':
#     reloadEntrypoints()
#     print(ENTRYPOINTS)
#     print(len(ENTRYPOINTS))
