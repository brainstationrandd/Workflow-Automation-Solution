import logging
import sys
import os

# Get Logger
logger = logging.getLogger(__name__)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create handler
stream_handler = logging.StreamHandler(sys.stdout)

# Check if logs directory exists, if not, create it
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = logging.FileHandler('logs/app.log')

# set formatter
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.handlers = [stream_handler, file_handler]

# Set log level
logger.setLevel(logging.INFO)