from core.Informations  import Informations
from core.Validate      import Validate
from core.Formatar      import Formatar
from helpers            import relatorios
from pyperclip          import copy
from collections        import namedtuple

def cep(cod:str='', msg_screen:str='', error:str='', retornar:bool=False, notes:object = {}) -> str | object:
    try:
        infos = Informations()

        while True:
            import requests

            infos.clear_screen()
            if cod in [ '', None ]:
                cod = Validate.ask('Informe o CEP a ser verificado: ', 'Por favor, informe um CEP a ser consultado!', f'{msg_screen}{error}')

            cep = Formatar.numeros(str(cod))

            if len(cep) == 8:
                Endereço = namedtuple( 'Endereço', [ 'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep', 'error' ] )

                endereço = requests.get( f'https://viacep.com.br/ws/{cep}/json/' ).json()
                endereço = Endereço( endereço['logradouro'], ' ', endereço['bairro'], endereço['localidade'], endereço['uf'], endereço['cep'], error=False)

                endereço_completo = f"Endereço: \n{ endereço.rua } nº[{ endereço.numero }], { endereço.bairro }, {endereço.cidade}-{endereço.estado}, CEP: {endereço.cep} \n"

                numero_casa = notes.get('numero_casa') or Validate.ask('Número da casa: ', 'Por favor, informe o numero da casa!', f'{msg_screen}\n{endereço_completo}')

                endereço = Endereço( endereço.rua, numero_casa, endereço.bairro, endereço.cidade, endereço.estado, endereço.cep, error=False )

                infos.clear_screen()
                endereço_completo = f"Endereço: \n{ endereço.rua } nº{ endereço.numero }, { endereço.bairro }, { endereço.cidade }-{ endereço.estado }, CEP: { endereço.cep } \n"

                if retornar:
                    return endereço
                infos.clear_screen()
                print(endereço_completo)
                copy(endereço_completo.replace('Endereço: \n', ''))
                break
            
            else:
                from colorama import Fore, Style

                Endereço = namedtuple( 'Endereço', [ 'error', 'message' ] )

                error = f'{Fore.RED}\nCEP inválido! Informe um CEP válido.{Style.RESET_ALL}'
                if retornar:
                    error = Endereço( error=True, message=error )
                    return error
                
                infos.clear_screen()
                continue

    except KeyError:
        infos.clear_screen()
        error = f'{Fore.RED}\nDados do endereço inválidos! Informe um CEP correto!{Style.RESET_ALL}'
        if retornar:
            error = Endereço( error=True, message=error )
            return error
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except Exception as e:
        relatorios.error_message(f'Erro: {e}')
        input()
    