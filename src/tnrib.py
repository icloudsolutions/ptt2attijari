import re

class TNRIB:
    data = [
        { 'code': '00', 'name': 'BCT', 'bic': 'BCT' },
        { 'code': '01', 'name': 'ATB', 'bic': 'ATBK' },
        { 'code': '02', 'name': 'BFT', 'bic': 'BFTN' },
        { 'code': '03', 'name': 'BNA', 'bic': 'BNTE' },
        { 'code': '04', 'name': 'ATTIJARI', 'bic': 'BSTU' },
        { 'code': '05', 'name': 'BT', 'bic': 'BTBK' },
        { 'code': '07', 'name': 'AMEN', 'bic': 'CFCT' },
        { 'code': '08', 'name': 'BIAT', 'bic': 'BIAT' },
        { 'code': '10', 'name': 'STB', 'bic': 'STBK' },
        { 'code': '11', 'name': 'UBCI', 'bic': 'UBCI' },
        { 'code': '12', 'name': 'UIB', 'bic': 'UIBK' },
        { 'code': '14', 'name': 'BH', 'bic': 'BHBK' },
        { 'code': '16', 'name': 'CITI', 'bic': 'CITI' },
        { 'code': '17', 'name': 'POSTE', 'bic': 'LPTN' },
        { 'code': '20', 'name': 'BTK', 'bic': 'BTKO' },
        { 'code': '21', 'name': 'TSB', 'bic': 'TSIB' },
        { 'code': '23', 'name': 'QNB', 'bic': 'BTQI' },
        { 'code': '24', 'name': 'BTE', 'bic': 'BTEX' },
        { 'code': '25', 'name': 'ZITOUNA', 'bic': 'BZIT' },
        { 'code': '26', 'name': 'BTL', 'bic': 'ATLD' },
        { 'code': '28', 'name': 'ABC', 'bic': 'ABCO' },
        { 'code': '29', 'name': 'BFPME', 'bic': 'BFPM' },
        { 'code': '32', 'name': 'ALBARAKA', 'bic': 'BEIT' },
        { 'code': '47', 'name': 'WIFAK', 'bic': 'WKIB' },
        { 'code': '81', 'name': 'ZITOUNAPAY', 'bic': 'ETZP' }
    ]

    def __init__(self, value):
        self.value = value
        self.valid = self.is_valid()
        if self.valid:
            self.iban_num = self.iban()
            self.bic_num = self.bic()
            self.account_number = self.account_number()
            self.bank_name = self.bank_name()

    def _get_exist_element_by_current_code(self):
        return next((item for item in self.data if item['code'] == self.value[:2]), None)

    def is_valid(self):
        regex = r'^[0-9]{20}$'
        return (
            bool(re.match(regex, self.value)) and
            self._get_exist_element_by_current_code() and
            int(self.value[-2:]) == (97 - int(self.value[:18] + '00') % 97)
        )

    def iban(self):
        if self.is_valid():
            return f"TN59 {self.value[:2]} {self.value[2:5]} {self.value[5:18]} {self.value[18:20]}"

    def bic(self):
        if self.is_valid():
            return f"{self._get_exist_element_by_current_code()['bic']}TNTT"

    def account_number(self):
        if self.is_valid():
            return self.value[5:18]

    def bank_name(self):
        if self.is_valid():
            return self._get_exist_element_by_current_code()['name']
