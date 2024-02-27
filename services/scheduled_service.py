import sys
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from config import DO_GET_WARP_DATA, REOPTIMIZE_INTERVAL, GET_WARP_DATA_INTERVAL
from services.tasks import doAddDataTaskOnce, saveAccount, reoptimizeEntryPoints


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
    logger.info(f"Start scheduler.")

    if DO_GET_WARP_DATA and GET_WARP_DATA_INTERVAL > 0:
        logger.info(f"DO_GET_WARP_DATA is True, will fetch WARP data per {GET_WARP_DATA_INTERVAL} seconds.")

        # Check if the GET_WARP_DATA_INTERVAL is too small
        if GET_WARP_DATA_INTERVAL < 18:
            logger.warning("To avoid 429 error, GET_WARP_DATA_INTERVAL is recommended to be set larger than 18")

        scheduler.add_job(doAddDataTaskOnce, 'interval', seconds=GET_WARP_DATA_INTERVAL, args=[None, logger])

    if REOPTIMIZE_INTERVAL > 0:
        if sys.platform == "win32":
            # Windows does not support reoptimize
            logger.warning(f"REOPTIMIZE_INTERVAL is set to {REOPTIMIZE_INTERVAL}, but reoptimize is not supported on "
                           f"Windows.")
        else:
            logger.info(f"REOPTIMIZE_INTERVAL is set to {REOPTIMIZE_INTERVAL}, will reoptimize account per "
                        f"{REOPTIMIZE_INTERVAL} seconds.")
            scheduler.add_job(reoptimizeEntryPoints, 'interval', seconds=REOPTIMIZE_INTERVAL, args=[logger])

    logger.info(f"Start save account job, will update account info per 120 seconds.")
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
