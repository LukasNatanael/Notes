from core.Validate import Validate
import os

from typing import Union

class MenuOptions:
    def __init__(self, title: str, options: Union[dict, list], question='Escolha uma das opções acima:', lastOption: str = 'Voltar', clearScreen: bool = True):
        self.title = title
        self.options = options
        self.lastOption = lastOption
        self.clearScreen = clearScreen
        question += ':' if ':' not in question else ''
        self.question = question


class Menu:
    def __init__(self, menu_options: MenuOptions):
        self.menu_options = menu_options

        self.message_screen = ''
        self.notes = {}
        self.history = []  # Pilha de navegação (submenus)
        self.choseOption = []

        try:
            self.terminal_width, _ = os.get_terminal_size()
        except OSError:
            self.terminal_width = 80  # fallback

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu_title(self, title, border='─'):
        return f'{border} {title} {border}'.center(self.terminal_width)

    def showOptions(self, title: str, options: Union[list, dict], lastOption: str = 'Voltar', question: str = 'Escolha uma opção:'):
        valid_options = []
        screen_menu = ''
        option_items = []

        if title:
            screen_menu += self.menu_title(title) + '\n'

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
            screen_menu += f'[ {i} ] - {nome}\n'
            valid_options.append(str(i))

        screen_menu += f'[ 0 ] - {lastOption}\n'
        valid_options.append('0')

        escolha = int(Validate.ask(
            question=question + ' ',
            error='Por favor, selecione uma opção válida!',
            message_screen=screen_menu,
            choices=valid_options
        ))

        return escolha

    def show(self):
        from collections import namedtuple

        DataDictionary = namedtuple( 'Data', [ 'key', 'value' ] )

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
                        # print(f'Você selecionou: {selected}')
                        # input("\nPressione Enter para continuar...")
                        break