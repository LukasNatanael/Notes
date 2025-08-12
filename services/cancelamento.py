from core.Informations  import Informations, Color
from core.Validate      import Validate
from core.Formatar      import Formatar
from helpers            import relatorios
from pyperclip          import copy

green_text = Color(content_color='green')

def cancelamento( notes:dict = {}, extra_notes:list = [] ):
    try:
        infos = Informations()

        infos.clear_data()
        infos.insert_division('Atendimento de cancelamento', color=green_text, new_line=1)

        id_huggy = Validate.confirm('Contato feito pelo Huggy', infos)

        if id_huggy:
            local_contato = Validate.ask('ID Huggy', 'Por favor, informe o ID do Huggy!', infos)
            local_contato = f'ID Huggy: {local_contato}'
        else:
            local_contato = notes.get('Contato') or Formatar.contato(Validate.ask('Contato', 'Por favor, informe o contato do cliente!', infos))
            local_contato = f'Contato: {local_contato}'

        infos.write(local_contato, new_line=1)

        relatorios.show_extra_notes(extra_notes)
        infos.show(clear=False)
        atendimento = input('[ | para quebra de linha ] \nEscreva o atendimento abaixo: \n\n')

        atendimento = atendimento.replace(' | ', '\n')
        infos.write( atendimento, new_line=1)

        if atendimento != '':
            copy(atendimento)
            relatorios.sucess_message()
            infos.write('Atendimento de cancelamento gerado')

    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except Exception as e:
        relatorios.error_message(f'Erro: {e}')
        input()