import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_folders():
    """Create input and output folders if they don't exist."""
    folders = ['input', 'output']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            logger.info(f"Created {folder} directory")