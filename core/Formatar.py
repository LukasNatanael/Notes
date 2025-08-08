class Formatar:

    @staticmethod
    def contato( contact:str ):
        import re
        contato = ''.join( re.findall('\d+', contact) )

        return contato
    
    @staticmethod
    def moeda( valor ):
        a = '{:,.2f}'.format(float(valor))
        b = a.replace(',','v')
        c = b.replace('.',',')
        return 'R$' + c.replace('v','.')
    
    @staticmethod
    def numeros( number:str ):
        import re
        numeros = ''.join( re.findall('\d+', number) )

        return numeros

    @staticmethod
    def luz_ONU( luz ):
        try:
            luz = str("%.2f" % float(luz))
        except:
            pass
        
        luz += 'dbm' if 'dbm' not in luz else ''
        luz = f'-{luz}' if '-' not in luz else luz

        return luz
    
    @staticmethod
    def ordenar_dict(dados: dict, ordem: list) -> dict:
        return {chave: dados[chave] for chave in ordem if chave in dados}

    @staticmethod
    def ordenar_lista(lista: list, ordem: list) -> list:
        return [Formatar.ordenar_dict(d, ordem) for d in lista]