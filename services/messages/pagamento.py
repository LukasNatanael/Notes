from core.Time         import Time
from core.Informations import Informations, Color
from core.Validate     import Validate
from helpers           import relatorios
from time              import sleep
from pyperclip         import copy

green_text = Color(content_color='green')

def pagamento():
    infos = Informations()

    try:
        infos.insert_division('Registrar pagamento', color=green_text, new_line=1)
        infos.clear_screen()

        data_atual = Time.data_formatada().full_date
        não_bloquear = Time.data_formatada(3).full_date

        infos.show()
        vencimento = Validate.ask('Vencimento do boleto: ', 'Por favor, informe o vencimento do boleto!', infos)
        infos.write(f'Vencimento: {vencimento}', new_line=1)

        message = f'\n(Lucas N.) Cliente enviou o comprovante referente a {vencimento}. {data_atual}'
        print(f'{message} \n')

        sleep(2)
        print(f'Não bloquear:\n{não_bloquear} \n')
        copy(message)
        sleep(2)
        copy(não_bloquear)

    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()