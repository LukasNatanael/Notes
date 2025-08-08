from core.Informations  import Informations, Color
from core.Validate      import Validate
from core.Formatar      import Formatar
from pyperclip          import copy
from helpers            import relatorios

green_text = Color(content_color='green')

def atendimento_generico( notes:dict, extra_notes:list ):
    try:
        infos = Informations()

        infos.clear_data()
        infos.insert_division('Atendimento', color=green_text, new_line=1)

        relatorios.show_extra_notes(extra_notes)
        infos.show(clear=False)
        atendimento = input('[ | para quebra de linha ] \nEscreva o atendimento abaixo: \n\n')

        if atendimento != '':
            atendimento = atendimento.replace(' | ', '\n')
            # atendimento = corretor.corrigir_texto(atendimento)
            OS = Validate.confirm('Será necessário abrir OS', str(infos) + f'\n{atendimento}\n')

            if OS:
                contato = notes.get('Contato') or Formatar.contato(Validate.ask('Contato', 'Por favor, informe o contato do cliente!', infos))
                atendimento = f'Contato: {contato} \n{atendimento}'

            infos.write( atendimento, new_line=1 )
            infos.show()

            if atendimento != '':
                copy(atendimento)
                relatorios.sucess_message()
                extra_notes.append('Atendimento gerado')
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()