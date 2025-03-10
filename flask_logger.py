import logging
import requests
from configparser import ConfigParser
import sys

class FlaskLogHandler(logging.Handler):
    """Custom logging handler to send logs to a Flask endpoint."""
    
    def __init__(self, url):
        super().__init__()
        self.url = url  # Flask logging endpoint

    def emit(self, record):
        """Send log message to the Flask logging endpoint."""
        log_entry = self.format(record)  # Format log message
        try:
            requests.post(self.url, json={"message": log_entry})
        except requests.exceptions.RequestException as e:
            print(f"Failed to send log: {e}", file=sys.stderr)  # Print error if request fails

def get_logger(name="FlaskLogger", flask_url="http://127.0.0.1:5000/set_logging", config_file='config.ini'):
    """Returns a configured logger that sends logs to a Flask server and stdout."""
    
    # Read configuration
    config = ConfigParser()
    config.read(config_file)

    # Get log level from config (default to 'INFO' if not set)
    level_str = config.get('General', 'log_level', fallback='INFO').upper()
    level = getattr(logging, level_str, logging.INFO)  # Default to INFO if invalid

    logger = logging.getLogger(name)
    logger.setLevel(level)  # Set log level from config

    # Define log format
    log_format = "%(levelname).4s | %(asctime)s | %(message)s"
    date_format = "%H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    # Prevent duplicate handlers
    if not any(isinstance(h, FlaskLogHandler) for h in logger.handlers):
        flask_handler = FlaskLogHandler(flask_url)
        flask_handler.setFormatter(formatter)
        logger.addHandler(flask_handler)
    
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
