import logging

FORMAT = "%(asctime)s.%(msecs)d %(levelname)s %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT)

level = logging.DEBUG

handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(level)

logger = logging.getLogger(__name__)
logger.handlers = []
logger.addHandler(handler)
logger.setLevel(level)
