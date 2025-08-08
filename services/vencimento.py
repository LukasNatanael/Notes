from core.Informations import Informations, Color
from core.Validate     import Validate
from core.Formatar     import Formatar
from helpers           import relatorios

from pyperclip         import copy
from collections       import namedtuple
from time              import sleep

green_text = Color(content_color='green')

def vencimento( notes:dict = {}, extra_notes:list = [] ):
    try:
        from colorama import Fore, Style

        infos      = Informations()
        extra_info = Informations()

        Dados = namedtuple('Dados_Serviço', [ 'valor_plano', 'vencimento_atual', 'vencimento_novo' ])
        notes_data = Dados(notes.get('valor_plano'), notes.get('vencimento_atual'), notes.get('vencimento_novo'))

        infos.clear_screen()
        vencimentos    = [ '5', '10', '15', '20', '25' ]
        valores_planos = [ '69.90', '84.90', '99.90', '129.90', '149.90' ]
        meses = [ 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro' ]

        infos.insert_division('Alteração de vencimento', color=green_text)
        extra_info.insert_division('Alteração de vencimento', new_line=2)

        extra_info.write('Valores dos planos: ')
        for valor in valores_planos: extra_info.write(f'{Formatar.moeda(valor)}', jump_line=False)

        extra_info.new_line()

        infos.clear_screen()
        valor_plano = notes_data.valor_plano or Validate.ask('Informe o valor do plano: ', 'Por favor, informe algum dos valores disponíveis!', extra_info, valores_planos)
        valor_plano = float(valor_plano)

        infos.write(f'Valor do plano: {Formatar.moeda(valor_plano)}', new_line=1)

        extra_info.clear_data()
        extra_info.write('Vencimentos disponíveis: ', new_line=1)
        for vencimento in vencimentos: extra_info.write(f'{vencimento}', jump_line=False)
        extra_info.new_line()

        infos.clear_screen()  
        vencimento_atual = notes_data.vencimento_atual or Validate.ask('Vencimento atual: ', 'Por favor, informe algum dos vencimento disponíveis!', str(infos) + str(extra_info), vencimentos)
        vencimento_atual = int(vencimento_atual)

        infos.write(f'Vencimento atual: { str(vencimento_atual).zfill(2) }', new_line=1)

        infos.clear_screen()
        vencimento_novo = notes_data.vencimento_novo or Validate.ask('Vencimento novo: ', 'Por favor, informe algum dos vencimento disponíveis!', str(infos) + str(extra_info), vencimentos)
        vencimento_novo = int(vencimento_novo)

        infos.write(f'Vencimento novo:  {vencimento_novo}')
        infos.new_line(1)

        infos.insert_division(width=30)

        dias_prorata = vencimento_atual - vencimento_novo
        diferença = dias_prorata

        dias_utilizados = f'{abs(dias_prorata)} dias utilizados' if ( dias_prorata ) < 0 else f'{abs(dias_prorata)} dias não utilizados'

        infos.write(f'Diferença: {dias_utilizados}', new_line=1)

        situação = f'Acréscimo' if ( dias_prorata ) < 0 else f'Desconto'

        if situação == 'Acréscimo':
            dias_prorata = abs(valor_plano/30*dias_prorata)
            novo_valor_plano = valor_plano + dias_prorata 
        elif situação == 'Desconto':
            dias_prorata = abs(valor_plano/30*dias_prorata)
            novo_valor_plano =  valor_plano - dias_prorata 

        situação_colorida = f'{Fore.RED}Acréscimo{Style.RESET_ALL}' if ( diferença ) < 0 else f'{Fore.GREEN}Desconto{Style.RESET_ALL}'

        infos.clear_screen()
        mes_do_proporcional = Validate.ask('O proporcional virá em qual mês: ', 'Por favor, informe em qual mês o proporcional virá!', infos, meses).capitalize()

        infos.write(f'{situação_colorida} de {Formatar.moeda(dias_prorata)}({dias_utilizados})', jump_line=2)
        infos.write(f'Valor da fatura em {mes_do_proporcional}: {Formatar.moeda(novo_valor_plano)}', jump_line=1)

        local_atendimento = Validate.confirm('Feito por chat: ', infos)

        local_atendimento = 'Feito por chat' if local_atendimento else 'Feito por ligação'
        infos.write(local_atendimento, jump_line=2)

        infos.insert_division(new_line=1)

        infos.show()

        mensagem_para_cliente = f'Devido a alteração de vencimento do dia {vencimento_atual} para o dia {vencimento_novo} haverá um {situação.lower()} de {Formatar.moeda(dias_prorata)}({dias_utilizados}) na sua fatura de {mes_do_proporcional}, totalizando em {Formatar.moeda(novo_valor_plano)}, após isso o valor do plano voltará ao normal: {Formatar.moeda(valor_plano)}. Tudo bem ?' 

        motivo_alteração_valor = f'{situação} de {Formatar.moeda(dias_prorata)}({dias_utilizados}) devido a alteração do vencimento do dia {vencimento_atual} para o dia {vencimento_novo}.'

        mensagem_atendimento = f'Cliente entrou em contato solicitando uma alteração de vencimento do dia {vencimento_atual} para o dia {vencimento_novo}. Ciente do {situação.lower()} de {Formatar.moeda(dias_prorata)}({dias_utilizados}) na sua fatura de {mes_do_proporcional}. {local_atendimento}.'


        infos.write(f'{Fore.GREEN}Mensagem para o cliente:{Style.RESET_ALL}', new_line=1)
        infos.write( mensagem_para_cliente )

        infos.write(f'{Fore.GREEN}Motivo do {situação.lower()}:{Style.RESET_ALL}', new_line=1)
        infos.write(motivo_alteração_valor)

        infos.write(f'{Fore.GREEN}Descrição do atendimento:{Style.RESET_ALL}', new_line=1)
        infos.write(mensagem_atendimento)

        infos.show()

        copy(mensagem_atendimento)
        sleep(1)
        copy(motivo_alteração_valor)
        sleep(1)
        copy(mensagem_para_cliente)

        relatorios.sucess_message()
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()
        
