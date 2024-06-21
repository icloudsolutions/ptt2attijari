import logging
from service import VirementService, ValidationService, BankService
import configparser
import os
import pprint

def main():

    # Read configuration from .conf file
    config = configparser.ConfigParser()
    config.read('./conf/config.conf')

    # Get log file location from the configuration
    log_file = config.get('Log', 'log_file')
    # Get log level from the configuration, default to INFO if not specified
    log_level = config.get('Log', 'log_level', fallback='INFO')

    # Get input file location from the configuration
    input_file = config.get('File', 'input_file')
    # Get output file location from the configuration
    output_file = config.get('File', 'output_file')
    target_bank_name = config.get('convert_to', 'target_bank_name').upper()
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
    
    def print_readable(virement):
        print("Header:")
        pprint.pprint(virement.header)
        
        print("\nBody:")
        for i, record in enumerate(virement.body):
            print(f"Virement {i + 1}:")
            pprint.pprint(record)
            print()  # Add an empty line between records
    #-------
        
    try:
        # Get virement from file
        virement_in = VirementService.get_virement(input_file)

        # Determine bank_name from header.code_remettant
        code_bank = virement_in.header.code_remettant
        bank_in = BankService.get_bank_by_code(code_bank)
        bank_out = BankService.get_bank_by_name(target_bank_name)
        if not bank_in:
            raise ValueError(f"Bank code '{code_bank}' from header not found in bank data")

        #bank_name_in = bank_in['name']
        logging.info(f"Bank name determined from header : {bank_in['name']}")
        
        # Validate virement in relation to the determined bank
        ValidationService.validate_virement(virement_in, bank_in)

        virement_out = VirementService.convert_virement(virement_in,bank_in,bank_out)

        # Save virement to an output file after validation
        VirementService.save_virement(virement_out, output_file)

        virement = VirementService.get_virement(output_file)
        ValidationService.validate_virement(virement, bank_out)

        print_readable(virement)

        logging.info(f"Virement validation and save completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {e}")




if __name__ == '__main__':
    main()