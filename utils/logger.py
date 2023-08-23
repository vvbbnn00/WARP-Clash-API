import logging
import os
from logging.handlers import TimedRotatingFileHandler


def create_logger(filename, level=logging.INFO):
    # 创建日志目录
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # 创建日志记录器
    logger = logging.getLogger(filename)
    logger.setLevel(level)

    # 创建 TimedRotatingFileHandler，每天自动切分日志文件
    log_filename = os.path.join("logs", filename + ".log")
    file_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7)

    # 设置日志格式
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # 创建 StreamHandler，用于将日志输出到控制台
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # 将处理器添加到记录器
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
