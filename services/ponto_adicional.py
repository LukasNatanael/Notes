from core.Informations import Informations, Color
from core.Validate     import Validate
from core.Formatar     import Formatar
from helpers           import relatorios

from pyperclip         import copy
from collections       import namedtuple

green_text = Color(content_color='green')

def ponto_adicional( notes:dict = {}, extra_notes:list = [] ):
    try:

        infos = Informations()
        Dados = namedtuple( 'Dados_Serviço', [ 'cadastro', 'contato', 'taxa', 'local_atendimento' ] )
        notes_data = Dados( notes.get('Nome'), notes.get('Contato'), notes.get('taxa_serviço'), notes.get('local_atendimento') )

        infos.insert_division('Ponto adicional', color=green_text)

        valor_taxa_do_serviço  = 'R$100,00'
        valor_metragem_do_cabo = 'R$3,00'

        nome    = notes_data.cadastro or Validate.ask('Cadastro: ', 'Por favor, informe o cadastro do cliente!', infos)
        infos.write(f'Cadastro: {nome}', new_line=1)

        contato = notes_data.contato or Validate.ask('Contato: ',  'Por favor, informe o contato do cliente!', infos)
        contato = Formatar.contato(contato)

        infos.write(f'Contato:  {contato}')

        taxa_de_instalação = notes_data.taxa or Validate.confirm('Taxa de instalação: ', infos)
        infos.write(f'Taxa: { f"{valor_taxa_do_serviço} + {valor_metragem_do_cabo} a metragem do cabo" if taxa_de_instalação else "Isenta"}', new_line=1)

        taxa = f'O mesmo está ciente da taxa de instalação no valor de {valor_taxa_do_serviço} + {valor_metragem_do_cabo} a metragem do cabo' if taxa_de_instalação else f'Taxa isenta pois o plano cobre outro ponto'

        feito_por_chat = notes_data.local_atendimento or Validate.confirm('Feito por chat: ', f'{infos}\n')
        local_atendimento = 'Feito por chat' if feito_por_chat else 'Feito por ligação'
        infos.write(f'{local_atendimento}')

        atendimento = f'Contato: {contato} \nCliente entrou em contato solicitando um ponto adicional. {taxa}. {local_atendimento}.'
        
        infos.new_line()
        infos.insert_division('Atendimento', 'left', color=green_text, width=35)
        infos.write(atendimento, jump_line=False, new_line=1)

        relatorios.show_extra_notes( extra_notes )
        infos.show(clear=False)
        informações_extras = infos.extra_info()

        atendimento += informações_extras

        infos.show()
        copy(atendimento)
        relatorios.sucess_message()
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except Exception as e:
        relatorios.error_message(f'Erro: {e}')
        input()

