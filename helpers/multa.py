from core.Informations  import Informations, Color
from core.Validate      import Validate
from core.Formatar      import Formatar
from helpers            import relatorios
from pyperclip          import copy

red_text = Color(content_color='red')


def multa():
    try:
        calculo_multa = '(valor_plano * meses faltantes) / 30%'
        infos = Informations()
        valores_disponiveis = Informations()

        valores_disponiveis.write('Valores dos planos:', new_line=1)
        valores_planos = [ '69.90', '84.90', '99.90', '129.90', '149.90' ]
        for valor in valores_planos: valores_disponiveis.write(f'{Formatar.moeda(valor)}', jump_line=False)

        valores_disponiveis.new_line()
        infos.show()
        valores_disponiveis.show( clear=False )

        infos.insert_division('CÁLCULO MULTA', color=red_text, align='left')
        valor_plano = Validate.ask('Valor do plano', 'Por favor, informe o valor do plano!', str(infos) + str(valores_disponiveis), valores_planos)
        valor_plano = float(valor_plano)

        infos.write(f'Cálculo: {calculo_multa}', new_line=1)
        infos.write(f'Valor do plano: {Formatar.moeda(valor_plano)}', new_line=1)
        qtd_meses_faltantes = Validate.ask('Meses para o fim da fidelização', 'Por favor, informe algo!', infos)
        qtd_meses_faltantes = int(qtd_meses_faltantes)

        multa = Formatar.moeda((valor_plano * qtd_meses_faltantes) * 30 / 100)
        
        infos.write(f'Meses para completar 1 ano: {qtd_meses_faltantes} meses')
        infos.write(f'Valor da multa: {multa}', new_line=1)
        infos.write('Mensagem copiada para área de transferência!')

        copy(f'Ainda restam {qtd_meses_faltantes} com isso, há uma multa no valor de {multa}')
        infos.show()
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()