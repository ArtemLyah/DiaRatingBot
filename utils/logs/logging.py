import logging

FORMAT = "[%(levelname)s] %(name)s | %(asctime)s\nmsg: %(message)s"

logger = logging.getLogger("Diarating")
logger.setLevel(logging.DEBUG)

fileHandler = logging.StreamHandler()
form = logging.Formatter(FORMAT)
fileHandler.setFormatter(form)
logger.addHandler(fileHandler)
