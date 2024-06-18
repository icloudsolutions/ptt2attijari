import pprint
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(filename='validation.log', level=logging.INFO)

file_path = "C:/Users/aysha/Downloads/ptt2attijari-1.0.1/ptt2attijari-1.0.1/VIR13062024.vir"
#file_path = "C:/Users/aysha/Downloads/ptt2attijari-1.0.1/ptt2attijari-1.0.1/ptt/virements1.txt"
class Entete:
    def __init__(self, line):
        self.sens = line[0:1]
        self.code_valeur = line[1:3]
        self.nature_remettant = line[3:4]
        self.code_remettant = line[4:6]
        self.ccrr = line[6:9]
        self.date_operation = line[9:17]
        self.num_lot = line[17:21]
        self.code_enregistrement = line[21:23]
        self.code_devise = line[23:26]
        self.rang = line[26:28]
        self.montant_total = line[28:43]
        self.nbr_virement = line[43:53]
        self.zone_libre_227 = line[53:280]
        
    def __repr__(self):
        return f"Entete({self.__dict__})"
    
    def test_entete_values(self):
        try:
            assert self.sens == "1", f"sens invalid: {self.sens}. Sens value must be 1"
            assert self.code_valeur == "10", f"Code valeur invalid: {self.code_valeur} code valeur must be 10 "
            assert self.nature_remettant == "1", f"Nature remettant invalid: {self.nature_remettant}"
            assert self.code_remettant == "17", f"Code remettant (code banque) invalid: {self.code_remettant} it must be 17 for la poste"
            assert self.ccrr == "000", f"Code du centre régional remettant  invalid: '{self.ccrr}' it must be '000'"
            assert self.date_operation == datetime.today().strftime("%Y%m%d"), f"Date opération invalid: {self.date_operation} it must be today value {datetime.today().strftime("%Y%m%d")}"
            assert self.num_lot == "0001", f"Numéro de lot invalid: {self.num_lot} it must be '0001' "
            assert self.code_enregistrement == "11", f"Code enregistrement invalid: {self.code_enregistrement} it must be 11"
            assert self.code_devise == "788", f"Code devise invalid: {self.code_devise} it mmust be 788 pour dinars"
            assert self.rang == "00", f"rang invalid: {self.rang} it must be '00'"
        except AssertionError as e:
            logging.error(f"Validation failed in Entete: {e}")

