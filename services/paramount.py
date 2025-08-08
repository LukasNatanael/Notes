from core.Informations  import Informations, Color
from core.Validate      import Validate
from core.Formatar      import Formatar
from pyperclip          import copy
from time               import sleep
from helpers            import relatorios
from collections        import namedtuple

green_text = Color( content_color='green' )

def paramount(notes:dict):
    try:
        Dados = namedtuple('Dados_Serviço', [ 'cadastro', 'contato', 'email' ])
        client_data = Dados( notes.get('Nome'), notes.get('Contato'), notes.get('email') )

        infos = Informations()
        infos.insert_division('Ativação Neo Vantagens', color=green_text)

        if client_data.cadastro:
            infos.write(f'Cadastro: {client_data.cadastro}', new_line=1)
        else:
            infos.new_line()

        email   = client_data.email or Validate.ask('Informe o e-mail do cliente', 'Por favor, informe e-mail do cliente!', infos).lower()
        infos.write(f'E-mail:   {email}')

        contato = client_data.contato or Validate.ask('Informe o contato do cliente', 'Por favor, informe contato do cliente!', infos)
        contato = Formatar.contato(contato)
        infos.write(f'Contato:  {contato}')

        paramount_ativo = Validate.confirm('Cliente já possui Paramount+ ativo', infos)

        if paramount_ativo:
            message = f'''Pelo que verifiquei, *já possui uma conta ativa em seu cadastro* com o e-mail: {email} cadastrado.
Caso tenha perdido acesso a conta, *peço que tente recuperar seus dados diretamente pelo site da Watch Brasil ou Paramount+*

Basta acessar algum dos sites abaixo:

[ Paramount+ ]
https://www.paramountplus.com/br/account/forgotpassword

[ Watch Brasil ]
https://play.watch.tv.br/login/esqueci-minha-senha

Basta inserir seu e-mail na caixa de texto e aguardar até que um e-mail de recuperação de senha seja enviado para você.'''
            print(f'\n{message}')
            copy(message)
            
        else:
            infos.show()
            message = 'Ativação Paramount+'
            
            print(message)
            copy(message)
            sleep(1)
            copy('Lucas Natanael Moreira Batista')
            print('\nNome do atendente copiado para a área de transferência\n')
            input('Pressione alguma tecla quando desejar continuar...')

            infos.show()
            relatorios.sucess_message()
    except KeyboardInterrupt:
        relatorios.error_message()
    except:
        relatorios.error_message()

