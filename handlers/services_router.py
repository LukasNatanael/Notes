from core.Informations  import Informations
from core.Validate      import Validate
from core.Formatar      import Formatar

def router( service_name:str, service_data:str, notes:dict, extra_notes:list, infos_notes:Informations ) -> None:

    service_type = service_name
    infos        = infos_notes
    alarmes      = [ 'dying', 'die', 'dying_gasp', 'los', 'link_loss', 'pon' ]

    cities      = { 
        'chl':  'Conchal',
        'ara':  'Araras',
        'ec':   'Engenheiro Coelho',
        'mm':   'Mogi Mirim',
        'mg':   'Mogi Guaçu',
        'tuju': 'Tujuguaba - Conchal'
    }

    service_type = service_type.lower()
    service      = service_data

    if service_type == 'nome':
        nome = service
        notes['Nome'] = nome[0:25]

    elif service_type == 'contato':
        contato = service
        notes['Contato'] =  Formatar.contato(contato)

    elif service_type == 'cidade':
        cidade = service
        if cidade in cities.keys():
            notes['Cidade'] = cities[cidade]

    elif service in [ *alarmes, 'sem acesso' ]:
        alarme = Validate.ask('Alarme em sistema/aparelho', message_screen=infos ,choices=alarmes) if service_type == 'sem acesso' else service
        
        alarme = alarme.lower()

        alarme = 'DYING_GASP'   if alarme in [ 'dying', 'die', 'dying_gasp' ] else alarme
        alarme = 'LINK_LOSS'    if alarme in [ 'link_loss' ] else alarme
        alarme = 'LOS'          if alarme in [ 'los' ] else alarme
        alarme = 'PON piscando' if alarme == 'pon' else alarme

        tempo_sem_acesso = input(f'{alarme} há quanto tempo: ')

        alarme = alarme.replace('piscando', '').strip().lower()
        service = f'{alarme.upper()} há {tempo_sem_acesso}' if tempo_sem_acesso else alarme
        
        notes['alarme']  = alarme
        notes['tempo_sem_acesso'] = tempo_sem_acesso 

    elif service in [ 'fhtt', 'mudança de endereço', 'mudança de cômodo']:
        if service != 'mudança de cômodo':
            cep = input('Informe o CEP: ')
            if cep:
                numero_casa = Validate.ask(f'CEP: {cep} | Nº', 'Informe o número da casa!', infos)
                extra_notes.append( f'CEP: {cep} | Nº{numero_casa}' )
                
                notes['CEP'] = Formatar.numeros(cep)
                notes['numero_casa'] = numero_casa
    
    elif service in ['paramount', 'watch', 'neovantagem', 'neovantagens']:
        email   = Validate.ask('E-mail', 'Por favor, informe um e-mail!', infos).lower()
        contato = notes.get('Contato') or Validate.ask('Contato', 'Por favor, informe um contato!', infos)
        
        contato = Formatar.contato(contato)
        extra_notes.append(f'E-mail: {email} | Contato: {contato} ')
        notes['email'] = email

    elif service in ['vencimento']:
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

    elif service in [ 'lentidão', 'oscilação', 'quedas' ]:
        dispositivos = { 
            'wi-fi':    'Wi-Fi',
            'cabeados': 'Cabeados',
            'ambos':    'Cabeados e Wi-Fi'
        }
        dispositivo_em_que_ocorre = Validate.ask('Em quais dispositivos isso ocorre', message_screen=infos, choices=dispositivos.keys(), show_choices=True)

        notes['dispositivo_em_que_ocorre'] = dispositivos[dispositivo_em_que_ocorre]

    elif service in [ 'ponto adicional', 'adicional' ]:
        local_atendimento = Validate.confirm('Feito por chat', infos)
        taxa = Validate.confirm('Taxa de instalação', infos)
        
        notes['local_atendimento'] = local_atendimento
        notes['taxa_serviço']      = taxa

    service = service.upper() if service in [ 'fhtt', 'off', *alarmes ] else f'{service[0].upper()}{service[1:]}'

    if service_type not in [ 'nome', 'contato', 'cidade'  ]:
        notes['Serviço'] = service 
        

