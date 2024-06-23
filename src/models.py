class Header:
    def __init__(self, line):
        if len(line) == 280:
            raise ValueError("Line is too short to be a valid BodyLine")
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
        return f"Header({self.__dict__})"

class BodyLine:
    def __init__(self, line):
        if len(line) == 280:
            raise ValueError("Line is too short to be a valid BodyLine")
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
        self.rib_emetteur = line[50:70]
        self.raison_social_emetteur = line[70:100]
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

    def __repr__(self):
        return f"BodyLine({self.__dict__})"
            
class Virement:
    def __init__(self, header, body):
        self.header = header
        self.body = body

    def __repr__(self):
        return f"Virement(header={self.header}, body={self.body})"
    
class Bank:
    data = [
        { 'code': '01', 'name': 'ATB', 'bic': 'ATBK' },
        { 'code': '02', 'name': 'BFT', 'bic': 'BFTN' },
        { 'code': '03', 'name': 'BNA', 'bic': 'BNTE' },
        { 'code': '04', 'name': 'ATTIJARI', 'bic': 'BSTU', 'num_lot': '0001', 'ccrr': '   ', 'ccra': '   ', 'extension': 'vir'  },
        { 'code': '05', 'name': 'BT', 'bic': 'BTBK' },
        { 'code': '07', 'name': 'AMEN', 'bic': 'CFCT' },
        { 'code': '08', 'name': 'BIAT', 'bic': 'BIAT' },
        { 'code': '10', 'name': 'STB', 'bic': 'STBK' },
        { 'code': '11', 'name': 'UBCI', 'bic': 'UBCI' },
        { 'code': '12', 'name': 'UIB', 'bic': 'UIBK' },
        { 'code': '14', 'name': 'BH', 'bic': 'BHBK' },
        { 'code': '16', 'name': 'CITI', 'bic': 'CITI' },
        { 'code': '17', 'name': 'POSTE', 'bic': 'LPTN', 'ccrr': '000', 'ccra': '000', 'extension': 'txt' },
        {'code': '20', 'name': 'BTK', 'bic': 'BTKO'},
        {'code': '21', 'name': 'TSB', 'bic': 'TSIB'},
        {'code': '23', 'name': 'QNB', 'bic': 'BTQI'},
        {'code': '24', 'name': 'BTE', 'bic': 'BTEX'},
        {'code': '25', 'name': 'ZITOUNA', 'bic': 'BZIT'},
        {'code': '26', 'name': 'BTL', 'bic': 'ATLD'},
        {'code': '28', 'name': 'ABC', 'bic': 'ABCO'},
        {'code': '29', 'name': 'BFPME', 'bic': 'BFPM'},
        {'code': '32', 'name': 'ALBARAKA', 'bic': 'BEIT'},
        {'code': '47', 'name': 'WIFAK', 'bic': 'WKIB'},
        {'code': '81', 'name': 'ZITOUNAPAY', 'bic': 'ETZP'}
    ]
