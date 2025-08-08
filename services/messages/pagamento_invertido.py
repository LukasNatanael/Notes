from core.Informations  import Informations, Color
from core.Validate      import Validate
from helpers            import relatorios
from pyperclip          import copy
green_text = Color(content_color='green')


def pagamento_invertido():
    try:
        infos = Informations()
        infos.insert_division('Pagamento invertido', color=green_text)

        dia_pago = Validate.ask('Vencimento pago: ', 'Por favor, informe o vencimento pago!', infos)
        infos.write(f'Vencimento pago: {dia_pago}', new_line=1)

        infos.clear_screen()
        em_aberto = Validate.ask('Fatura em aberto: ', 'Por favor, informe o qual fatura ficou em aberto!', infos)
        infos.write(f'Vencimento em aberto: {em_aberto}')

        message = f'Pelo que verifiquei no sistema, aparentemente ocorreu um pagamento invertido, você pagou a fatura com o vencimento {dia_pago} e o vencimento {em_aberto} ficou em aberto. Você teria algum prazo para estar realizando o pagamento correto da fatura ? \nCaso queira posso inverter o vencimento da mesma.'

        infos.show()
        copy(message)
        print(message)
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()