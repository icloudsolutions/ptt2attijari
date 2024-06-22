import logging
from datetime import datetime
from dao import VirementDAO, HeaderDAO, BodyDAO, BodyLineDAO, BankDAO
from tnrib import TNRIB
import os

class VirementService:

    @staticmethod
    def get_virement(file_path):
        return VirementDAO.get_vir_file(file_path)

    @staticmethod
    def save_virement(virement, output_path):
        VirementDAO.write_vir_file(virement, output_path)

    @staticmethod
    def add_body_line_to_virement(virement, body_line):
        VirementDAO.add_body_line(virement, body_line)

    @staticmethod
    def update_body_line_in_virement(virement, index, body_line):
        VirementDAO.update_body_line(virement, index, body_line)

    @staticmethod
    def delete_body_line_from_virement(virement, index):
        VirementDAO.delete_body_line(virement, index)

    @staticmethod
    def convert_virement(virement, old_bank, new_bank):
        updated_virement = VirementDAO.convert(virement, new_bank)
        print(f"Convertion sucess from {old_bank['name']} to {new_bank['name']} structure.")
        return updated_virement

class ValidationService:
    @staticmethod
    def validate_virement(virement, bank,filename):
        try:
            ValidationService._validate_header(virement.header, bank)
            for body_line in virement.body:
                ValidationService._validate_bodyline(body_line, bank)
            montant_total = int(virement.header.montant_total)
            montant_virements = sum(int(line.montant_virement) for line in virement.body)
            nbr_virement = int(virement.header.nbr_virement)
            count_virement = len(virement.body)
            valid_montant = montant_total == montant_virements
            valid_count = nbr_virement == count_virement
            print(f"\nValidation Test Results of file {filename} :")
            print(f"Le Montant total du bordereau {montant_total/1000} {' est égal ' if valid_montant else 'n est pas égal'} à la somme des montants des virements soit {montant_virements/1000} dinars : Test {'Valid' if valid_montant else 'Invalid'}")
            print(f"Le nombre total de virements est égal au nombre de lignes dans le corps du fichier soit {nbr_virement} virements : Test {'Valid' if valid_count else 'Invalid'}")
            logging.info(f"Validation montant total du bordereau soit {montant_virements/1000} dinars : {'Valid' if valid_montant else 'Invalid'}")
            logging.info(f"Validation nombre de virements {nbr_virement}: {'Valid' if valid_count else 'Invalid'}")

        except AssertionError as e:
            logging.error(f"Validation failed of {filename} : {e}")
            raise

    @staticmethod
    def _validate_header(header, bank):
        try:
            assert header.sens == "1", f"sens invalid: {header.sens}. Sens value must be 1"
            assert header.code_valeur == "10", f"Code valeur invalid: {header.code_valeur} code valeur must be 10 "
            assert header.nature_remettant == "1", f"Nature remettant invalid: {header.nature_remettant}"
            assert header.code_remettant == bank['code'], f"Code remettant (code banque) invalid: {header.code_remettant}. It must be {bank['code']} for {bank['name']}"
            assert header.ccrr == bank['ccrr'], f"Code du centre régional remettant invalid: '{header.ccrr}'. It must be '{bank['ccrr']}'"
            assert header.date_operation == datetime.today().strftime("%Y%m%d"), f"Date opération invalid: {header.date_operation}. It must be today's date {datetime.today().strftime('%Y%m%d')}"
            # Check if bank.num_lot is defined before comparing
            if 'num_lot' in bank and bank['num_lot']:
                assert header.num_lot == bank['num_lot'], f"Numéro de lot invalid: {header.num_lot}. It must be {bank['num_lot']}"
            assert header.code_enregistrement == "11", f"Code enregistrement invalid: {header.code_enregistrement}. It must be 11"
            assert header.code_devise == "788", f"Code devise invalid: {header.code_devise}. It must be 788 for dinars"
            assert header.rang == "00", f"Rang invalid: {header.rang}. It must be '00'"

        except AssertionError as e:
            logging.error(f"Validation failed in Header: {e}")
            raise

    @staticmethod
    def _validate_bodyline(body_line, bank):
        try:
            assert body_line.sens == "1", f"Sens invalid: {body_line.sens}. Sens value must be 1"
            assert body_line.code_valeur == "10", f"Code valeur invalid: {body_line.code_valeur}. Code valeur must be 10"
            assert body_line.nature_remettant == "1", f"Nature remettant invalid: {body_line.nature_remettant}"
            assert body_line.ccrr == bank['ccrr'], f"Code du centre régional remettant invalid: '{body_line.ccrr}'. It must be '{bank['ccrr']}'"
            assert body_line.date_operation == datetime.today().strftime("%Y%m%d"), f"Date opération invalid: {body_line.date_operation}. It must be today's date {datetime.today().strftime('%Y%m%d')}"
            if 'num_lot' in bank and bank['num_lot']:
                assert body_line.num_lot ==  bank['num_lot'], f"Numéro de lot invalid: {body_line.num_lot}. It must be {bank['num_lot']}"
            assert body_line.code_devise == "788", f"Code devise invalid: {body_line.code_devise}. It must be 788 for dinars"
            assert body_line.rang == "00", f"Rang invalid: {body_line.rang}. It must be '00'"
            assert body_line.code_enregistrement == "21", f"Code enregistrement invalid: {body_line.code_enregistrement}. It must be 21"
            assert body_line.code_enregistrement_complementaire == "0", f"Code enregistrement complémentaire invalid: {body_line.code_enregistrement_complementaire}. It must be 0"
            assert body_line.nbr_enregistrement == "00", f"Nombre enregistrement invalid: {body_line.nbr_enregistrement}. It must be 00"
            assert body_line.date_compensation == datetime.today().strftime("%Y%m%d"), f"Date de compensation invalid: {body_line.date_compensation}. It must be today's date {datetime.today().strftime('%Y%m%d')}"
            assert body_line.situation_donneur == "0", f"Situation du donneur d’ordres invalid: {body_line.situation_donneur}. It must be 1 (Résident)"
            assert body_line.type_compte_donneur == "1", f"Type du compte du donneur d’ordres invalid: {body_line.type_compte_donneur}. It must be 1 (Compte en dinars)"
            assert body_line.nature_compte_donneur == "0", f"Nature du compte du donneur d’ordres invalid: {body_line.nature_compte_donneur}. It must be '0' (pas d'exigence d’un dossier de change et de commerce extérieur)"
            assert TNRIB(body_line.rib_emetteur).valid , f"Le RIB de l'émetteur invalid: {body_line.rib_emetteur}."
            assert TNRIB(body_line.rib_beneficiaire).valid , f"Le RIB du bénéficiaire invalid: {body_line.rib_beneficiaire}."

        except AssertionError as e:
            logging.error(f"Validation failed in BodyLine: {e}")
            print(f"Validation failed in BodyLine ref: {body_line.ref_dossier}: {e}")
            raise

