import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "POM_log.log")

def get_logger(name = __name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # Create log directory if it doesn't exist
        os.makedirs(LOG_DIR, exist_ok = True)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
