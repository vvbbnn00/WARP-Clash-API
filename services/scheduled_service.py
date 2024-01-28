import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from config import DO_GET_WARP_DATA
from services.tasks import doAddDataTaskOnce, saveAccount


def main(logger=None):
    """
    Start scheduler
    :param logger:
    :return:
    """
    if logger is None:
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger()
    scheduler = BackgroundScheduler()
    logger.info(f"Start scheduler")
    if DO_GET_WARP_DATA:
        scheduler.add_job(doAddDataTaskOnce, 'interval', seconds=18, args=[None, logger])
    scheduler.add_job(saveAccount, 'interval', seconds=120, args=[None, logger])
    scheduler.start()

    try:
        while True:
            time.sleep(1)  # Prevent main thread from exiting
    except (KeyboardInterrupt, SystemExit):
        # Catch Ctrl+C or system exit event, close scheduler
        scheduler.shutdown()


if __name__ == '__main__':
    main()
