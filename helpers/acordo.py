from core.Informations  import Informations, Color
from core.Validate      import Validate
from helpers            import relatorios
from pyperclip          import copy

green_text = Color(content_color='green')

def acordo():
    try:
        infos = Informations()
        valor_equipamento = 'R$600,00'

        infos.insert_division('Acordo', color=green_text)

        qtd_faturas = Validate.ask('Quantidade de mensalidades em aberto', 'Por favor, informe a quantidade de mensalidades em aberto!', infos)
        infos.write(f'Mensalidades em aberto: {qtd_faturas}', new_line=1)
        
        total_parcelado = Validate.ask('Valor total parcelado em 6x: ', 'Por favor, informe o valor total parcelado em 6x!', infos)
        infos.write(f'Valor parcelado: {total_parcelado}')

        total_a_vista = Validate.ask('Valor total à vista: ', 'Por favor, informe o valor total à vista!', infos)
        infos.write(f'Valor à vista:   {total_a_vista}')
        infos.new_line()

        equipamentos_lançados = Validate.confirm('Equipamentos lançados em conta', infos)

        message = f'Pelo que verifiquei, no cadastro constam {qtd_faturas} faturas em aberto, com o valor total de {total_parcelado} conseguimos fazer esse valor em até 6x no cartão de crédito, ou o valor de {total_a_vista} a vista. '
        
        if equipamentos_lançados:
            message += f'Há uma fatura no valor de {valor_equipamento}, essa fatura é referente aos equipamentos(roteador em modem). Os devolvendo esse valor será retirado de sua conta.'

        infos.insert_division('Mensagem', width=50, align='left', color=green_text, new_line=2)
        infos.write(message)

        infos.show()
        copy(message)
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()