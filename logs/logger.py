# logger.py
from datetime import datetime
import logging
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
# Get the log directory from environment variables or use a default
LOG_DIR = os.getenv('LOG_DIR', 'logs/logs_data')
os.makedirs(LOG_DIR, exist_ok=True)     # Ensure the log directory exists
# Create a log file with a timestamp for this session
SESSION_TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = os.path.join(LOG_DIR, f"{SESSION_TIMESTAMP}.log")


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler = logging.FileHandler(LOG_FILE)
        print(f"[logger.py] Logger module loaded. Timestamp = {SESSION_TIMESTAMP}")

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
