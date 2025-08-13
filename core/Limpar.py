from core.Informations import Informations
from helpers.input_multiline import input_multiline
from pyperclip import copy
import string
import re
import unicodedata

infos = Informations()

class Limpar:
    @staticmethod
    def personalizado(texto: str, remover_digitos: bool = False, remover_letras: bool = False, remover_especiais: bool = False, remover_espacos: bool = False, remover_quebras: bool = False, strict: bool = False) -> str:
        """
        Remove partes específicas do texto conforme parâmetros.
        """
        resultado = texto

        if strict:
            return ''.join([c for c in resultado if c.isalnum()])
        
        if remover_digitos:
            resultado = ''.join([c for c in resultado if not c.isdigit()])

        if remover_letras:
            resultado = ''.join([c for c in resultado if not c.isalpha()])

        if remover_especiais:
            permitidos = string.ascii_letters + string.digits + ' \n\r\t'
            resultado = ''.join([c for c in resultado if c in permitidos])

        if remover_espacos:
            resultado = resultado.replace(' ', '')

        if remover_quebras:
            resultado = resultado.replace('\n', '').replace('\r', '').replace('\t', '')

        return resultado

    def __init__(self, txt=''):
        self.cities = {
            'mg'   : 'Mogi Guaçu',
            'guaçu': 'Mogi Guaçu',
            'mogi mirim': 'Mogi Guaçu',

            'mm'   : 'Mogi Mirim',
            'mirim': 'Mogi Mirim',
            'mogi mirim': 'Mogi Mirim',
            
            'ec'   : 'Engenheiro Coelho',
            'eng'  : 'Engenheiro Coelho',
            'eng. coelho'       : 'Engenheiro Coelho',
            'engenheiro coelho' : 'Engenheiro Coelho',
            
            'chl'  : 'Conchal',

            'ara'    : 'Araras',
            'araras' : 'Araras',
        }

        if txt:
            self.original_txt = txt.split()
            return self.getFullData(txt)
        else:
            infos.clear_screen()
            txt = input_multiline('Informe os dados que deseja limpar: ')
            self.original_txt = txt.split()
            infos.clear_screen()

            fullData = self.getFullData(txt)
            name     = self.getName(txt)
            document = self.getDocument(txt)
            city     = self.getCity(txt)

            infos.clear_screen()
            print()
            if fullData:
                print(f'{fullData}\n')
            if name:
                print(f'Cadastro: \n{name}\n')
                copy(name)
            if document:
                copy(document) if not name else ''
                print(f'Documento: \n{document}\n')
            if city['city']:
                city = self.cities[city['city'].lower()]
                print(f'Cidade: \n{city}')

    def normalize_text(self, txt: str) -> str:
        """Normaliza espaços, remove espaços não-quebráveis e caracteres invisíveis."""
        txt = txt.replace('\xa0', ' ').replace('\t', ' ')
        txt = re.sub(r'\s+', ' ', txt)
        return txt.strip()

    def removeSpecialChars(self, txt):
        txt = self.transformOneLineStr(txt)
        if txt:
            for punctuation in string.punctuation:
                txt = txt.replace(punctuation, '').strip()
        return txt
    
    def removeTrash(self, txt):
        txt = self.transformOneLineStr(txt)

        cod_cliente = re.findall('Cliente: \d+ - |Cliente \d+ ', txt)
        cpf_cnpj    = re.findall('CPF/CNPJ: |CPFCNPJ |CPF: | CPF |CNPJ: |CNPJ ', txt)
        bloqueado   = re.findall(' Bloqueado: \d| Bloqueado \d| Bloqueado: Não| Bloqueado Não| Bloqueado: {{bloqueado}}| Bloqueado bloqueado', txt)

        if cod_cliente:
            txt = txt.replace(cod_cliente[0], '')
        if cpf_cnpj:
            txt = txt.replace(cpf_cnpj[0], '')
        if bloqueado:
            txt = txt.replace(bloqueado[0], '')

        return txt

    def transformOneLineStr(self, txt):
        if txt:
            txt = txt.strip()
            try:
                txt = txt.replace('\n', ' ')
            except:
                pass
        return txt

    def getDocument(self, txt):
        txt = self.transformOneLineStr(txt)
        document = re.search(r"(\d{2}).(\d{3}).(\d{3})/(\d{4})-(\d{2})|(\d{3}).(\d{3}).(\d{3})-(\d{2})", txt)
        
        if document:
            return self.removeSpecialChars(document[0])
        
        document = re.search(r'\d{14}|\d{11}', txt)    
        txt = self.removeTrash(txt)
        txt = self.removeSpecialChars(txt)

        return document[0] if document else None

    def getCity(self, txt):
        txt = self.removeTrash(txt)
        txt = self.removeSpecialChars(txt)
        txt = self.normalize_text(txt)

        # nomes completos
        full_names_pattern = r'(?<!\w)(mogi guaçu|mogi mirim|araras|conchal|engenheiro coelho|tujuguaba)(?!\w)'
        m = re.search(full_names_pattern, txt, flags=re.IGNORECASE)
        if m:
            return {'city': m.group(1), 'id': [m.start(1), m.end(1)]}

        # abreviações
        codes_pattern = r'(?<!\w)(chl|ara|ec|mm|mg|tuju)(?!\w)'
        m = re.search(codes_pattern, txt, flags=re.IGNORECASE)
        if m:
            return {'city': m.group(1).lower(), 'id': [m.start(1), m.end(1)]}

        return {'city': None, 'id': []}

    def getName(self, txt):
        txt = self.removeTrash(txt)
        txt = self.removeSpecialChars(txt)

        document = self.getDocument(txt)
        city     = self.getCity(txt)

        if city and city['id']:
            startIndex, endIndex = city['id']
            txt = txt[:startIndex] + txt[endIndex:]

        if document:
            txt = txt.replace(document, '')

        return txt.strip()

    def getFullData(self, txt):
        fullData = ''
        name     = self.getName(txt)
        city     = self.getCity(txt)
        document = self.removeSpecialChars(self.getDocument(txt)) if self.getDocument(txt) else None
        
        if name:
            fullData += name
        if document:
            document = f'CNPJ: {document}' if len(document) == 14 else f'CPF: {document}'
            fullData += f' {document}'
        if city['city']:
            city = self.cities[city['city'].lower()]
            fullData = f'{city} - {fullData}'

        return fullData.strip()
