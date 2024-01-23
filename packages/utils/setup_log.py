import logging
import os
from datetime import datetime

def setup_logging(log_name):
    # Create the directory structure for logs
    log_dir = os.path.join("log", datetime.now().strftime("%Y-%m-%d"))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Log file path
    log_file_path = os.path.join(log_dir, "app.log")

    # Create a custom logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)  # Set log level

    # Create file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)

    # Create formatter and add it to the file handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add file handler to the logger
    logger.addHandler(file_handler)

    return logger