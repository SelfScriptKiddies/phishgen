import logging
import colorama
import sys
from src.config import LOG_LEVEL, LOG_FILENAME, LOG_DATE

colorama.init()
datefmt = '%H:%M:%S'
if LOG_DATE:
    datefmt = '%d.%m.%Y : %H:%M:%S'

logging.basicConfig(level=LOG_LEVEL)

class CustomFormatter(logging.Formatter):
    prefix = "[%(levelname)s : %(name)s : %(asctime)s]"
    format = " %(message)s"

    FORMATS = {
        logging.DEBUG: colorama.Fore.CYAN + prefix + colorama.Style.RESET_ALL + format,
        logging.INFO: colorama.Fore.BLUE + prefix + colorama.Style.RESET_ALL + format,
        logging.WARNING: colorama.Fore.YELLOW + prefix + colorama.Style.RESET_ALL + format,
        logging.ERROR: colorama.Fore.RED + prefix + colorama.Style.RESET_ALL + format,
        logging.CRITICAL: colorama.Back.RED + prefix + colorama.Style.RESET_ALL + format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt)
        return formatter.format(record)


def get_logger(name: str = "root") -> logging.Logger:
    log = logging.getLogger(name)
    log.propagate = False

    stdout = logging.StreamHandler(stream=sys.stdout)
    stdout.setFormatter(CustomFormatter())
    log.addHandler(stdout)

    if LOG_FILENAME != None:
        file = logging.FileHandler(LOG_FILENAME)
        log.addHandler(file)

    return log