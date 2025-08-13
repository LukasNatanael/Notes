from   core.Informations       import Informations
from   helpers.input_multiline import input_multiline
from   pyperclip               import copy
import string
import re

infos = Informations()

class Limpar:

    @staticmethod
    def personalizado(texto: str, remover_digitos: bool = False, remover_letras: bool = False, remover_especiais: bool = False, remover_espacos: bool = False, remover_quebras: bool = False, strict: bool = False) -> str:
        """
        Remove partes específicas do texto conforme parâmetros.

        Args:
            texto: texto de entrada
            remover_digitos: remove números (0-9)
            remover_letras: remove letras (a-zA-Z)
            remover_especiais: remove pontuação e símbolos
            remover_espacos: remove espaços simples ( )
            remover_quebras: remove \n, \r e tabs (\t)

        Returns:
            Texto modificado
        """
        resultado = texto


        if strict:
            # Apenas letras e dígitos
            resultado = ''.join([c for c in resultado if c.isalnum()])
            return resultado
        
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


    def __init__(self,txt=''):

        self.cities = {
            'mg'   : 'Mogi Guaçu',
            'guaçu': 'Mogi Guaçu',
            'mogi mirim': 'Mogi Guaçu',

            'mm'   : 'Mogi Mirim',
            'mirim': 'Mogi Mirim',
            'mogi mirim': 'Mogi Mirim',
            
            'ec'   : 'Engenheiro Coelho',
            'eng'  : 'Engenheiro Coelho',
            'eng. coelho'        : 'Engenheiro Coelho',
            'engenheiro coelho'  : 'Engenheiro Coelho',
            
            'chl'     : 'Conchal',

            'ara'    : 'Araras',
            'araras' : 'Araras',
        }

        if txt:
            self.original_txt = txt.split()
            return self.getFullData(txt)
        else:
            txt = input_multiline('Informe os dados que deseja limpar: ')
            self.original_txt = txt.split()

            infos.clear_screen()

            fullData = self.getFullData(txt)
            name     = self.getName(txt)
            document = self.getDocument(txt)
            city     = self.getCity(txt) # deixar minusculo caso não funcione

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


    def removeSpecialChars(self, txt):
        txt = self.transformOneLineStr(txt)
        if txt:
            for punctuation in string.punctuation: txt = txt.replace( punctuation, '').strip()

        return txt
    
    def removeTrash(self, txt):
        txt = self.transformOneLineStr(txt)

        cod_cliente = re.findall('Cliente: \d+ - |Cliente \d+ ', txt)
        cpf_cnpj    = re.findall('CPF/CNPJ: |CPFCNPJ |CPF: | CPF |CNPJ: |CNPJ ', txt)
        bloqueado   = re.findall(' Bloqueado: \d| Bloqueado \d| Bloqueado: Não| Bloqueado Não| Bloqueado: {{bloqueado}}| Bloqueado bloqueado', txt)

        if cod_cliente:
            cod_cliente = cod_cliente[0]
            txt = txt.replace( cod_cliente, '' )
            
        if cpf_cnpj:
            cpf_cnpj = cpf_cnpj[0]
            txt = txt.replace( cpf_cnpj, '' )
            
        if bloqueado:
            bloqueado = bloqueado[0]
            txt = txt.replace( bloqueado, '' )

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

        # funcionando
        txt = self.transformOneLineStr(txt)
        document = re.search("(\d{2}).(\d{3}).(\d{3})/(\d{4})-(\d{2})|(\d{3}).(\d{3}).(\d{3})-(\d{2})", txt)
        
        if document:
            return self.removeSpecialChars(document[0])
        
        document = re.search('\d{14}|\d{11}', txt)    
        txt = self.removeTrash(txt)
        txt = self.removeSpecialChars(txt)

        if not document:
            return None

        return document[0]

    def getCity(self, txt):

        txt = self.removeTrash(txt)
        txt = self.removeSpecialChars(txt)

        city = None
        
        import re
        city = re.findall('Mogi Guaçu|Mogi Mirim|Araras|Conchal|Engenheiro Coelho', txt)

        if city:
            city = city[0]
            city = city.split()

            if len(city) == 1:
                cityLength = len(city[0])
                cityIndex  = txt.index(city[0])
                startIndex = cityIndex
                endIndex   = cityIndex + len(city[0])

                index = [ startIndex, endIndex ]

                for k, v in self.cities.items():
                    for content in txt.split():
                        if ( v == content or v == content.lower()):
                            city = k

                data = { 'city': city, 'id': index }

                print('Em cima 1')

                return data
            
            elif len(city) == 2:
                city = ' '.join(city)

                cityLength = len(city)
                cityIndex  = txt.index(city)
                startIndex = cityIndex
                endIndex   = cityIndex + cityLength
                
                index = [ startIndex, endIndex ]

                for k, v in self.cities.items():
                    if v == city:
                        city = k

                data = { 'city': city, 'id': index }

                print('Em cima 2')
                return data

            txt = txt.split()
            index = []

            for k, v in self.cities.items():
                for cont in city:
                    for id, content in enumerate(txt):
                        if cont == content:
                            index.append(id)
                            city = k

        else:
            
            id = 0
            index = []
            txt = txt.split()

            # for content in txt:
            for id, content in enumerate(txt):
                for k, v in self.cities.items():

                    if ((len(content) == 2 or len(content) == 3) and (k == content or k == content.lower())):
                        txt = ' '.join(txt)

                        city = content

                        cityLength = len(city)
                        startIndex = txt.index(city)
                        endIndex   = startIndex + (cityLength + 1)


                        index = [ startIndex, endIndex ]

                        print('Em baixo 1')
                        print( len(txt), [startIndex, endIndex])
                id += 1


        data = { 'city': city, 'id': index }
        
        return data

    def getName(self, txt):

        txt = self.removeTrash(txt)
        txt = self.removeSpecialChars(txt)

        document = self.getDocument(txt)
        city     = self.getCity(txt)

        if city:
            print(city)
            try:
                try:
                    startIndex = city['id'][0]
                    endIndex   = city['id'][1]

                    print( txt[startIndex: endIndex]  )

                    txt = txt.replace(txt[startIndex: endIndex], '')

                    print(txt)
                except:
                    pass
            except:
                if city[1] in txt.split():
                    txt = txt.split()

                    index = txt.index(city[1])
                    txt.pop(index)
                    txt = ' '.join(txt)
                    
                city = self.cities[city[0]]

                for k, v in self.cities.items():
                    for texto in txt:
                        if ((len(texto) == 2 or len(texto) == 3) and k == texto):
                            index = txt.index(texto)
                            txt[index] = ''
                        elif ( v == texto or v == texto.lower()):
                            index = txt.index(texto)
                            txt[index] = ''

                txt = ''.join(txt)

        if document:
            txt = txt.replace(document, '')

        return txt.strip()

    def getFullData(self, txt):
        fullData = ''

        name     = self.getName(txt)
        city     = self.getCity(txt)
        document = self.removeSpecialChars(self.getDocument(txt))
        
        if name:
            fullData += name

        if document:
            document = f'CNPJ: {document}' if len(document) == 14 else f'CPF: {document}'
            fullData += f' {document}'

        if city['city']:
            city = self.cities[city['city'].lower()]
            fullData = f'{city} - {fullData}'


        return fullData.strip()