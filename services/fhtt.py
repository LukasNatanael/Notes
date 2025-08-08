from core.Informations import Informations, Color
from core.Validate     import Validate
from core.Formatar     import Formatar
from helpers           import relatorios

from pyperclip         import copy
from collections       import namedtuple

green_text = Color(content_color='green')

def fhtt(notes:dict = {}, extra_notes:list = []):
    try:
        from helpers.cep import cep
        from core.Menu import Menu, MenuOptions

        Dados = namedtuple('Dados_Serviço', [ 'cadastro', 'contato', 'serviço', 'cep', 'numero_casa', 'local' ])
        notes_data = Dados( notes.get('Nome'), notes.get('Contato'), notes.get('Serviço'), notes.get('CEP'), notes.get('numero_casa'), notes.get('Local') )

        lista_serviços = [ 'Mudança de endereço', 'Mudança de cômodo' ]

        menu_serviços = Menu(
            MenuOptions('Serviço', lista_serviços)
        )

        infos       = Informations()
        extra_infos = Informations()

        extra_infos.insert_division('FHTT | Mudança de cômodo', color=green_text)

        cliente = notes_data.cadastro or Validate.ask('Cliente: ', 'Por favor, informe o nome do cliente!', extra_infos)
        extra_infos.write(f'Cliente: {cliente}', new_line=1)

        contato = notes_data.contato or  Validate.ask('Contato: ', 'Por favor, informe o contato do cliente!', extra_infos)
        contato = Formatar.contato(contato)
        extra_infos.write(f'Contato: {contato}')

        if not notes_data.serviço:
            menu_serviços.show()
            serviço = menu_serviços.choseOption[0]
            serviço = lista_serviços[serviço]
        else:
            serviço = notes_data.serviço
        
        extra_infos.clear_data()

        infos.insert_division( 'Mudança de endereço - FHTT' if serviço == 'FHTT' else 'Mudança de cômodo', color=green_text )
        infos.write(f'Cliente: {cliente}', new_line=1)
        infos.write(f'Contato: {contato}')

        
        if serviço == 'FHTT':
            serviço = 'mudança de endereço'
            error = ''
            while True:
                endereço = cep(cod=notes_data.cep, retornar=True, notes=notes, msg_screen=infos) or cep( msg_screen=infos, error=error, retornar=True )

                if endereço.error:
                    error += endereço.message if endereço.error == '' else ''
                
                elif endereço:
                    error = ''
                    endereço_completo = f'{ endereço.rua } nº{ endereço.numero }, { endereço.bairro }, { endereço.cidade }-{ endereço.estado }, CEP: { endereço.cep }'
                    break
                
            numero = notes_data.numero_casa or endereço.numero
            infos.write(f'CEP: {endereço.cep} | Nº{ numero }', new_line=1)
            infos.write(f'Rua: {endereço.rua}, {endereço.bairro}')
            infos.write(f'Cidade: {endereço.cidade}')

            local = f' para a {endereço_completo}'

        else:
            local = notes_data.local or Validate.ask('Em qual cômodo os aparelhos irão ficar: ', 'Por favor, informe em qual cômodo os aparelhos irão ficar!', f'{infos}\n[ 00 ] Não foi informado\n')

            local = '' if local in [ '', '00' ] else f'{local}'

            infos.write(f'Novo cômodo: {local.capitalize()}' if local != '' else 'Novo cômodo: n/a')
            
            local = f' para {local[-1].lower()} {local}' if local != '' else ''

        taxa_serviço = Validate.confirm('Taxa de serviço', infos)
        
        if taxa_serviço:
            taxa_serviço = 'O mesmo está ciente da taxa de instalação no valor de R$100,00(caso não tenha fibra existente)'

            infos.write('Taxa: R$100,00', jump_line=False)
            dividido_taxa = Validate.confirm('Valor dividido em 2x', infos)

            dividido_taxa = ' dividido em 2x' if dividido_taxa else ''
            infos.write(f'{dividido_taxa}')

            taxa_serviço += f'{dividido_taxa}.'
        else:
            infos.write('Taxa: Isenta pois fidelizou', new_line=1)
            taxa_serviço = f'Taxa de serviço isenta pois, fidelizou o contrato por +12 meses.'

        feito_por_ligação = Validate.confirm('Feito por ligação', infos)

        local_atendimento = 'Feito por ligação' if feito_por_ligação else 'Feito por chat'

        infos.write(f'{local_atendimento}')
        infos.new_line()
        infos.insert_division()

        atendimento = f'Contato: { contato } \nCliente entrou em contato solicitando uma { serviço.lower() }{local}. Cliente ciente que a equipe responsável pelos agendamentos entrará em contato para verificar o dia e horário para atendimento. { taxa_serviço } { local_atendimento }. Verificar no local por gentileza. Ligar com antecedência.'.strip()

        infos.write('Atendimento:', new_line=1)
        infos.write(atendimento)

        relatorios.show_extra_notes(extra_notes)
        infos.show( clear=False )

        informações_extras = infos.extra_info()
        atendimento += informações_extras

        infos.show()
        copy(atendimento)

        relatorios.sucess_message()
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()
    
