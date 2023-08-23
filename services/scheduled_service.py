import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from services.tasks import doAddDataTaskOnce, saveAccount

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
scheduler = BackgroundScheduler()


def main():
    logger.info(f"Start scheduler")
    scheduler.add_job(doAddDataTaskOnce, 'interval', seconds=18, args=[None, logger])
    scheduler.add_job(saveAccount, 'interval', seconds=120, args=[None, logger])
    scheduler.start()

    try:
        while True:
            time.sleep(1)  # 防止主线程退出
    except (KeyboardInterrupt, SystemExit):
        # 捕获 Ctrl+C 或系统退出事件，关闭调度器
        scheduler.shutdown()


if __name__ == '__main__':
    main()
