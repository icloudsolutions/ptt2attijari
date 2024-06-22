from models import Header, BodyLine, Virement, Bank

class VirementDAO:

    @staticmethod
    def get_vir_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        header = Header(lines[0])  # Assuming Header can be initialized with a single line
        body = [BodyLine(line) for line in lines[1:]]  # Assuming BodyLine can be initialized with a single line
        return Virement(header, body)

    @staticmethod
    def write_vir_file2(virement, output_path):
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(repr(virement.header) + '\n')  # Assuming repr of header gives the correct string representation
            for body_line in virement.body:
                file.write(repr(body_line.ge) + '\n')  # Assuming repr of body_line gives the correct string representation
    
    @staticmethod
    def write_vir_file(virement, output_path):
        with open(output_path, 'w', encoding='utf-8') as file:
            # Writing header
            header_string = f"{virement.header.sens:1}{virement.header.code_valeur:2}{virement.header.nature_remettant:1}" \
                            f"{virement.header.code_remettant:2}{virement.header.ccrr:3}{virement.header.date_operation:8}" \
                            f"{virement.header.num_lot:4}{virement.header.code_enregistrement:2}{virement.header.code_devise:3}" \
                            f"{virement.header.rang:2}{virement.header.montant_total:15}{virement.header.nbr_virement:10}" \
                            f"{virement.header.zone_libre_227:227}"
            file.write(header_string.strip().ljust(280) + '\n')

            # Writing body lines
            for body_line in virement.body:
                body_line_string = f"{body_line.sens:1}{body_line.code_valeur:2}{body_line.nature_remettant:1}" \
                                f"{body_line.code_remettant:2}{body_line.ccrr:3}{body_line.date_operation:8}" \
                                f"{body_line.num_lot:4}{body_line.code_enregistrement:2}{body_line.code_devise:3}" \
                                f"{body_line.rang:2}{body_line.montant_virement:15}{body_line.num_virement:7}" \
                                f"{body_line.rib_emetteur:20}{body_line.raison_social_emetteur:30}" \
                                f"{body_line.code_banque_destinataire:2}{body_line.ccra:3}" \
                                f"{body_line.rib_beneficiaire:20}{body_line.nom_beneficiaire:30}" \
                                f"{body_line.ref_dossier:20}{body_line.code_enregistrement_complementaire:1}" \
                                f"{body_line.nbr_enregistrement:2}{body_line.motif_virement:45}" \
                                f"{body_line.date_compensation:8}{body_line.code_rejet:8}" \
                                f"{body_line.situation_donneur:1}{body_line.type_compte_donneur:1}" \
                                f"{body_line.nature_compte_donneur:1}{body_line.flag_change:1}" \
                                f"{body_line.zone_libre_37:37}"
                file.write(body_line_string.strip().ljust(280) + '\n')

    @staticmethod
    def add_body_line(virement, body_line):
        virement.body.append(body_line)

    @staticmethod
    def update_body_line(virement, index, body_line):
        if 0 <= index < len(virement.body):
            virement.body[index] = body_line
        else:
            raise IndexError("Index out of range")

    @staticmethod
    def delete_body_line(virement, index):
        if 0 <= index < len(virement.body):
            del virement.body[index]
        else:
            raise IndexError("Index out of range")

    @staticmethod
    def update_code_remettant(virement, code):
        if code is not None:
            virement.header.code_remettant = code
            for body_line in virement.body:
                body_line.code_remettant = code

    @staticmethod
    def update_ccrr(virement, ccrr):
        if ccrr is not None:
            virement.header.ccrr = ccrr
            for body_line in virement.body:
                body_line.ccrr = ccrr

    @staticmethod
    def update_ccra(virement, ccra):
        if ccra is not None:    
            for body_line in virement.body:
                body_line.ccra = ccra

    @staticmethod
    def update_num_lot(virement, num_lot):
        if num_lot is not None:    
            virement.header.num_lot = num_lot
            for body_line in virement.body:
                body_line.num_lot = num_lot

    @staticmethod
    def convert(virement, bank_out):
        # Update num_lot, ccra, ccrr, and code_remettant
        VirementDAO.update_num_lot(virement, bank_out['num_lot'])
        VirementDAO.update_ccra(virement, bank_out['ccra'])
        VirementDAO.update_ccrr(virement, bank_out['ccrr'])
        VirementDAO.update_code_remettant(virement, bank_out['code'])
        # Return the modified virement object
        return virement

class HeaderDAO:
    @staticmethod
    def get_from_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
        header = Header(line)
        return header


class BodyDAO:
    @staticmethod
    def get_from_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()[1:]  # Skip the first line (header)
        body = [BodyLine(line.strip()) for line in lines]
        return body

    @staticmethod
    def get_lines_from_file(file_path, ids):
        body_lines = []
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()[1:]  # Skip the first line (header)
            for id in ids:
                if 0 <= id < len(lines):
                    body_lines.append(BodyLine(lines[id].strip()))
                else:
                    raise IndexError(f"Index {id} is out of range for the body lines in the file.")
        return body_lines


class BodyLineDAO:
    @staticmethod
    def get_from_file(file_path, id):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()[1:]  # Skip the first line (header)
        if 0 <= id < len(lines):
            body_line = BodyLine(lines[id].strip())
            return body_line
        else:
            raise IndexError(f"Index {id} is out of range for the body lines in the file.")

class BankDAO:
    @staticmethod
    def get_bank_by_name(bank_name):
        for bank in Bank.data:
            if bank['name'] == bank_name:
                return bank
        return None

    @staticmethod
    def get_bank_by_code(bank_code):
        for bank in Bank.data:
            if bank['code'] == bank_code:
                return bank
        return None
