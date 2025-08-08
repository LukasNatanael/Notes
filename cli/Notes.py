# CORE
from core.Informations  import Informations, Color
from core.Validate      import Validate
from core.Formatar      import Formatar
from core.Device        import Device

# HANDLERS
from handlers import services_router, report_router

# Externos
from time               import sleep

CLIENT_DATA     = [ 'Nome', 'Contato', 'Cidade', 'chlnet', 'Serviço' ]
EQUIPAMENT_DATA = [ 'MAC', 'IP', 'Senha', 'Serial', 'Luz ONU' ]
SERVICE_DATA    = [ 'Protocolo', 'OS' ]
EXTRA_DATA      = [ '\nAdicionar nota', 'Remover nota\n' ]

class Notes:
    def __init__(self):
        self.infos           = Informations()
        self.log_infos       = Informations()
        self.log_extra_notes = Informations()
        self.atendimento_log = Informations()

        self.notes       = {}
        self.extra_notes = []

    @property
    def info_data(self):
        return str(self.log_infos) + str(self.infos)

    def add_note( self, key:str, value:str|int|float ) -> None:
        self.notes[key] = value

    def add_extra_note( self, value:str|int|float ) -> None:
        self.extra_notes.append(value)

    def main_menu(self):
        self.infos.clear_data()

        options = [ 'Inserir dados', 'Copiar dados' ]
        valid_options = [ '0' ]
        id = 1
        self.infos.insert_division('MENU PRINCIPAL', color=Color(content_color='green'), new_line=2)

        for option in options:
            self.infos.write(f'[ {id} ] - {option}')
            valid_options.append( str(id) )
            id += 1
        self.infos.write('[ 0 ] - Finalizar')

        self.infos.new_line()
        self.infos.insert_division('Informe uma opção', color=Color(content_color='green'), width=40, align='left')
        option = Validate.ask('Escolha uma das opções acima', 'Por favor, informe uma opção válida!', self.infos, valid_options)

        self.infos.show()

        return option
    
    def menu(self, title:str, options:str, last_option:str='Voltar', notes_info:bool=False) -> str:
        self.infos.clear_data()

        valid_options = [ '0' ]
        id = 1
        green = Color(content_color='green')

        self.infos.insert_division( title, color=green, new_line=2)

        for option in options:
            if '\n' in option[0]:
                option = option.replace('\n', '')
                self.infos.write(f'\n[ {str(id).zfill(2)} ] - {option}')
            elif '\n' in option[-1]:
                option = option.replace('\n', '')
                self.infos.write(f'[ {str(id).zfill(2)} ] - {option}\n')
            else:
                self.infos.write(f'[ {str(id).zfill(2)} ] - {option}')
            valid_options.append( str(id) )
            id += 1
        self.infos.write(f'[ 00 ] - {last_option}')

        self.infos.new_line()
        self.infos.insert_division('Informe uma opção', color=green, width=40, align='left')

        if len(self.notes) != 0:
            self.display()

        info_data = str(self.log_infos) + str(self.infos) if notes_info else self.infos
        option = Validate.ask('Escolha uma das opções acima', 'Por favor, informe uma opção válida!', info_data, valid_options)

        return option
    
    def insert_all_data(self):
        all_fields = CLIENT_DATA + EQUIPAMENT_DATA+ SERVICE_DATA

        while True:
            options = { str(i+1): field for i, field in enumerate(all_fields) }
            options['0'] = 'Voltar'

            # Cria menu numerado
            menu_display = "\nPreencha um campo:\n\n"
            for key, value in options.items():
                menu_display += f"[ { str(key).zfill(2) } ] {value}\n"

            option = Validate.ask("Escolha uma opção", "Informe uma opção válida!", message_screen=menu_display, choices=list(options.keys()))

            if option == '0':
                break

            selected_field = options[option]
            current = self.notes.get(selected_field)
            prompt = f"{selected_field} (atual: {current})" if current else selected_field

            value = Validate.ask(prompt, f'Por favor, informe um(a) {selected_field.lower()}!', menu_display)
            self.notes[selected_field] = value or current

            break

    def client_data(self):
        try:
            option = self.menu('Dados do cliente', CLIENT_DATA)
            if option in '0':
                return
            input_data = CLIENT_DATA[int(option) - 1]
            info_type = Validate.ask(input_data, f'Por favor, informe um(a) {input_data.lower()}!', self.infos)
            services_router.router(input_data, info_type, self.notes, self.extra_notes, self.infos)
            
        except KeyboardInterrupt:
            return

    def equip_data(self):
        try:
            option = self.menu('Dados do equipamento', EQUIPAMENT_DATA)
            if option in '0':
                return
            input_data = EQUIPAMENT_DATA[int(option) - 1]

            info_type = Validate.ask(input_data, f'Por favor, informe um(a) {input_data.lower()}!', self.infos)
            
            if input_data == 'MAC':
                device = Device.from_mac( info_type, return_data=True )

                self.notes['Dispositivo']  = device.type + device.model 
                self.notes['Configuração'] = device.config

                if device.serial:
                    self.notes['Serial'] = device.serial
                
                info_type = device.mac
            
            elif input_data == 'Serial':
                info_type = info_type.upper()

            elif input_data == 'Luz ONU':
                info_type = Formatar.luz_ONU(info_type)

            self.notes[input_data] = info_type 
        except KeyboardInterrupt:
            return

    def service_data(self):
        try:
            option = self.menu('Dados do serviço', SERVICE_DATA)
            if option in '0':
                return
            input_data = SERVICE_DATA[int(option) - 1]
            self.notes[input_data] = Validate.ask(input_data, f'Por favor, informe um(a) {input_data.lower()}!', self.infos)
        except KeyboardInterrupt:
            return

    def add_note(self):
        try:
            self.display()
            extra_note = Validate.ask('[ | para quebra de linha ] \n\nInformação extra:', 'Por favor, informe algo!', self.log_extra_notes)
            self.extra_notes += extra_note.split('|') 
        except KeyboardInterrupt:
            return

    def remove_note(self):
        try:
            if self.extra_notes == []:
                self.infos.clear_data()
                red = Color(border_color='red', content_color='red')
                self.infos.insert_division('Nenhuma nota extra adicionada', color=red)
                self.infos.show()
                sleep(1)
                return

            valid_options = [str(i+1) for i in range(len(self.extra_notes))]
            extra_note = Validate.ask('Informe a nota que deseja remover:', 'Por favor, informe algo!', self.log_extra_notes, valid_options)
            self.extra_notes.pop(int(extra_note) - 1)
        except KeyboardInterrupt:
            return
    
    def display(self):
        self.log_infos.clear_data()
        self.log_extra_notes.clear_data()

        terminal_width = self.log_infos.terminal_size.columns
        padding_space = terminal_width - 4

        green = Color(content_color='green')

        # Define os blocos
        sections = {
            'Dados do Cliente': ['Nome', 'Contato', 'chlnet','Cidade', 'Serviço'],
            'Dados do Equipamento': ['Dispositivo', 'Configuração', 'MAC', 'IP', 'Senha', 'Serial', 'Luz ONU' ],
            'Dados do Serviço': ['Protocolo', 'OS']
        }

        self.log_infos.insert_division('Anotações ', color=green, corner_l='┌', corner_r='┐', align='center')
        self.log_infos.empty_line()

        for section, keys in sections.items():
            # Filtra os dados dessa seção
            section_data = {k: self.notes[k] for k in keys if k in self.notes and self.notes[k] != ''}
            if not section_data:
                continue

            # Título da seção
            self.log_infos.insert_division(title=section, color=green, corner_l='├', corner_r='┤', align='left')

            # Exibe os dados da seção
            for title, note in section_data.items():
                title_str = title.ljust(20)
                note_str = str(note).ljust(padding_space - 23)  # ajustando 3 do separador
                self.log_infos.insert_division(f'{title_str} │ {note_str}', corner_l='│', corner_r='│')

            self.log_infos.empty_line()

        # Informações extras
        if self.extra_notes:
            self.log_infos.insert_division('Informações extras', color=green, corner_l='├', corner_r='┤', align='left')

            self.log_extra_notes.insert_division('Informações extras', color=green, corner_l='┌', corner_r='┐', align='left')
            self.log_extra_notes.empty_line()
            
            for note in self.extra_notes:
                note = note.strip()
                if note != '':
                    note_str = note.ljust(padding_space)
                    self.log_infos.insert_division(note_str, corner_l='│', corner_r='│')
                    self.log_extra_notes.insert_division(note_str, corner_l='│', corner_r='│')

            self.log_extra_notes.empty_line()
            self.log_infos.empty_line()
            self.log_extra_notes.insert_division(corner_l='└', corner_r='┘', new_line=2)
        else:
            self.log_extra_notes.insert_division('Nenhuma informação extra adicionada')

        self.log_infos.insert_division(corner_l='└', corner_r='┘', new_line=2)
        self.log_infos.show()

    def interactive(self):
        main_menu_options = [ 'Inserir dados', 'Gerar relatório' ]

        sub_menu_options  = [ 'Dados do cliente', 'Dados do equipamento', 'Dados do serviço', *EXTRA_DATA ]

        data_handlers = {
            '1': self.client_data,
            '2': self.equip_data,
            '3': self.service_data,
            '4': self.add_note,
            '5': self.remove_note
        }
        
        while True:
            try:
                option = self.menu( 'MENU PRINCIPAL', main_menu_options, last_option='Finalizar', notes_info=True )
                if option in '0':
                    if len(self.notes) != 0:
                        self.display()
                        
                    finish = Validate.confirm('Você deseja finalizar o serviço', self.info_data)
                    if finish:
                        self.display()
                        break

                ## para exibir o menu da forma antiga utilizando o insert_all_data()
                # elif option == '1':
                #     self.insert_all_data()

                elif option == '1':
                    while True:
                        try:
                            option = self.menu( 'Selecionar tipo de dado', sub_menu_options )
                            if option in '0':
                                break

                            handler = data_handlers.get(option)
                            if handler:
                                handler()
                        except KeyboardInterrupt:
                            continue
                elif option == '2':
                    service = self.notes.get('alarme') or self.notes.get('Serviço')
                    report_router.router( service, self.notes, self.extra_notes )
                    if service != None:
                        self.extra_notes.append(f'Atendimento de {service.lower()} gerado')
                else:
                    self.display()
                    finish = Validate.confirm('Você deseja finalizar o serviço', self.info_data)
                    if finish:
                        self.display()
                        break
                        
            except KeyboardInterrupt:
                continue
