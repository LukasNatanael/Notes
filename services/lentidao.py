from core.Informations import Informations, Color
from core.Validate     import Validate
from core.Formatar     import Formatar
from core.Device       import Device
from helpers           import relatorios

from pyperclip         import copy
from collections       import namedtuple

green_text = Color(content_color='green')

def lentidao(notes:dict = {}, extra_notes:list = []):
    try:
        from core.Menu   import Menu, MenuOptions

        infos       = Informations()
        extra_infos = Informations()

        lista_serviços     = [ 'Lentidão', 'Oscilação', 'Quedas' ]
        lista_dispositivos = [ 'Cabeados e Wi-Fi', 'Wi-Fi', 'Cabeados']
        lista_quedas       = [ 'Sem quedas', 'Algumas quedas', 'Muitas quedas', 'Alguns reinicios' ]
        lista_reiniciado   = [ 'Ambos aparelhos reiniciados', 'Reiniciado somente o modem', 'Reiniciado somente roteador', 'Nenhum aparelho reiniciado' ]

        lista_procedimentos = [ 'Alterado largura e canal', 'Alterado somente largura', 'Alterado somente canal', 'Sem acesso remoto ao roteador', 'Nenhum procedimento foi realizado' ]

        Informações = namedtuple( 'Informações', [ 'serviço', 'dispositivos_que_apresentam_falhas', 'luz_ONU', 'aparelho_autenticando', 'quedas' ] )

        Dados = namedtuple('Dados_Serviço', [
            'contato', 'serviço', 
            'dispositivo_em_que_ocorre',
            'luz_ONU', 'dispositivo', 'configuração' 
        ])

        notes_data = Dados( notes.get('Contato'),  notes.get('Serviço'), notes.get('dispositivo_em_que_ocorre'), notes.get('Luz ONU'), notes.get('Dispositivo'), notes.get('Configuração') )


        # ──────────────────── Menus ────────────────────

        menu_serviços = Menu(
            MenuOptions( 'Serviço', lista_serviços )
        )

        menu_dispositivos  = Menu(
            MenuOptions( 'Em quais dispositivos isso ocorre', lista_dispositivos, lastOption='Voltar' )
        )

        menu_quedas = Menu(
            MenuOptions( 'Quedas recentes', lista_quedas, lastOption='Voltar' )
        ) 

        menu_aparelhos_reiniciados = Menu(
            MenuOptions( 'Aparelhos reiniciados', lista_reiniciado, lastOption='Voltar' ),
        )

        menu_procedimentos = Menu(
            MenuOptions('Procedimentos realizados', lista_procedimentos, lastOption='Voltar')
        )

        # ──────────────────────────────────────────────

        serviço = notes_data.serviço
        if not serviço:
            menu_serviços.show()
            serviço = menu_serviços.choseOption[0]
            serviço = lista_serviços[serviço]
            
        dispositivo_em_que_ocorre = notes_data.dispositivo_em_que_ocorre

        if not dispositivo_em_que_ocorre:
            menu_dispositivos.show()
            dispositivo_em_que_ocorre = menu_dispositivos.choseOption[0]
            dispositivo_em_que_ocorre = lista_dispositivos[dispositivo_em_que_ocorre]
            

        infos.insert_division(f'Dificuldade relatada: {serviço}', color=green_text)
        infos.write(f'{serviço} ocorre em dispositivos: {dispositivo_em_que_ocorre}', new_line=1)

        extra_infos.write('[ 00 ] Não foi possível verificar a luz', new_line=1, jump_line=False)

        # infos.clear_screen()
        luz_ONU = notes_data.luz_ONU or Validate.ask('Luz ONU: ', 'Por favor informe a luz da ONU!', str(infos) + str(extra_infos))

        if luz_ONU == '00':
            # luz_ONU = 'Não foi possível verificar a luz do modem.'
            luz_ONU = False
            infos.write('Luz ONU: n/a')
        else:
            luz_ONU = Formatar.luz_ONU(luz_ONU)
            infos.write(f'Luz ONU: {luz_ONU}')
            
        aparelho_autenticando = notes_data.dispositivo
        dispositivo = aparelho_autenticando
        configuração = notes_data.configuração

        if not aparelho_autenticando:
            aparelho_autenticando = Device.interactive( return_data=True )
            dispositivo  = f'{aparelho_autenticando.type}{aparelho_autenticando.model}'
            dispositivo  = dispositivo.replace('Fiberhome')
            configuração = aparelho_autenticando.config

        infos.write(f'Autenticando: {dispositivo}'  if dispositivo else 'Autenticando: n/a')
        infos.write(f'Configuração: {configuração}' if configuração else '')

        dispositivo = f'{dispositivo} autenticando' if dispositivo else False
        dispositivo = 'Não foi possível verificar quem está autenticando.' if not dispositivo else dispositivo

        dispositivo += '' if 'ONU' in dispositivo else '.'


        luz_ONU = f'com {luz_ONU} em sistema.'     if ( 'ONU' in dispositivo and luz_ONU) else luz_ONU
        luz_ONU = f'ONU com {luz_ONU} em sistema.' if ( 'ONU' not in dispositivo and luz_ONU) else luz_ONU

        luz_ONU = 'Sem acesso a ONU para verificar luz.' if not luz_ONU  else luz_ONU
        luz_ONU = 'Sem acesso a ONU para verificar luz.' if ( not luz_ONU and not dispositivo ) else luz_ONU

        infos.show()
        
        menu_quedas.show()

        quedas = menu_quedas.choseOption[0]
        quedas = lista_quedas[quedas]

        infos.write(f'Quedas: {quedas}')

        menu_aparelhos_reiniciados.show()

        aparelhos_reiniciados = lista_reiniciado[menu_aparelhos_reiniciados.choseOption[0]]
        aparelhos_reiniciados = f'{aparelhos_reiniciados}'.lower()

        if aparelhos_reiniciados == 'ambos aparelhos reiniciados':
            aparelhos_reiniciados = 'reiniciado aparelhos'

        if 'ONU' in aparelho_autenticando:
            menu_procedimentos.show()
            procimentos = menu_procedimentos.choseOption[0]
            procimentos = lista_procedimentos[procimentos]
            
            aparelhos_reiniciados = 'Reiniciado somente ONU' if procimentos == 'Sem acesso remoto ao roteador' else aparelhos_reiniciados
            
            if procimentos == 'Nenhum procedimento foi realizado':
                procimentos = ''
            else:
                procimentos = f'{procimentos} e {aparelhos_reiniciados}.' if procimentos != 'Sem acesso remoto ao roteador' else f'{aparelhos_reiniciados}. Sem acesso remoto ao roteador.'
        else:
            procimentos = ''

        infos.new_line()

        dados = Informações( serviço.lower(), dispositivo_em_que_ocorre.lower(), luz_ONU, dispositivo, quedas )

        atendimento = f'Cliente entrou em contato alegando {dados.serviço} na rede. De acordo com o mesmo isso ocorre em aparelhos {dados.dispositivos_que_apresentam_falhas}. {dados.aparelho_autenticando} {dados.luz_ONU} {dados.quedas} recentes em extrato. {procimentos}'.strip().replace('wi-fi','Wi-Fi')

        infos.insert_division('Atendimento', color=green_text, new_line=1, width=50, align='left')
        infos.write(atendimento, jump_line=False)

        relatorios.show_extra_notes(extra_notes)
        infos.show( clear=False )
        informações_extras = infos.extra_info()

        resolvido = Validate.confirm('\nFoi resolvido', infos)

        if resolvido:
            testou = Validate.confirm('Cliente conseguiu testar no momento', infos)
            conclusão = 'Cliente informou que de momento o problema foi solucionado.' if testou else 'Cliente não pode testar no momento, fará isso posteriormente.'

            conclusão = f'{atendimento} {conclusão} Orientado o mesmo a acompanhar a rede no decorrer do dia e retornar contato caso necessário.'
        else:

            falta_contato = Validate.confirm('Finalizado por falta de contato', infos)

            if falta_contato:
                conclusão = 'Como cliente não manteve mais contato, o atendimento foi finalizado.'
                conclusão = f'{atendimento} {conclusão}'
            else:
                contato = notes_data.contato or Validate.ask('Contato do cliente: ', 'Por favor, informe o contato do cliente!', infos)
                contato = Formatar.contato(contato)

                conclusão = 'Como mesmo após os procedimentos não houve uma melhora, verificar diretamente no local por gentileza. Ligar com antecedência.' if procimentos else 'Verificar diretamente no local por gentileza. Ligar com antecedência.'

                conclusão = f'Contato: {contato} \n{atendimento} {conclusão}'

        conclusão += f'{informações_extras}'

        infos.show()
        copy(conclusão)
        
        relatorios.sucess_message()
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()
