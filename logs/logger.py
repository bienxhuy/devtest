# logger.py
import logging
from logging.handlers import SocketHandler


# Get a logger instance, creating it if it doesn't exist
# This function caches the logger instances to
# avoid creating multiple instances with the same name
def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Check if the logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        # Add socket handler for logging to a remote server
        socket_handler = SocketHandler("localhost", 9020)
        logger.addHandler(socket_handler)
        logger.propagate = False

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
        f"duration={field.duration}"
    )
