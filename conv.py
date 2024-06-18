import logging
from datetime import date
import configparser
import os
from test_ptt import virement 
import test_ptt
# Read configuration from .conf file
config = configparser.ConfigParser()
config.read('./conf/config.ini')


# Get log file location from the configuration
log_file = config.get('Log', 'log_file')
# Get log level from the configuration, default to INFO if not specified
log_level = config.get('Log', 'log_level', fallback='INFO')



# Get input file location from the configuration
input_file = config.get('File', 'input_file')
# Get output file location from the configuration
output_file = config.get('File', 'output_file')


# Extract directory from the log file path
log_directory = os.path.dirname(log_file)
# Extract directory from the log file path
input_directory = os.path.dirname(input_file)
# Extract directory from the log file path
output_directory = os.path.dirname(output_file)

# Check if the log directory exists, create it if not
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Check if the input directory exists, create it if not
if not os.path.exists(input_directory):
    os.makedirs(input_directory)

# Check if the output directory exists, create it if not
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Set the log level based on the configuration
numeric_log_level = getattr(logging, log_level.upper(), None)
if not isinstance(numeric_log_level, int):
    raise ValueError('Invalid log level: %s' % log_level)
# Configure logging
logging.basicConfig(filename=log_file, level=numeric_log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Log the start of execution
logging.info('Script execution started.')

# Open files
source= open(input_file, 'r', encoding="utf-8")
destination=open(output_file, 'w+')

try:
    virement_ptt=test_ptt.parse_vir_file(source)
    
    # Log success message
    logging.info('Execution completed successfully.')
    
except Exception as e:
    # Log error message
    logging.error(f'An error occurred: {str(e)}')

finally:
    # Close files
    source.close()
    destination.close()