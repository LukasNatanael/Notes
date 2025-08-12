from core.Informations  import Informations
from core.Validate      import Validate
from core.Formatar      import Formatar

def router( service_name:str, service_data:str, notes:dict, extra_notes:list, infos_notes:Informations ) -> None:

    type_service = service_name
    infos        = infos_notes
    alarmes      = [ 'dying', 'die', 'dying_gasp', 'los', 'link_loss', 'pon', 'link_los', 'link los' ]

    cities      = { 
        'chl':  'Conchal',
        'ara':  'Araras',
        'ec':   'Engenheiro Coelho',
        'mm':   'Mogi Mirim',
        'mg':   'Mogi Guaçu',
        'tuju': 'Tujuguaba - Conchal'
    }

    type_service = type_service.lower()
    data_service = service_data.lower()

    if type_service == 'nome':
        nome = data_service
        data_service = nome[0:25]

    elif type_service == 'contato':
        contato = data_service
        data_service =  Formatar.contato(contato)

    elif type_service == 'cidade':
        cidade = data_service
        if cidade in cities.keys():
            data_service = cities[cidade]

    elif data_service in [ *alarmes, 'sem acesso' ]:
        alarme = Validate.ask('Alarme em sistema/aparelho', message_screen=infos ,choices=alarmes) if type_service == 'sem acesso' else data_service
        
        alarme = alarme.lower()

        alarme = 'DYING_GASP'   if alarme in [ 'dying', 'die', 'dying_gasp' ]         else alarme
        alarme = 'LINK_LOSS'    if alarme in [ 'link_loss', 'link_los', 'link los' ]  else alarme
        alarme = 'LOS'          if alarme in [ 'los', 'los aceso', 'los piscando' ]   else alarme
        alarme = 'PON piscando' if alarme in [ 'pon', 'pon piscando' ]                else alarme
        
        tempo_sem_acesso = input(f'{alarme} há quanto tempo: ') if alarme in [ 'DYING_GASP', 'LINK_LOSS' ] else ''

        alarme = alarme.replace('piscando', '').strip().lower()
        data_service = f'{alarme.upper()} há {tempo_sem_acesso}' if tempo_sem_acesso else alarme
        
        notes['alarme']  = alarme
        notes['tempo_sem_acesso'] = tempo_sem_acesso 

    elif data_service in [ 'fhtt', 'mudança de endereço', 'mudança de cômodo']:
        if data_service != 'mudança de cômodo':
            cep = input('Informe o CEP: ')
            if cep:
                numero_casa = Validate.ask(f'CEP: {cep} | Nº', 'Informe o número da casa!', infos)
                extra_notes.append( f'CEP: {cep} | Nº{numero_casa}' )
                
                notes['CEP'] = Formatar.numeros(cep)
                notes['numero_casa'] = numero_casa
    
    elif data_service in ['paramount', 'watch', 'neovantagem', 'neovantagens']:
        email   = Validate.ask('E-mail', 'Por favor, informe um e-mail!', infos).lower()
        contato = notes.get('Contato') or Validate.ask('Contato', 'Por favor, informe um contato!', infos)
        
        contato = Formatar.contato(contato)
        extra_notes.append(f'E-mail: {email} | Contato: {contato} ')
        notes['email'] = email

    elif data_service in ['vencimento']:
        valores_planos   = [ '69.90', '84.90', '99.90', '129.90', '149.90' ]
        vencimentos      = [ '5', '10', '15', '20', '25' ]
        
        valor_plano      = Validate.ask('Valor do plano', 'Por favor, informe um valor válido!',        infos, valores_planos)
        vencimento_atual = Validate.ask('Vencimento atual', 'Por favor, informe um vencimento válido!', infos, vencimentos)
        vencimento_novo  = Validate.ask('Vencimento novo' , 'Por favor, informe um vencimento válido!', infos, vencimentos)

        notes['valor_plano']      =  valor_plano
        notes['vencimento_atual'] =  vencimento_atual
        notes['vencimento_novo']  =  vencimento_novo

        extra_notes.append(f'Valor do plano:   {Formatar.moeda(valor_plano)}')
        extra_notes.append(f'Vencimento atual: {vencimento_atual}')
        extra_notes.append(f'Vencimento novo:  {vencimento_novo}')

    elif data_service in [ 'lentidão', 'oscilação', 'quedas' ]:
        dispositivos = { 
            'wi-fi':    'Wi-Fi',
            'cabeados': 'Cabeados',
            'ambos':    'Cabeados e Wi-Fi'
        }
        dispositivo_em_que_ocorre = Validate.ask('Em quais dispositivos isso ocorre', message_screen=infos, choices=dispositivos.keys(), show_choices=True)

        notes['dispositivo_em_que_ocorre'] = dispositivos[dispositivo_em_que_ocorre]

    elif data_service in [ 'ponto adicional', 'adicional' ]:
        local_atendimento = Validate.confirm('Feito por chat', infos)
        taxa = Validate.confirm('Taxa de instalação', infos)
        
        notes['local_atendimento'] = local_atendimento
        notes['taxa_serviço']      = taxa

    if data_service in [ 'fhtt', 'off', *alarmes ]:
        data_service = data_service.upper()
    elif data_service in [ 'cidade' ]:
        data_service = f'{data_service[0].upper()}{data_service[1:]}'
    else:
        data_service = data_service


    if type_service not in [ 'nome', 'contato', 'cidade', 'chlnet' ]:
        notes['Serviço'] = f'{data_service[0].upper()}{data_service[1:]}'
    else:
        notes[service_name] = data_service
