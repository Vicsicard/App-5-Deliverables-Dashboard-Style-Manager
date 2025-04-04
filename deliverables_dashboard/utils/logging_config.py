"""
Logging configuration for the deliverables dashboard.
"""
import logging
import os
from datetime import datetime

def setup_logger():
    """Configure logging for the application."""
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Set up file handler
    log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatters and add it to the handlers
    file_format = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    console_format = logging.Formatter('[%(levelname)s] %(message)s')
    file_handler.setFormatter(file_format)
    console_handler.setFormatter(console_format)
    
    # Get the root logger and add handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger
