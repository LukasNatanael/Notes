from core.Informations import Informations, Color
from core.Validate     import Validate
from core.Formatar     import Formatar
from helpers           import relatorios

from pyperclip         import copy
from collections       import namedtuple

red_text   = Color(content_color='red')
green_text = Color(content_color='green')


def los(notes:dict = {}, extra_notes:list = []):
    try:
        infos         = Informations()
        infos_extra   = Informations()

        Dados = namedtuple( 'Dados_Serviço', [ 'cadastro', 'contato', 'alarme', 'tempo_sem_acesso' ] )
        
        notes_data = Dados( notes.get('Nome'), notes.get('Contato'), notes.get('alarme'), notes.get('tempo_sem_acesso') )

        infos.insert_division('Sem acesso - Fibra rompida', color=red_text)
        infos_extra.write('[ 00 ] - Não foi possível verificar', new_line=1)

        alarmes = { 
            'LINK_LOSS'   : 'LINK_LOSS',
            'DYING_GASP'  : 'DYING_GASP',

            'LOS': 'LOS piscando',
            'PON': 'PON piscando',
            'los': 'LOS piscando',
            'pon': 'PON piscando',
        }

        # Dados do Notes.py
        cadastro = notes_data.cadastro or Validate.ask('Cadastro: ', 'Informe o cadastro do cliente!', infos)
        contato  = notes_data.contato  or Validate.ask('Contato: ',  'Informe o contato do cliente!', infos)
        contato  = Formatar.contato(contato)

        infos.write(f'Cadastro: {cadastro}', new_line=1)
        infos.write(f'Contato:  {contato}')

        infos_extra_infos = infos.__str__() + infos_extra.__str__()

        alarme = notes_data.alarme or Validate.ask('Alarme em sistema: ', 'Informe o alarme!', infos_extra_infos, alarmes)

        alarme = alarme.upper()
        if alarme in [ 'LOS', 'PON' ]:
            alarme = f'{alarmes[alarme]} no aparelho'
        else:
            tempo = notes_data.tempo_sem_acesso or Validate.ask('Sem acesso há quanto tempo: ', 'Informe o tempo sem acesso!', infos)
            alarme = f'Alarmando {alarmes[alarme]} em sistema há {tempo}'
        
        infos.write(alarme)

        atendimento = (
            f'Contato: {contato} \n'
            f'Cliente entrou em contato alegando estar sem acesso à rede. '
            f'{alarme}. Verificar no local por favor. Ligar com antecedência.'
        )

        infos.new_line()
        infos.insert_division('Atendimento', 'left', color=green_text, width=35, new_line=1)
        infos.write(atendimento, new_line=1, jump_line=False)

        relatorios.show_extra_notes(extra_notes)
        infos.show( clear=False )

        atendimento += infos.extra_info()
        copy(atendimento)

        relatorios.sucess_message()
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except Exception as e:
        relatorios.error_message(f'Erro!\n {e}')
        input()
