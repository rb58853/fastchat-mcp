import logging
import logging.handlers
from pathlib import Path
import sys


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "{color}%(levelname)s\x1b[0m: %(asctime)s  -  %(message)s"

    FORMATS = {
        logging.DEBUG: format.replace("{color}", grey),
        logging.INFO: format.replace("{color}", yellow),
        logging.WARNING: format.replace("{color}", yellow),
        logging.ERROR: format.replace("{color}", red),
        logging.CRITICAL: format.replace("{color}", bold_red),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger() -> logging.Logger:
    """Configure logging for the MCP client with log rotation."""
    logger = logging.getLogger("client-mcp")

    # Remove existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Define a consistent log directory in the user's home folder
    log_dir = Path.home() / ".local" / "share" / "mcp-llm-client"
    log_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    # Define the log file path
    log_file = log_dir / "mcp_client.log"

    # Create a rotating file handler
    # - Rotate when log reaches 5MB
    # - Keep 3 backup files
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding="utf-8",
    )

    # Add formatter to file handler
    file_handler.setFormatter(CustomFormatter())

    # Add handler to logger
    logger.addHandler(file_handler)

    # Terminal Handler  (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    # Set level
    logger.setLevel(logging.DEBUG)

    return logger


logger = setup_logger()
