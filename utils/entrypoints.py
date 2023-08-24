import csv

from models import Entrypoint
from config import *

ENTRYPOINTS = []
FILE_PATH = './config/result.csv'


def read_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row


def reload_entrypoints():
    global ENTRYPOINTS
    ENTRYPOINTS = []
    for row in read_csv(FILE_PATH):
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


def get_entrypoints():
    if not ENTRYPOINTS:
        reload_entrypoints()
    return ENTRYPOINTS


def get_best_entrypoints(num=1):
    """
    Get best entrypoints
    :param num:
    :return:
    """
    if not ENTRYPOINTS:
        reload_entrypoints()

    # sort by loss and delay
    returnEntryPoints = sorted(ENTRYPOINTS, key=lambda x: (x.loss, x.delay))[:num]
    return returnEntryPoints


if __name__ == '__main__':
    reload_entrypoints()
    print(ENTRYPOINTS)
    print(len(ENTRYPOINTS))
