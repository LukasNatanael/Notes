from helpers.colored_text import colored_text
class Cobranca:

    def ultimo_cliente(self):
        return self.dados_clientes[-1]
    
    def total_contatos(self):
        soma = 0
        for cliente in self.dados_clientes:
            contatos = cliente.contatos.split('||')
            soma += len(contatos)
        return soma

    def contatos_formatados(self, contatos, infos, add_total=False):
        from core.Formatar import Formatar

        contatos = contatos.split('||')
        infos.write(f'Contatos:')

        for id, contato in enumerate(contatos): 
            contatos[id] = Formatar.contato(contato)
            infos.write(f'    {contatos[id]}')

        if add_total:
            # adicionar no log_clientes apenas
            infos.write(f'Total de contatos: {len(contatos)}', new_line=1)

    def estatisticas(self):
        from core.Informations import Color

        total_contatos = self.total_contatos()
        self.log_clientes.new_line()
        self.log_clientes.insert_division('Estatísticas', color=Color(content_color='green'), new_line=1, width=50)
        self.log_clientes.write(f'Soma de contatos: {total_contatos} | Soma de tentativas: {total_contatos*2}', new_line=1)

    def __init__(self):

        from pyperclip import copy
        from collections import namedtuple
        from time import sleep
        from helpers.input_multiline  import input_multiline

        from core.Validate     import Validate
        from core.Informations import Informations, Color
        from core.Time         import Time

        atendente = 'Lucas N.'
        data = Time.data_formatada().full_date

        infos             = Informations()
        extra_infos       = Informations()
        self.log_clientes = Informations()

        Cliente = namedtuple( 'dados_cliente', [ 'nome', 'contatos', 'atendeu' ] )

        self.dados_clientes = []
        ultimo_cliente = ''

        self.log_clientes.insert_division('Cobrança', color=Color(content_color='green'))
        
        try:
            vencimento = Validate.ask('Vencimento: ', 'Por favor, informe um vencimento!', self.log_clientes)
            self.log_clientes.write(f'Vencimento: {vencimento}', new_line=1)
            self.log_clientes.new_line()

            while True:
                try:
                    # limpando dados para reutiliza-los
                    infos.clear_screen()
                    infos.clear_data()
                    extra_infos.clear_data()
                    message = ''

                    infos.insert_division('Cobrança', color=Color(content_color='green'))
                    infos.write(f'Vencimento: {vencimento}', new_line=1)

                    if ultimo_cliente != '':
                        ultimo_cliente_nome   = ultimo_cliente.nome[0:18]
                        ultimo_cliente_status = 'Sim' if ultimo_cliente.atendeu else 'Não'
                        infos.write(f'Último cliente: {ultimo_cliente_nome} | Atendeu: {ultimo_cliente_status}', new_line=1)
                    
                    cadastro = Validate.ask('Cadastro: ', 'Por favor, informe um cadastro!', infos)
                    
                    if '0000' in [ vencimento, cadastro ]:
                        self.log_clientes.show()
                        break

                    infos.write(f'Cadastro: {cadastro}', new_line=1)

                    contatos = input_multiline('Contatos:')
                    while contatos == '':
                        infos.clear_screen()
                        infos.show()
                        contatos = input_multiline('Contatos:')

                    # adiciona os contatos formatados a instancia de Informations
                    self.contatos_formatados( contatos, infos )

                    # Copia o nome do cadastro para a área de transferência com tamanho limitado
                    copy(cadastro[0:18])

                    extra_infos.write('[ 00 ] - Retirada em aberto', new_line=1)
                    extra_infos.write('[ 77 ] - Há promessa de pagamento')
                    extra_infos.write('[ 88 ] - Cliente já pagou')

                    infos_data = str(infos) + str(extra_infos)

                    cliente_atendeu = Validate.ask(f'Cliente atendeu [{colored_text("s|n", "green")}]', message_screen=infos_data, choices=['s', 'n', '00', '77', '88'])

                    não_precisa_ligar = cliente_atendeu
                    cliente_atendeu = True  if cliente_atendeu == 's' else cliente_atendeu
                    cliente_atendeu = False if cliente_atendeu in [ 'n', '00', '77', '88' ] else cliente_atendeu

                    self.dados_clientes.append( Cliente( cadastro, contatos, cliente_atendeu ) )
                    ultimo_cliente = self.ultimo_cliente()

                    if não_precisa_ligar == '00':
                        print('\nRetirada em aberto, não precisa ligar.')
                        sleep(.9)
                        continue
                    elif não_precisa_ligar == '77':
                        print('\nHá promessa de pagamento, não precisa ligar.')
                        sleep(.9)
                        continue
                    elif não_precisa_ligar == '88':
                        print('\nCliente pagou, não precisa ligar.')
                        sleep(.9)
                        continue

                    elif cliente_atendeu:
                        message = 'Entrei em contato com o cliente, '
                        realizou_pagamento = Validate.confirm('Cliente realizou o pagamento', infos)

                        message += 'o mesmo informou que já realizou o pagamento' if realizou_pagamento else ''

                        if not realizou_pagamento:
                            message += 'mas o mesmo ainda não realizou o pagamento. '
                            data_para_pagamento = Validate.confirm('Mencionou alguma data para pagamento', infos)

                            if data_para_pagamento:
                                dias_semana = [ 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo' ]
                                dia_pagamento = Validate.ask('Quando cliente irá pagar', 'Por favor, informe uma data!', infos)

                                if dia_pagamento.lower() in [ *dias_semana, 'hoje', 'amanhã']:
                                    dia_pagamento = dia_pagamento
                                else:
                                    dia_pagamento = f'dia {dia_pagamento}'

                                message += f'Informou que irá pagar {dia_pagamento}'
                            else:
                                message += 'Nenhuma data para pagamento foi informada'

                        infos.clear_screen()
                        infos.insert_division(width=50, new_line=1)
                        infos.show()
                        print(f'Mensagem: \n({atendente}) {message}. [informações extras]. {data}\n')
                        informações_extras = input('Informações extras: \n').strip().capitalize()
                        if informações_extras != '':
                            informações_extras += '. ' if '.' not in informações_extras[-1] else ''
                    else:
                        message = 'Tentei contato com o cliente mas, não obtive sucesso'
                        informações_extras = ''

                    message += '.' if '.' not in message[-1] else ''

                    message = message.strip()

                    tratativa = f'\n({atendente}) {message} {informações_extras}{data}'

                    self.log_clientes.insert_division(width=50, new_line=1)
                    self.log_clientes.write(f'Cadastro: {cadastro}', new_line=1)
                    self.contatos_formatados( contatos, self.log_clientes, add_total=True )

                    infos.show()
                    print(f'Mensagem:{tratativa}')
                    sleep(.9)
                    copy(tratativa)

                except KeyboardInterrupt:
                    continue
            self.estatisticas()
            self.log_clientes.show()
        
        except KeyboardInterrupt:
            infos.clear_screen()
            mostrar_dados = Validate.confirm('Mostrar dados', 'Encerrado cobranças!!')

            self.estatisticas()
            if mostrar_dados:
                self.log_clientes.show()

        except:
            infos.clear_screen()
            self.estatisticas()
            self.log_clientes.show()

            print('Retornando dados devido a um erro dsconhecido')
