from core.Informations  import Informations, Color
from core.Validate      import Validate
from core.Time          import Time
from helpers            import relatorios

from pyperclip          import copy
from time               import sleep

def desbloqueio():
    try:
        infos      = Informations()
        extra_info = Informations()

        data       = Time.data_formatada(3)
        dia_semana = str(data.dia_semana).lower()
        dia          = data.dia
        não_bloquear = data.full_date

        infos.insert_division('Desbloqueio')

        extra_info.write('Dias disponíveis: ', new_line=1)
        extra_info.new_line()

        cliente = Validate.ask('Cliente: ', 'Informe o nome do cliente!', infos)
        infos.write(f'Cadastro: {cliente}', new_line=1)
        extra_info.clear_data()

        dia_liberação = f"{dia}({dia_semana})".lower()

        infos.write(f'Liberação até: {dia_liberação}')

        message = f'Cliente entrou em contato solicitando liberação do acesso. Aberto exceção até dia {dia_liberação}. Alterado status do cadastro para avisado até o respectivo dia.'
        
        infos.write(message)

        infos.show()
        infos.write(f'Não bloquear: \n{não_bloquear}\n')
        
        sleep(.5)
        copy(não_bloquear)

        infos.extra_info()
        
        infos.show()
        sleep(.5)
        copy(message)
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()