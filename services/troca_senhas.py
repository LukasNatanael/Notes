from core.Informations  import Informations, Color
from core.Validate      import Validate
from core.Formatar      import Formatar
from pyperclip          import copy
from helpers            import relatorios

green_text = Color(content_color='green')

def senha_central(notes:dict={}):
    try:
        infos = Informations()
        infos.insert_division('Alterar senha da Central do Assinante', color=green_text)

        infos.clear_screen()

        cadastro = notes.get('Cadastro')
        if cadastro:
            infos.write(f'Cliente: {cadastro}')
            
        CPF = Validate.ask('Qual o CPF do cliente: ', 'Por favor, informe o CPF do cliente!', infos)
        CPF = Formatar.numeros(CPF)
        infos.write(f'CPF do cliente: {CPF}', new_line=1)

        atendimento = f'Cliente entrou em contato solicitando alteração da senha da Central do Assinante. Alterado para o CPF somente os números: {CPF} e orientado a alterar a senha posteriormente por questões de segurança.'
        
        infos.new_line()
        infos.insert_division('Atendimento', 'left', color=green_text, width=35, new_line=1)
        infos.write(atendimento, new_line=1, jump_line=False)

        infos.show()
        copy(atendimento)
        relatorios.sucess_message()
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()

def senha_wifi(notes:dict={}):
    try:
        infos = Informations()
        message = f'Cliente entrou em contato solicitando troca '

        infos.insert_division('Alteração de dados Wi-Fi', new_line=1, color=green_text)

        cadastro = notes.get('Cadastro')
        if cadastro:
            infos.write(f'Cliente: {cadastro}')

        infos.show()
        rede  = input('Nome da rede: ')
        senha = input('Senha: ')

        if rede != '' or senha != '':
            infos.write(f'Rede Wi-Fi: { rede if rede   != "" else "Não alterada" }', new_line=1)
            infos.write(f'Senha:      { senha if senha != "" else "Não alterada" }')

            if (rede != '' and senha == ''):
                dados = f'do nome da rede para: {rede}'
            elif (rede == '' and senha != ''):
                dados = f'da senha da rede para: {senha}'
            elif (rede != '' and senha != ''):
                dados = f'do nome da rede e senha para: \nRede Wi-Fi: {rede} \nSenha: {senha}'
            else:
                message += 'dos dados Wi-Fi mas, não os informou.'
                dados = ''

            message += dados

            infos.new_line()
            infos.insert_division('Atendimento', 'left', color=green_text, width=35, new_line=1)
            infos.write(message, new_line=1, jump_line=False)

            # infos.write(message, new_line=1)
            infos.show()

            if dados != '':
                copy( message )
                relatorios.sucess_message()
        else:
            relatorios.error_message('Nenhum dado informado!')

    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except Exception as e:
        relatorios.error_message(f'Erro: {e}')
        input()