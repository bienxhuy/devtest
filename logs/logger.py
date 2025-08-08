# logger.py
import logging
import os
from dotenv import load_dotenv
from logs.custom_formatters.MicrosecondFormatter import MicrosecondFormatter


# Create a directory for logs if it doesn't exist
# This is used to store logs taken during a test session
load_dotenv()
BASE_LOG_DIR = os.getenv('LOG_DIR', 'logs/logs_data')
LOG_DIR = os.path.join(BASE_LOG_DIR, os.getenv('SESSION_ID', 'none_specified_session'))
os.makedirs(LOG_DIR, exist_ok=True)
# Create a unique log file name based on worker ID (xdist)
WORKER_ID = os.getenv("PYTEST_XDIST_WORKER", "main")
LOG_FILE = os.path.join(LOG_DIR, f"{WORKER_ID}.log")
# Get table name of database from environment variables
TABLE_NAME = os.getenv('TABLE_NAME', 'test_results')


# Get a logger instance, creating it if it doesn't exist
# This function caches the logger instances to
# avoid creating multiple instances with the same name
def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Check if the logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        # Follow line protocol of influxdb
        formatter = MicrosecondFormatter(
            f'{TABLE_NAME},%(message)s %(unix_micro_ts)d'
        )
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
                
    return logger


# Initilize the logger for the current module
logger = get_logger(__name__)
# Fetch relevant context for the current test run
from models.test_result.Field import Field
from models.TestContext import context as ctx


# Log the test result with line protocol format
# i.e: table,t1=v1,t2=v2 f1=v1,f2=v2 timestamp
def log_test_result(field):
    # Escape special characters in the field values
    # This is necessary to ensure that the values are correctly formatted
    def escape(s): 
        return str(s).replace(' ', r'\ ').replace(',', r'\,').replace('=', r'\=')
    
    # Quote the string values
    # Follow line protocol format of influxdb
    def quote(s):
        return f'"{s}"'

    # In case dev forget to use Field class
    if not isinstance(field, Field):
        logger.error(
            f"commit={escape(ctx.commit)},"
            f"branch={escape(ctx.branch)},"
            f"env={escape(ctx.env)},"
            f"test_suite={escape(ctx.test_suite)},"
            f"test_case={escape(ctx.test_case)} "
            f"message=Poor test result field: {quote(field)}"
        )
        return

    # Log the test result with the appropriate log level
    logger.log(level=field.log_level, msg=
        f"commit={escape(ctx.commit)},"
        f"branch={escape(ctx.branch)},"
        f"env={escape(ctx.env)},"
        f"test_suite={escape(ctx.test_suite)},"
        f"test_case={escape(ctx.test_case)} "
        f"status={quote(field.status)},"
        f"log_level={quote(field.get_log_level())},"
        f"message={quote(field.message)},"
        f"duration={field.duration},"
    )
