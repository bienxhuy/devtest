# logger.py
import logging, os
from dotenv import load_dotenv


# Create a directory for logs if it doesn't exist
# This is used to store logs taken during a test session
load_dotenv()

BASE_LOG_DIR = os.getenv('LOG_DIR', 'logs/logs_data')
LOG_DIR = os.path.join(BASE_LOG_DIR, os.getenv('SESSION_ID', 'none_specified_session'))
os.makedirs(LOG_DIR, exist_ok=True)

# Create a unique log file name based on worker ID (xdist)
WORKER_ID = os.getenv("PYTEST_XDIST_WORKER", "main")
LOG_FILE = os.path.join(LOG_DIR, f"{WORKER_ID}.log")


# Get a logger instance, creating it if it doesn't exist
# This function caches the logger instances to
# avoid creating multiple instances with the same name
def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Check if the logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        # Add file handler and formatter
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
