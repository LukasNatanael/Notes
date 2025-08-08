from core.Informations import Informations, Color
from core.Validate     import Validate
from core.Device       import Device
from core.Formatar     import Formatar
from helpers           import relatorios

from pyperclip         import copy
from collections       import namedtuple

red_text   = Color(content_color='red')
green_text = Color(content_color='green')


def roteador_bugado( notes:dict = {}, extra_notes:list = [] ):
    try:

        infos       = Informations()
        extra_infos = Informations()

        Dados = namedtuple( 'Dados_Serviço', [ 'cadastro', 'contato', 'taxa', 'local_atendimento' ] )
        notes_data = Dados( notes.get('Nome'), notes.get('Contato'))

        infos.insert_division('Sem acesso - Roteador bugado', color=red_text)

        cadastro = notes_data.cadastro or Validate.ask('Cadastro: ', 'Por favor, informe um cadastro!', infos)
        infos.write(f'Cadastro: {cadastro}', new_line=1)
        
        contato  = notes_data.contato or Validate.ask('Contato: ', 'Por favor, informe o contato do cliente!', infos)
        contato = Formatar.contato(contato)
        infos.write(f'Contato: {contato}')
        
        rede   = Validate.confirm('Nome da rede aparece normalmente', infos)
        rede = 'Nome da rede aparece normalmente' if rede else 'Nome da rede não aparece'

        infos.write(f'Wi-Fi: {rede}', new_line=1)
        extra_infos.new_line()
        extra_infos.insert_division()

        online = Validate.confirm('ONU online', str(infos) + str(extra_infos))
        online = 'ONU consta como ONLINE' if online else 'ONU consta como OFFLINE'

        roteador = Device.interactive( return_data=True )
        roteador = roteador.tipo + roteador.modelo

        infos.write(f'Roteador: {roteador}')
        infos.new_line()
        extra_infos.insert_division()

        atendimento = f'Cliente entrou em contato alegando estar sem acesso. {roteador} autenticando, {rede.lower()} e no sistema {online}. Cabos conectados corretamente, removido MAC, cabo da WAN, reiniciado aparelhos e conectado cabo novamente'
        
        extra_infos.clear_data()
        extra_infos.insert_division('Atendimento', width=40, color=Color(content_color='green'))
        extra_infos.write(atendimento, new_line=1)
        resolvido = Validate.confirm('Foi resolvido', str(infos) + str(extra_infos))
        
        if resolvido:
            atendimento += f'. Após isso, cliente voltou a ficar online em sistema.'
        else:
            atendimento = f'Contato: {contato} \n{atendimento}'
            atendimento += f' mas, sem sucesso. Aparentemente o roteador, está com algum conflito nas suas configurações. Verificar no local por favor. Ligar com antecedência.'

        infos.insert_division('Atendimento', width=40, color=green_text)
        infos.write(atendimento, new_line=1, jump_line=False)

        relatorios.show_extra_notes(extra_notes)
        infos.show(clear=False)

        observação_complementar = infos.extra_info()
        atendimento + observação_complementar

        infos.show()
        copy(atendimento)
    except KeyboardInterrupt:
        relatorios.error_message('Serviço finalizado pelo usuário')
    except:
        relatorios.error_message()

