from core.Validate     import Validate
from core.Informations import Informations, Color
from typing            import Union

from collections       import namedtuple
import os

DataDictionary = namedtuple( 'Data', [ 'key', 'value' ] )
green_text = Color(content_color='green')

class MenuOptions:
    def __init__(self, title: str, options: Union[dict, list], question='Escolha uma das opções acima:', lastOption: str = 'Voltar', clearScreen: bool = True):
        self.title       = title
        self.options     = options
        self.lastOption  = lastOption
        self.clearScreen = clearScreen
        question += ':' if ':' not in question else ''
        self.question = question


class Menu:
    def __init__(self, menu_options: MenuOptions):
        self.menu_options = menu_options

        self.message_screen = ''
        self.notes          = {}
        self.history        = []  # Pilha de navegação (submenus)
        self.choseOption    = []

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def showOptions(self, title: str, options: Union[list, dict], lastOption: str = 'Voltar', question: str = 'Escolha uma opção:'):
        valid_options = []
        infos         = Informations()
        option_items  = []

        if title:
            infos.insert_division( title, color=green_text, new_line=2 )

        # Suporte a dict ou list
        if isinstance(options, dict):
            option_items = list(options.items())
        else:
            option_items = list(enumerate(options))

        for i, item in enumerate(option_items, start=1):
            if isinstance(options, dict):
                nome = str(item[0])
            else:
                nome = item[1].menu_options.title if isinstance(item[1], Menu) else str(item[1])
            infos.write(f'[ { str(i).zfill(2) } ] - {nome}')
            valid_options.append(str(i))

        infos.write(f'[ 00 ] - {lastOption}')
        valid_options.append('0')

        escolha = int(Validate.ask(
            question       = question + ' ',
            error          = 'Por favor, selecione uma opção válida!',
            message_screen = infos,
            choices        = valid_options
        ))

        return escolha

    def show(self):
        current_menu = self  # começa no menu raiz

        while True:
            self.clear()
            options = current_menu.menu_options.options
            choice = current_menu.showOptions(
                title=current_menu.menu_options.title,
                options=options,
                lastOption=current_menu.menu_options.lastOption,
                question=current_menu.menu_options.question
            )

            if choice == 0:
                if not self.history:
                    self.clear()
                    print("Saindo do menu. Até mais!")
                    break
                else:
                    current_menu = self.history.pop()
            else:
                # Diferenciar se options é list ou dict
                if isinstance(options, dict):
                    keys = list(options.keys())
                    key = keys[choice - 1]
                    value = options[key]

                    if isinstance(value, Menu):
                        self.choseOption.append({'key': key, 'value': value.menu_options.title})
                        self.history.append(current_menu)
                        current_menu = value

                    elif callable(value):
                        self.choseOption.append(DataDictionary( key, value.__name__ ))
                        self.clear()
                        value()
                        input("\nPressione Enter para continuar...")

                    else:
                        self.choseOption.append(DataDictionary( key, value ))
                        break

                else:  # é uma lista
                    selected = options[choice - 1]

                    if isinstance(selected, Menu):
                        self.choseOption.append(choice)
                        self.history.append(current_menu)
                        current_menu = selected

                    elif callable(selected):
                        self.choseOption.append(choice)
                        self.clear()
                        selected()
                        input("\nPressione Enter para continuar...")

                    else:
                        self.choseOption.append(choice)
                        break