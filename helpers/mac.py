from os import system
from core.Device import Device

def mac(mac: str = '', retornar: bool = False):
    """
    Função simplificada de consulta de dispositivo por MAC,
    usando a classe Device como base.
    """
    clear = lambda: system('cls')

    clear()
    try:
        if not mac:
            mac = input('MAC: ').strip()
            while True:
                if len(mac) != 17:
                    clear()
                    print('Informe um valor MAC válido (17 caracteres)!')
                    mac = input('MAC: ').strip()
                else:
                    break

        clear()
        dispositivo = Device.from_mac(mac, return_data=True)

        if retornar:
            return dispositivo

        clear()
        print(f'Dispositivo:\n{dispositivo.type} {dispositivo.model.strip()}')

        if dispositivo.serial:
            print(f'\nSerial:\n{dispositivo.serial}')

    except KeyboardInterrupt:
        clear()
        print('Encerrando verificação!')
    except Exception as e:
        clear()
        print('Algo deu errado!')
        print(e)