class ProcessingService:
            def processing_vir_batch(input_file,output_directory,target_bank_name):
                # Log the start of execution
                logging.info('Processing vir Batch started.')
                filename_without_extension = os.path.splitext(os.path.basename(input_file))[0]
                output_file = os.path.join(output_directory, f"{filename_without_extension}.vir")
                # Get virement from file
                virement_in = VirementService.get_virement(input_file)
                # Determine bank_name from header.code_remettant
                code_bank = virement_in.header.code_remettant
                bank_in = BankService.get_bank_by_code(code_bank)
                if not bank_in:
                    raise ValueError(f"Bank code '{code_bank}' from header not found in bank data")
                bank_out = BankService.get_bank_by_name(target_bank_name)
                if not bank_out:
                    raise ValueError(f"Bank code '{target_bank_name}' from config file not found in bank data")
                logging.info(f"Bank name determined from header : {bank_in['name']}")
                logging.info(f"Bank name determined from config file : {bank_out['name']}")
                # Validate virement in relation to the determined bank
                ValidationService.validate_virement(virement_in, bank_in,input_file)
                virement_out = VirementService.convert_virement(virement_in,bank_in,bank_out)
                # Save virement to an output file after validation
                VirementService.save_virement(virement_out, output_file)
                virement = VirementService.get_virement(output_file)
                ValidationService.validate_virement(virement, bank_out,output_file)
                logging.info(f"Virement processing completed successfully")

            def processing_vir_file(input_file,target_bank_name,output_file):
                # Log the start of execution
                logging.info('Processing vir file started.')
                # Get virement from file
                virement_in = VirementService.get_virement(input_file)
                # Determine bank_name from header.code_remettant
                code_bank = virement_in.header.code_remettant
                bank_in = BankService.get_bank_by_code(code_bank)
                if not bank_in:
                    raise ValueError(f"Bank code '{code_bank}' from header not found in bank data")
                bank_out = BankService.get_bank_by_name(target_bank_name)
                if not bank_out:
                    raise ValueError(f"Bank code '{target_bank_name}' from config file not found in bank data")
                logging.info(f"Bank name determined from header : {bank_in['name']}")
                logging.info(f"Bank name determined from config file : {bank_out['name']}")
                # Validate virement in relation to the determined bank
                ValidationService.validate_virement(virement_in, bank_in,input_file)
                virement_out = VirementService.convert_virement(virement_in,bank_in,bank_out)
                # Save virement to an output file after validation
                VirementService.save_virement(virement_out, output_file)
                virement = VirementService.get_virement(output_file)
                ValidationService.validate_virement(virement, bank_out,output_file)
                logging.info(f"Virement processing completed successfully")

class HeaderService:

    @staticmethod
    def get_header(file_path):
        return HeaderDAO.get_from_file(file_path)

class BodyService:

    @staticmethod
    def get_body(file_path):
        return BodyDAO.get_from_file(file_path)

    @staticmethod
    def get_specific_body_lines(file_path, ids):
        return BodyDAO.get_lines_from_file(file_path, ids)

    @staticmethod
    def get_body_line(file_path, id):
        return BodyLineDAO.get_from_file(file_path, id)

class BankService:

    @staticmethod
    def get_bank_by_name(bank_name):
        return BankDAO.get_bank_by_name(bank_name)

    @staticmethod
    def get_bank_by_code(bank_code):
        return BankDAO.get_bank_by_code(bank_code)
