from core.Informations  import Informations, Color
from helpers            import relatorios
from pyperclip          import copy

def unm():
    try:
        from unidecode import unidecode
        '''
            Substitui todos os espaços entre as palavras por underscore/underline e remove acentos 

            copia o resultado para a área de transferência
        '''
        Informations().clear_screen()
        cadastro = unidecode(input('Cadastro: ').replace(' ', '_').strip())
        
        Informations().clear_screen()
        print(f'Cadastro:\n\n{cadastro}')
        copy(cadastro)
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()