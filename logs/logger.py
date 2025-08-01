# logger.py
from datetime import datetime
import logging
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
# Get the log directory from environment variables or use a default
# TODO: Create sub folder for logs of each test session
LOG_DIR = os.getenv('LOG_DIR', 'logs/logs_data')
os.makedirs(LOG_DIR, exist_ok=True)
# Create a unique log file name based on the current timestamp and worker ID (xdist)
WORKER_ID = os.getenv("PYTEST_XDIST_WORKER", "main")
SESSION_TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = os.path.join(LOG_DIR, f"{SESSION_TIMESTAMP}_{WORKER_ID}.log")


# Get a logger instance, creating it if it doesn't exist
# This function caches the logger instances to
# avoid creating multiple instances with the same name
def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Check if the logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
                
    return logger
