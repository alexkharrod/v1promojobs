import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def log_error(message, exception=None):
    """
    Logs an error message with optional exception information.
    """
    if exception:
        logger.error(message, exc_info=True)
    else:
        logger.error(message)

def log_info(message):
    """
    Logs an info message.
    """
    logger.info(message)

def log_warning(message):
    """
    Logs a warning message.
    """
    logger.warning(message)
