from core.Informations  import Informations, Color
from core.Validate      import Validate
from helpers            import relatorios
from pyperclip          import copy

def agendamento():
    try:
        infos = Informations()
        infos.insert_division('Verificar agendamento')

        dia     = Validate.ask('Qual dia de realização', 'Por favor informe algo!', infos)
        infos.write(f'Dia do serviço: {dia}', new_line=1)

        horario = Validate.ask('Qual o horário de realização', 'Por favor informe algo!', infos)
        infos.write(f'Horário do serviço: {horario}')


        dias_semana = [ 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo' ]

        if dia.lower() in [ *dias_semana, 'hoje', 'amanhã']:
            dia = dia
        else:
            dia = f'dia {dia}'

        message = f'Pelo que verifiquei o serviço está agendado para {dia} próximo as {horario} sendo assim, peço que aguarde até que os técnicos se desloquem ao local. Eles irão ligar com antecedência.'

        infos.show()
        print(message)
        copy(message)
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()