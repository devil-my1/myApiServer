import logging

logger = logging.getLogger("__name__")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename="logger.log")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    datefmt="%Y-%m-%d %H:%M:%S",
    fmt="%(asctime)s %(levelname)s %(module)s %(funcName)s: %(message)s",
)
fh.setFormatter(formatter)

logger.addHandler(fh)
