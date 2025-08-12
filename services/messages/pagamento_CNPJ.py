'''
Bom dia, cliente pagou no CNPJ  pois, sua fatura não havia sido registrada. Dar baixa por gentileza, agradeço desde já!
Cadastro: {cadastro}
Cód. Cobrança: {cod_cobranca}
'''
from core.Validate     import Validate
from core.Informations import Informations, Color
from core.Time         import Time
from pyperclip         import copy

green_text = Color( content_color='green' )
yellow_text = Color( content_color='yellow' )

def cnpj():
    infos = Informations()

    infos.insert_division(color=green_text, title='Pagamento no CNPJ')

    cadastro     = Validate.ask('Cadastro', 'Por favor, informe o cadastro do cliente!', infos)
    infos.write(f'Cadastro: {cadastro}', new_line=1)

    cod_cobranca = Validate.ask('Cód. Cobrança', 'Por favor, informe o código da cobrança!', infos)
    infos.write(f'Cód. Cobrança: {cod_cobranca}')

    horario = int(Time.hora_formatada().horas)

    if horario <= 11:
        saudacao = 'Bom dia'
    elif horario < 17:
        saudacao = 'Boa tarde'
    else:
        saudacao = 'Boa noite'


    message = f'{saudacao}, cliente pagou no CNPJ pois, sua fatura não havia sido registrada. Dar baixa por gentileza, agradeço desde já!\nCadastro: {cadastro}\nCód. Cobrança: {cod_cobranca}'

    infos.write(message, new_line=1)
    infos.new_line()

    infos.insert_division('Não esqueça de marcar a responsável', width=50, color=yellow_text)

    infos.show()
    copy(message)