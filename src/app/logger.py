"""
Logging Configuration for the Gateway

Initializes a centralized logger that writes security events
to a rotating file, preventing logs taking up too much disk space
"""
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    """
    Initializes and configures the 'qr_gateway' logger

    Sets up a RotatingFileHandler to manage log file size and
    applies a standardized format for all log entries

    :return: A configured logging.Logger instance
    """
    # Create or retrieve the logger by name
    logger = logging.getLogger("qr_gateway")
    logger.setLevel(logging.INFO)

    # Check if handlers already exist to prevent duplicate logs (during re-imports)
    if not logger.handlers:
        # Create a handler: max 2MB per file, keeps the last 5 old files
        handler = RotatingFileHandler(
            "security.log",
            maxBytes=2_000_000,
            backupCount=5
        )
        # Define the visual structure of each log line
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger