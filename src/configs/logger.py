import logging

fmt = {
    'time': '%(asctime)s',
    'name': '%(name)s',
    'level': '%(levelname)s',
    'message': '%(message)s'
}

logging.basicConfig(
    filename=".\\temp\\logs.txt",
    filemode="w",
    level=logging.INFO,
    format=str(fmt)
)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
