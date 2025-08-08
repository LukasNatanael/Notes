from os       import system, name
from colorama import Fore, Style

class Validate:

    @staticmethod
    def clear_screen():
        system('cls' if name == 'nt' else 'clear')

    @staticmethod
    def print_message(message, error=None, clear_before=True):
        if clear_before:
            Validate.clear_screen()
        
        print(message, end='')
        if error:
            print(f'{Fore.RED}{error}{Style.RESET_ALL}')

    @staticmethod
    def get_input(prompt):
        return input(prompt).strip()

    @staticmethod
    def confirm(question, message_screen=''):
        return Validate.ask(
            question,
            choices        = ['s', 'n'],
            show_choices   = True,
            message_screen = message_screen
        )


    @staticmethod
    def ask(question:str, error:str='Informe uma opção válida!', message_screen:str='', choices:list=[], show_choices=False, clear_screen_before=True):
        if choices is None:
            choices = []

        if clear_screen_before:
            Validate.clear_screen()

        message = f"{message_screen}\n" if message_screen else ""
        prompt = question.replace(':', '')
        prompt = question.strip()

        if choices and show_choices:
            choices_str = f" [{Fore.GREEN}{'|'.join(choices)}{Style.RESET_ALL}]:"
            prompt += choices_str
        prompt += ':' if ':' not in prompt else ''

        prompt += ' '
        data = Validate.get_input(f"{message}{prompt}")

        while not data or (choices and data not in choices):
            Validate.print_message(f'{message}', error=error, clear_before=True)
            data = Validate.get_input(f"{prompt}")

        # Interpretação de 's'/'n' para booleano
        if set(choices) == {'s', 'n'}:
            return data.lower() == 's'

        return data
