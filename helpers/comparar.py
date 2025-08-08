from core.Informations import Informations, Color
from core.Validate     import Validate
from core.Limpar       import Limpar
from helpers           import relatorios

green_text = Color(content_color='green')

def comparar():
    from colorama import Fore, Style
    infos = Informations()

    try:
        infos.insert_division('Comparador', color=green_text)

        valor1 = Validate.ask('Informe o 1º valor', 'Por favor, informe o primeiro valor!', infos)
        infos.write(f'1º valor: {valor1}', new_line=1)
        valor1 = Limpar.personalizado(valor1, strict=True)

        valor2 = Validate.ask('Informe o 2º valor', 'Por favor, informe o segundo valor!', infos)
        infos.write(f'2º valor: {valor2}')
        valor2 = Limpar.personalizado(valor2, strict=True)


        comparacao_formatada = ''
        max_len = max(len(valor1), len(valor2))

        for i in range(max_len):
            char1 = valor1[i] if i < len(valor1) else ''
            char2 = valor2[i] if i < len(valor2) else ''

            if char1 == char2:
                comparacao_formatada += f'{char1}'
            else:
                comparacao_formatada += f'{Fore.RED}{char2 or "_"}{Style.RESET_ALL}'

        infos.new_line()
        infos.insert_division('Resultado', color=Color(content_color='green'), new_line=1, width=50, align='left')
        infos.write(valor1, new_line=1)
        infos.write(comparacao_formatada)
        infos.show()
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()