from core.Formatar     import Formatar
from core.Validate     import Validate
from core.Informations import Informations, Color
from pyperclip         import copy
from collections       import namedtuple

def prorata():
    Prorata = namedtuple('Prorata', ['valor_integral', 'novo_valor', 'dias_utilizados', 'valor_dias_utilizados', 'promoção'] ) 
    infos   = Informations()
    valores_disponiveis = Informations()

    infos.insert_division('Prorata', new_line=1, color=Color(content_color='green'))

    valores_disponiveis.write('Valores dos planos:', new_line=1)
    valores_planos = [ '69.90', '84.90', '99.90', '129.90', '149.90' ]
    for valor in valores_planos: valores_disponiveis.write(f'{Formatar.moeda(valor)}', jump_line=False)

    valores_disponiveis.new_line()
    infos.show()
    valores_disponiveis.show( clear=False )

    try:

        while True:
            try:
                valor_plano = Validate.ask(f'Informe o valor do plano: ', 'Por favor, informe o valor do plano!', str(infos) + str(valores_disponiveis), valores_planos)
                valor_plano = float(valor_plano)
                
                infos.write(f'Valor do plano: {Formatar.moeda(valor_plano)}', new_line=1,)
                dias_prorata = Validate.ask('Quantos dias de prorata: ', 'Por favor, informe quantos dias de prorata!', infos)
                dias_prorata = int(dias_prorata)
                infos.write(f'Dias de prorata: {dias_prorata}')

                promoção = Validate.ask('[ 00 ] - Nenhuma promoção aplicada\nValor da promoção: ', 'Por favor, informe quantos dias de prorata!',  infos)
                promoção = float(promoção)

                break
            except ValueError:
                infos.clear_data()
                infos.insert_division('Prorata', new_line=1, color=Color(content_color='green'))
                continue

        promoção = 0 if promoção == '00' else float(promoção)

        prorata = (valor_plano / 30) * dias_prorata + float(promoção)
        infos.write(f'Prorata:  {Formatar.moeda(prorata)}')
        infos.write(f'Promoção: {Formatar.moeda(promoção)}')

        infos.show()

        prorata = Prorata( 
            valor_integral        = Formatar.moeda(valor_plano),
            novo_valor            = Formatar.moeda( valor_plano + prorata ),
            dias_utilizados       = dias_prorata,
            valor_dias_utilizados = Formatar.moeda(prorata),
            promoção              = Formatar.moeda(promoção)
        )

        mensagem_cliente = f'O valor de {prorata.novo_valor} é referente a uma prorata de {prorata.dias_utilizados} dias utilizados({prorata.valor_dias_utilizados}) desde a instalação da sua rede. Nas faturas seguintes o valor do plano virá integral: {prorata.valor_integral}.'

        infos.new_line()
        infos.insert_division( 'Mensagem para o cliente:', align = 'left', color = Color(content_color='green'), width=40 )
        infos.write(mensagem_cliente, new_line=1)

        copy(mensagem_cliente)

    except:
        infos.clear_screen()
        infos.clear_data()
        infos.insert_division('Erro ao calcular prorata', color=Color('red', 'red'))

    infos.show()