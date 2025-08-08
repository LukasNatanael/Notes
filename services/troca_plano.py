from core.Informations import Informations, Color
from core.Validate     import Validate
from core.Formatar     import Formatar
from helpers           import relatorios

from pyperclip         import copy
from collections       import namedtuple

green_text = Color(content_color='green')

def troca_plano( notes:dict = {}, extra_notes:list = [] ):
    try:
        Plano = namedtuple('Plano', [ 'nome', 'valor' ])
        infos              = Informations()
        extra_infos        = Informations()
        valores_str        = Informations()
        planos_str         = Informations()
        meses_str          = Informations()

        infos.insert_division('Alteração de plano', new_line=2, color=green_text)

        planos = {
            '69.90':  'Fibra 10mb',
            '84.90':  ['Start 100mb', 'Hiper Start 100mb'],
            '99.90':  ['Familia Mais 300mb', 'Hiper Family 700mb'],
            '129.90': ['Cine Plus 600mb', 'Hiper Cine 1GB'],
            '149.90': ['Infinite 1GB', 'Hiper Infinite 1GB'],
        }

        valores = [ '69.90', '84.90', '99.90', '129.90', '149.90' ] 
        vencimentos = [ '5', '10', '15', '20', '25' ]
        meses_numerais = [*range(1, 13)]
        meses_extenso = [ 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro' ]
        
        for m in meses_numerais: meses_numerais[m-1] = str(m).zfill(2)
        
        meses = meses_numerais + meses_extenso

        valores_str.write('Valores dos planos:', new_line=1)
        avaliable_choices = []

        for valor in valores: valores_str.write(f'{Formatar.moeda(valor)}', jump_line=False)
        valores_str.new_line()

        meses_str.new_line(1)
        meses_str.insert_division('Meses disponíveis [ numeral ou extenso ]', width=50, new_line=2, color=green_text)

        for cont in range(len(meses_numerais)):
            if cont == 6:
                meses_str.new_line(1)
            meses_str.write(f'{meses_extenso[cont]}', jump_line=False)
        meses_str.new_line(1)

        infos_extras_infos = infos.__str__() + valores_str.__str__()

        plano_antigo = Validate.ask('Valor do plano antigo: ', 'Por favor, informe o valor do plano antigo!', infos_extras_infos, valores )

        if type(planos[plano_antigo]) == str:
            plano_antigo    = Plano( planos[plano_antigo], plano_antigo )
        elif type(planos[plano_antigo]) == list:
            for id, plano in enumerate(planos[plano_antigo]):
                planos_str.write(f'[ {id} ] - {plano}')
                avaliable_choices.append( str(id) )

            infos_extras_infos = infos.__str__() + planos_str.__str__()

            plano_antigo_id = int(Validate.ask('Plano antigo: ', 'Por favor, informe o plano antigo!', infos_extras_infos, avaliable_choices ))
            plano_antigo    = Plano( planos[plano_antigo][plano_antigo_id], plano_antigo )

        infos.write(f"Plano antigo │ {plano_antigo.nome}")
        infos_extras_infos = infos.__str__() + valores_str.__str__()

        plano_novo = Validate.ask('Valor do plano novo: ', 'Por favor, informe o valor do plano novo!', infos_extras_infos, valores )
        
        planos_str.clear_data()
        planos_str.new_line()

        if type(planos[plano_novo]) == str:
            plano_novo    = Plano( planos[plano_novo], plano_novo )
        elif type(planos[plano_novo]) == list:
            for id, plano in enumerate(planos[plano_novo]):
                planos_str.write(f'[ {id} ] - {plano}')
                avaliable_choices.append( str(id) )
        
            infos_extras_infos = infos.__str__() + planos_str.__str__()
            plano_novo_id = int(Validate.ask('Plano novo: ', 'Por favor, informe o valor do plano novo!', infos_extras_infos, avaliable_choices ))
            plano_novo    = Plano( planos[plano_novo][plano_novo_id], plano_novo )

        diferença = float(plano_novo.valor) - float(plano_antigo.valor)

        situação = f'Upgrade' if diferença > 0 else f'Downgrade'
        situação = f'Fidelização/upgrade' if plano_novo.valor == plano_antigo.valor else situação

        comissão = f'{Formatar.moeda(abs(diferença))}' if diferença > 0  else False
        comissão = f'{Formatar.moeda(abs(5))}' if diferença == 0 else comissão

        infos.write(f"Plano novo   │ {plano_novo.nome}" )
        infos.write(f'Situação     │ {situação}')
        infos.write(f'───────────────────────────────────')
        infos.write(f'Comissão     │ {comissão}' if comissão else '')

        extra_infos.new_line()
        extra_infos.insert_division('Vencimentos disponíveis', 'left', width=50, new_line=2)
        for vencimento in vencimentos: extra_infos.write( f'{vencimento}', jump_line=False)
        extra_infos.new_line()

        vencimento = Validate.ask('Vencimento do cliente: ', 'Por favor, informe algum dos vencimento disponíveis!', str(infos) + str(extra_infos), vencimentos)

        mes_fatura = Validate.ask(f'Informe o mês da fatura: \n{vencimento} de', 'Por favor, informe de qual mês é cobrança!', str(infos) + str(meses_str), meses).capitalize() # não faz diferença se for número, é uma string da mesma forma
        
        divisoria = '/' if len(mes_fatura) == 2 else ' de '
        vencimento_fatura = f'{str(vencimento).zfill(2)}{divisoria}{mes_fatura}'

        infos.write(f'Vencimento   │ {vencimento_fatura}')
        feito_por_chat = Validate.confirm('Feito por chat: ', infos )

        feito_por_chat = 'chat' if feito_por_chat else 'ligação'
        infos.write(f'Feito por    │ {feito_por_chat.capitalize()}')
        
        mensagem_atendimento = f'Cliente entrou em contato solicitando {situação.lower()} do plano {plano_antigo.nome} para o plano {plano_novo.nome}. Ciente da renovação do contrato por +12 meses, feito por {feito_por_chat}.'

        infos.new_line()
        infos.insert_division('Atendimento', 'left', width=40, color=Color(content_color='green'))
        
        infos.write(mensagem_atendimento, jump_line=False)

        relatorios.show_extra_notes(extra_notes)    
        infos.show()
        informações_extras = infos.extra_info(retornar=True)
        mensagem_atendimento += informações_extras

        infos.show()
        copy(mensagem_atendimento)
        relatorios.sucess_message()

    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()