class BodyLine:
    def __init__(self, line):
        self.sens = line[0:1]
        self.code_valeur = line[1:3]
        self.nature_remettant = line[3:4]
        self.code_remettant = line[4:6]
        self.ccrr = line[6:9]
        self.date_operation = line[9:17]
        self.num_lot = line[17:21]
        self.code_enregistrement = line[21:23]
        self.code_devise = line[23:26]
        self.rang = line[26:28]
        self.montant_virement = line[28:43]
        self.num_virement = line[43:50]
        self.rib_emeteur = line[50:70]
        self.raison_social_emeteur = line[70:100]
        self.code_banque_destinataire = line[100:102]
        self.ccra = line[102:105]
        self.rib_beneficiaire = line[105:125]
        self.nom_beneficiaire = line[125:155]
        self.ref_dossier = line[155:175]
        self.code_enregistrement_complementaire = line[175:176]
        self.nbr_enregistrement = line[176:178]
        self.motif_virement = line[178:223]
        self.date_compensation = line[223:231]
        self.code_rejet = line[231:239]
        self.situation_donneur = line[239:240]
        self.type_compte_donneur = line[240:241]
        self.nature_compte_donneur = line[241:242]
        self.flag_change = line[242:243]
        self.zone_libre_37 = line[243:280]
    
    def test_bodyline_values(self):
        try:
            assert self.sens == "1", f"sens invalid: {self.sens}. Sens value must be 1"
            assert self.code_valeur == "10", f"Code valeur invalid: {self.code_valeur} code valeur must be 10 "
            assert self.nature_remettant == "1", f"Nature remettant invalid: {self.nature_remettant}"
            assert self.code_remettant == "17", f"Code remettant (code banque) invalid: {self.code_remettant} must be 17 for la poste"
            assert self.ccrr == "000", f"Code du centre régional remettant  invalid: '{self.ccrr}' must be '000'"
            assert self.date_operation == datetime.today().strftime("%Y%m%d"), f"Date opération invalid: {self.date_operation} must be today value {datetime.today().strftime("%Y%m%d")} "
            assert self.num_lot == "    ", f"Numéro de lot invalid: {self.num_lot} must be '    ' "
            assert self.code_devise == "788", f"Code devise invalid: {self.code_devise} mmust be 788 pour dinars"
            assert self.rang == "00", f"rang invalid: {self.rang} it must be '00'"
            assert self.code_enregistrement == "21", f"Code enregistrement invalid: {self.code_enregistrement} must be 21"
            assert self.code_enregistrement_complementaire == "0", f"Code enregistrement complémentaire invalid: {self.code_enregistrement} must be 0"
            assert self.nbr_enregistrement == "00", f"Nombre enregistrement invalid: {self.code_enregistrement_complementaire} must be 00"
            assert self.date_compensation == datetime.today().strftime("%Y%m%d"), f"Date de compensation invalid: {self.date_compensation} must be today value{datetime.today().strftime("%Y%m%d")}"
            assert self.situation_donneur == "0", f"Situation du donneur d’ordres invalid: {self.situation_donneur} must be 1 (Résident))"
            assert self.type_compte_donneur == "1", f"Type du compte du donneur d’ordres invalid: {self.type_compte_donneur} must be 1 (Compte en dinars)"
            assert self.nature_compte_donneur == " ", f"Nature du compte du donneur d’ordres invalid: {self.nature_compte_donneur} must be ' ' (pas d'exigence d’un dossier de change et de commerce extérieur)"
            assert self.code_banque_destinataire == "17", f"Code institution destinataire invalid: {self.code_banque_destinataire} must be '17' (17 car vers poste )"

        except AssertionError as e:
            logging.error(f"Validation failed in bodyline: {e}")
            print(f"Validation failed in bodyline ref : {self.ref_dossier}: {e}")


    def __repr__(self):
        return f"BodyLine({self.__dict__})"

class Virement:
    def __init__(self, entete, body):
        self.entete = entete
        self.body = body

    def validate(self):
        # Validate header
        self.entete.test_entete_values()
        # Validate each body line
        for line in self.body:
            line.test_bodyline_values()
        # Convert montant_total and montant_virement to integers for comparison
        montant_total = int(self.entete.montant_total)
        montant_virements = sum(int(line.montant_virement) for line in self.body)

        nbr_virement = int(self.entete.nbr_virement)
        count_virement = len(self.body)

        valid_montant = montant_total == montant_virements
        valid_count = nbr_virement == count_virement
        
        print("\nValidation Test Results :")
        print(f"Le Montant total du bordereau est égal à la somme des montants des virements soit {montant_virements/1000} dinars : Test {'Valid' if valid_montant else 'Invalid'}")
        print(f"Le nombre total de virements est égal au nombre de lignes dans le corps du fichier soit {nbr_virement} virements: Test {'Valid' if valid_count else 'Invalid'}")
        logging.info(f"Validation montant total du bordereau soit {montant_virements/1000} dinars : {'Valid' if valid_montant else 'Invalid'}")
        logging.info(f"Validation nombre de virements {nbr_virement}: {'Valid' if valid_count else 'Invalid'}")


    def __repr__(self):
        return f"Virement(entete={self.entete}, body={self.body})"

def parse_vir_file(file_path):
    with open(file_path, 'r' , encoding="utf-8") as file:
        lines = file.readlines()
        entete = Entete(lines[0])
        body = [BodyLine(line) for line in lines[1:]]

    return Virement(entete, body)

def print_readable(virement):
    print("Header:")
    pprint.pprint(virement.entete)
    
    print("\nBody:")
    for i, record in enumerate(virement.body):
        print(f"Virement {i + 1}:")
        pprint.pprint(record)
        print()  # Add an empty line between records

# Usage
virement = parse_vir_file(file_path)
print_readable(virement)
virement.validate()