from mac_vendor_lookup import MacLookup
from collections       import namedtuple
from core.Validate     import Validate
from core.Informations import Informations

DeviceData = namedtuple('DeviceData', ['type', 'model', 'config', 'serial', 'mac'])

class Device:

    @staticmethod
    def extract_serial(mac: str) -> str:
        serial = mac.strip().replace(':', '')[-6:]
        try:
            if serial[-1].upper() == 'B':
                return serial[:5] + '8'
            elif serial[-1] == '3':
                return serial[:5] + '0'
            return serial
        except:
            return ''

    @staticmethod
    def from_mac(mac: str, return_data: bool = False) -> DeviceData:
        try:
            user_input = mac
            mac_device = mac if mac not in [ 'ax2', 'ax2s', 'ax3', 'ax3s', 'g5', 'c5'] else ''
            try:
                vendor = MacLookup().lookup(mac)
            except:
                vendor = mac
            
            serial = ''
            model  = ''
            config = 'BRIDGE'

            if user_input.lower() in ['ax2', 'ax2s', 'ax3', 'ax3s']:
                model = user_input.upper()
                vendor = 'Huawei'

            elif user_input.lower() in ['g5', 'c5']:
                model  = user_input.upper()
                vendor = 'TP-LINK'

            elif 'Huawei' in vendor:
                vendor = 'Huawei'
            elif 'tp-link' in vendor.lower():
                vendor = 'TP-LINK'
            elif 'Fiberhome' in vendor:
                model  = 'Fiberhome'
                vendor = 'ONU'
                config = 'PPPOE'
                serial = Device.extract_serial(mac)

            if vendor in ['Huawei', 'TP-LINK'] and model == '':
                print(f'{vendor} [modelo]')
                model = input('Modelo: ').strip().upper()

            device_data = DeviceData(vendor, f' {model}' if model else '', config, serial, mac_device )

        except Exception as e:
            device_data = DeviceData('', '', '', '', mac_device)

            print(e)
            input()

        if return_data:
            return device_data

        info = Informations()

        dispositivo = f'{device_data.type} {str(device_data.model).strip()}' if device_data.model != '' else device_data.type
        serial = f'Serial: {device_data.serial}' if device_data.serial != '' else ''

        if device_data.type:
            info.write(f'Dispositivo: {dispositivo}')
        if device_data.config:
            info.write(f'Configuração: {device_data.config}')
        if device_data.serial:
            info.write(f'Serial: {device_data.serial}')

        info.show()

        device_data = DeviceData(user_input, f' {model}' if model else '', '', '')

        return device_data

    @staticmethod
    def interactive(prompt_message: str = 'Escolha um dos dispositivos abaixo', return_data: bool = False) -> DeviceData:
        info = Informations()
        info.write(f'{prompt_message}\n[ 1 ] - Huawei\n[ 2 ] - TP-LINK\n[ 3 ] - Outro\n[ 00 ] - Desconhecido')
        info.write('Informe um MAC, nome do dispositivo ou escolha uma das opções acima', new_line=1)
        info.show()

        user_input = Validate.ask('Dispositivo: ', 'Digite um valor válido!', info)
        model = ''

        if user_input.lower() in ['ax2', 'ax2s', 'ax3', 'ax3s']:
            model = user_input.upper()
            user_input = 'Huawei'
        elif user_input.lower() in ['g5', 'c5']:
            model = user_input.upper()
            user_input = 'TP-LINK'
        elif user_input == '1':
            user_input = '3C:B2:33:4C:0C:A6'  # Huawei
        elif user_input == '2':
            user_input = 'C0:06:C3:36:CD:16'  # TP-LINK
        elif user_input == '00':
            user_input = ''
        elif user_input == '3':
            user_input = Validate.ask('Quem autentica: ', 'Digite algo!').capitalize()

        if ':' in user_input:
            return Device.from_mac(user_input, return_data)

        device_data = DeviceData(user_input, f' {model}' if model else '', '', '', '')
        return device_data if return_data else Device.display(device_data)

    @staticmethod
    def display(device_data: DeviceData) -> DeviceData:
        info = Informations()

        dispositivo = f'{device_data.type} {str(device_data.model).strip()}' if device_data.model != '' else device_data.type

        if device_data.type:
            info.write(f'Dispositivo: {dispositivo}')
        if device_data.config:
            info.write(f'Configuração: {device_data.config}')
        if device_data.serial:
            info.write(f'Serial: {device_data.serial}')
        info.show()
        return device_data
