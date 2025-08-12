from core.Informations  import Informations, Color
from core.Validate      import Validate
from helpers            import relatorios
from pyperclip          import copy

green_text = Color(content_color='green')

def suspensão():
    try:
        infos = Informations()

        infos.insert_division('Suspensão do acesso', color=green_text)

        while True:
            qtd_meses   = Validate.ask('Quantidade de meses', 'Por favor, informe a quantidade de meses!' , str(infos) + '\nSão permitidos no máximo 3 meses de suspensão')
            if int(qtd_meses) <= 3:
                break

        infos.write(f'Meses de suspensão: {qtd_meses}', new_line=1)

        inicio_susp = Validate.ask('Inicio da suspensão', 'Por favor, informe o início da suspensão!' ,infos)
        infos.write(f'Início: {inicio_susp}')

        fim_susp    = Validate.ask('Fim da suspensão'   , 'Por favor, informe o fim da suspensão!' ,infos)
        infos.write(f'Fim: {fim_susp}')
        
        motivo      = Validate.ask('Motivo da suspensão', 'Por favor, informe o motivo da suspensão!' ,infos)
        infos.write(f'Motivo: {motivo}', new_line=2)

        atendimento = f'Cliente entrou em contato solicitando suspensão do acesso por {qtd_meses}, do dia {inicio_susp} a {fim_susp}. Motivo: {motivo}'

        infos.insert_division('Atendimento', color=green_text, width=30, new_line=2)
        infos.write(atendimento)
        copy(atendimento)

        infos.show()
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except Exception as e:
        relatorios.error_message(f'Erro: {e}')
        input()
