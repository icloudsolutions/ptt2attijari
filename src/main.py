import logging
from service import ProcessingService
import configparser
import os
import glob

def main():
    # Default configuration content
    default_config_content ="""[FILE]
input_file = virement.txt
output_file = virement.vir
[LOG]
#log_file = ./error.log
log_level = info
[CONVERSION]
target_bank_name = attijari
rib = 04012086008646649785
allowance = 1
mode_batch = true
"""
    user_dir = os.path.expanduser('~')
    virement_dir = os.path.join(user_dir, '.virement')
    print('Work Directory : ',virement_dir)

    def create_directory(directory_name):
        directory_path = os.path.join(virement_dir, directory_name)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Répertoire {directory_name} a été créer à : {directory_path}")
        else:
            print(f"Répertoire {directory_name} existant trouvé à : {directory_path}")

        return directory_path


    config_dir = create_directory('conf')
    log_dir = create_directory('logs')
    input_directory = create_directory('input')
    output_directory = create_directory('output')

    config_file_path = os.path.join(config_dir,'config.ini')

    def read_config(config_file_path, default_config_content):
        # Check if the config file exists
        if not os.path.exists(config_file_path):
            # Create a default config file if it doesn't exist
            with open(config_file_path, 'w', encoding='utf-8') as config_file:
                config_file.write(default_config_content)
                logging.info("Default config file created at {}".format(config_file_path))
        config = configparser.ConfigParser()
        config.read(config_file_path, encoding='utf-8')
        return config

    config = read_config(config_file_path, default_config_content)

    # Get output file location from the configuration
    try:
        input_file = config.get('FILE', 'input_file')
    except Exception as e:
        input_file = None  # valeur par défaut
        print(f"Input File Not Found :  {e}")
        logging.info(f"Input File Not Found : {e}")
    
    input_file_path = os.path.join(input_directory, input_file)

    try:
        output_file = config.get('FILE', 'output_file')
    except Exception as e:
        output_file = None  # valeur par défaut
        print(f"Batch Mode Activated : {e}")
        logging.info(f"Batch Mode Activated : {e}")
    
    output_file_path = os.path.join(output_directory, output_file)

    # Get the log file path, with handling for empty values
    log_file_path = config.get('LOG', 'log_file', fallback=os.path.join(log_dir, 'virement.log'))
    log_level = config.get('LOG', 'log_level', fallback='INFO').upper()
    # Set the log level based on the configuration
    numeric_log_level = getattr(logging, log_level, None)
    if not isinstance(numeric_log_level, int):
        raise ValueError('Invalid log level: %s' % log_level)

    # Configure logging
    logging.basicConfig(filename=log_file_path, level=numeric_log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Configuration file : '+ config_file_path)
    print('Configuration file : '+ config_file_path)
    logging.info('log_file_path : '+log_file_path)
    print('log_file_path : '+log_file_path)
    logging.info('log_level  : '+log_level)
    print('log_level  : '+log_level)

    #---------------------- MODE BATCH ----------------------------------------------
    try:
        # Retrieve 'mode_batch' value from the 'CONVERSION' section in the config
        mode_batch = config.get('CONVERSION', 'mode_batch')
        # Convert the string to a boolean value
        mode_batch = {"true": True, "false": False}.get(mode_batch.lower(), False)
        # Print and log the batch mode status
        print(f"Batch Mode {'Activated' if mode_batch else 'Disactivated'}")
        logging.info(f"Batch Mode {'Activated' if mode_batch else 'Disactivated'}")
    except Exception as e:
        # In case of an error, set default value to False and log the error
        mode_batch = False  # default value
        print(f"Batch Mode Disactivated : {e}")
        logging.error(f"Batch Mode Disactivated : {e}")


    
    try:
        target_bank_name = config.get('CONVERSION', 'target_bank_name').upper()
    except Exception as e:
        target_bank_name = None  # valeur par défaut
        print(f"Targed Bank Conversion not specified : {e}")
        logging.info(f"Targed Bank Conversion not specified: {e}")
        
    try:
        allowance = int(config.get('CONVERSION', 'allowance'))
    except Exception as e:
        allowance = 0  # valeur par défaut
        print(f"Allowance not specified : {e}")
        logging.info(f"Allowance not specified : {e}")
    
    try:
        rib = config.get('CONVERSION', 'rib')
    except Exception as e:
        rib = None  # valeur par défaut
        print(f"RIB not specified : {e}")
        logging.info(f"RIB not specified : {e}")

    """# Read configuration from .conf file ---------------------------------------------
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

    try:
        mode_batch = config.get('conversion', 'mode_batch')
        mode_batch = {"true": True, "false": False}.get(mode_batch.lower(), False)
        print(f"Batch Mode {'Activated' if mode_batch else 'Disactivated'}")
    except Exception as e:
        mode_batch = False  # valeur par défaut
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
"""
    # Main program  ------------------------------------------------------------------
    if mode_batch or output_file is None:
        input_files = glob.glob(os.path.join(input_directory, '*'))
        print(f"List of processing files: {input_files}")
        for input_file in input_files:
            try:
                ProcessingService.processing_vir_batch(input_file, output_directory, target_bank_name,rib,log_level,allowance)
            except Exception as e:
                print(f"An error occurred while batch processing {input_file}: {e}")
                logging.error(f"An error occurred while batch processing {input_file}: {e}")
    else:
            
            try:
                ProcessingService.processing_vir_file(input_file_path, target_bank_name,rib, output_file_path,log_level,allowance)
            except Exception as e:
                logging.error(f"An error occurred while file processing {input_file_path}: {e}")
    # Main program  -----------------------------------------------------------------

if __name__ == '__main__':
    main()
