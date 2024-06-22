import logging
from service import ProcessingService
import configparser
import os
import pprint
import glob

def main():
    # Read configuration from .conf file ---------------------------------------------
    config = configparser.ConfigParser()
    config.read('./conf/config.conf')
    input_file = config.get('File', 'input_file')
    input_directory = os.path.dirname(input_file)
    # Check if the input directory exists, create it if not
    if not os.path.exists(input_directory):
        os.makedirs(input_directory)
    output_directory = os.path.dirname('./output/')
    # Check if the output directory exists, create it if not
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    # Get output file location from the configuration
    try:
        output_file = config.get('File', 'output_file')
    except Exception as e:
        output_file = None  # valeur par défaut
        print(f"Batch Mode Activated : {e}")
    try:
        mode_batch = config.get('conversion', 'mode_batch').upper
    except Exception as e:
        mode_batch = None  # valeur par défaut
        print(f"Batch Mode Disactivated : {e}")
    target_bank_name = config.get('conversion', 'target_bank_name').upper()
    # Read configuration from .conf file ---------------------------------------------

    # Config Log ---------------------------------------------------------------------
    # Get log file location from the configuration
    log_file = config.get('Log', 'log_file')
    # Get log level from the configuration, default to INFO if not specified
    log_level = config.get('Log', 'log_level', fallback='INFO')
    # Extract directory from the log file path
    log_directory = os.path.dirname(log_file)
    # Extract directory from the log file path
    # Check if the log directory exists, create it if not#
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    # Set the log level based on the configuration
    numeric_log_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_log_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    # Configure logging
    logging.basicConfig(filename=log_file, level=numeric_log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    # Config Log ---------------------------------------------------------------------

    # Print virement ------------------------------------------------------------------
    def print_readable(virement):
        print("Header:")
        pprint.pprint(virement.header)
        
        print("\nBody:")
        for i, record in enumerate(virement.body):
            print(f"Virement {i + 1}:")
            pprint.pprint(record)
            print()  # Add an empty line between records
    # Print virement -----------------------------------------------------------------

    # Main program  ------------------------------------------------------------------

    if mode_batch is None or output_file is None:
        input_files = glob.glob(os.path.join(input_directory, '*'))
        print(f"List of processing files: {input_files}")
        for input_file in input_files:
            try:
                ProcessingService.processing_vir_batch(input_file, output_directory, target_bank_name)
            except Exception as e:
                logging.error(f"An error occurred while batch processing {input_file}: {e}")
    else:
            try:
                ProcessingService.processing_vir_file(input_file, target_bank_name, output_file)
            except Exception as e:
                logging.error(f"An error occurred while file processing {input_file}: {e}")
    # Main program  -----------------------------------------------------------------

if __name__ == '__main__':
    main()
