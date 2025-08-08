import os
from colorama import Fore, Style
from typing import Union, List

class Title:
    VALID_ALIGNS = [ 'left', 'center', 'right' ]
    def __init__(self, top_title:str='', bottom_title:str='', align_tt:str='left', align_bt:str='left'):
        self.top_title    = top_title
        self.bottom_title = bottom_title
        self.align_tt     = align_tt if align_tt in self.VALID_ALIGNS else 'left'
        self.align_tb     = align_bt if align_bt in self.VALID_ALIGNS else 'left'

class Padding:
    def __init__(self, top:int=0, right:int=1, bottom:int=0, left:int=1):
        # Impede que os valores sejam negativos
        top    = max(0, top)
        right  = max(0, right)
        bottom = max(0, bottom)
        left   = max(0, left)

        terminal_width = self.terminal_size.columns // 2
        left  = terminal_width if left  == 0 else left
        right = terminal_width if right == 0 else right

        self.top    = top
        self.right  = right * terminal_width // 100
        self.bottom = bottom
        self.left   = left * terminal_width // 100

    @property
    def terminal_size(self):
        """Retorna dinamicamente o tamanho atual do terminal."""
        return os.get_terminal_size()

    def __repr__(self):
        return f"<Padding padding_top={self.padding_top}, padding_right={self.padding_right}, padding_bottom={self.padding_bottom}, padding_left={self.padding_left}>"

class Border:
    VALID_BORDER_CHARS = {'─', '│', '┌', '┐', '└', '┘', '├', '┤', ''}

    def __init__(self, border_h:str = '─', border_v: str = '│',corner_tl: str = '┌', corner_tr: str = '┐', corner_bl: str = '└', corner_br: str = '┘'):
        # Verifica se os caracteres passados são válidos.
        if not all(char in self.VALID_BORDER_CHARS for char in [border_h, border_v, corner_tl, corner_tr, corner_bl, corner_br]):
            raise ValueError("Um ou mais caracteres de borda são inválidos.")
        
        self.border_h  = border_h
        self.border_v  = border_v
        self.corner_tl = corner_tl
        self.corner_tr = corner_tr
        self.corner_bl = corner_bl
        self.corner_br = corner_br

    def __repr__(self):
        return f"<Border border_h={self.border_h}, border_v={self.border_v}, corner_tl={self.corner_tl}, corner_tr={self.corner_tr}, corner_bl={self.corner_bl}, corner_br={self.corner_br}>"

class Color:
    VALID_COLORS = ['red', 'green', 'blue', 'yellow', 'pink', 'cyan', 'white']

    # Códigos ANSI para as cores
    COLORS = {
        'red':    Fore.RED,
        'green':  Fore.GREEN,
        'blue':   Fore.BLUE,
        'yellow': Fore.YELLOW,
        'pink':   Fore.MAGENTA,
        'cyan':   Fore.CYAN,
        'white':  Fore.WHITE,
    }

    def __init__(self, border_color: str = 'white', content_color: str = 'white'):
        if border_color not in self.VALID_COLORS:
            raise ValueError(f"Invalid border color: {border_color}. Must be one of {self.VALID_COLORS}")
        if content_color not in self.VALID_COLORS:
            raise ValueError(f"Invalid content color: {content_color}. Must be one of {self.VALID_COLORS}")

        self.border_color  = self.COLORS[border_color]
        self.content_color = self.COLORS[content_color]

    def __repr__(self):
        return f"<Color border_color={self.border_color}, content_color={self.content_color}>"
        
class Informations:
    def __init__(self, data: str = ''):
        self.data = data

    @property
    def terminal_size(self):
        """Retorna dinamicamente o tamanho atual do terminal."""
        return os.get_terminal_size()

    def clear_screen(self):
        """Limpa o terminal de forma multiplataforma."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def clear_data(self):
        """Limpa as informações armazenadas."""
        self.data = ''

    def write(self, content: str, space: bool = True, new_line: bool = False, break_line: bool = False, jump_line:bool=True):
        """Escreve conteúdo nas informações, controlando espaçamentos e quebras de linha."""
        space_char      = ' ' if space else ''
        new_line_char   = '\n' if new_line else ''
        break_line_char = self.new_line(2) if break_line else ''
        jump_line_char  = '\n' if jump_line else ''

        self.data += f'{new_line_char}{content}{space_char}{break_line_char}{jump_line_char}'

    def empty_line(self, width:int=None, corner_l:str= '│', corner_r:str='│'):

        """
        Retorna uma linha vazia do tamanho ideal para alinhamento interno.
        Se 'width' não for fornecido, usa a largura total do terminal menos bordas.
        """
        if width is None:
            width = self.terminal_size.columns - 4  # 4 = margem das bordas

        empty_line = ''.ljust(width)

        self.data += f'{corner_l} {empty_line} {corner_r}\n' 


    def extra_info(self, retornar=True):
        extra_informations = input('\nInformações extras:\n').strip()

        if extra_informations != '':
            extra_informations = f'\nInformações extras: \n{extra_informations}'
            extra_informations += '.' if '.' not in extra_informations[-1] else ''
        else:
            extra_informations = ''

        self.data += f'\n{extra_informations}'

        if retornar:
            return extra_informations

    def title(self, title: str, border: str = '─', color: str = ''):
        """Adiciona um título centralizado com bordas e cor opcional."""
        styled_title = f'{border} {title} {border}'
        colored_title = f"{color}{styled_title.center(self.terminal_size.columns)}{Style.RESET_ALL}"
        self.data += colored_title + '\n'

    def new_line(self, lines: int = 1):
        """Adiciona uma ou mais quebras de linha."""
        self.data += '\n' * lines

    def box(self, 
            title:     Title    = Title(),
            content:   Union[str, List[str]] = '',
            padding:   Padding  = Padding(),
            border:    Border   = Border(),
            align:     str      = 'center',
            color:     Color    = Color(),
            width:     int      = 0,
            new_line:  int      = 1
            ):

        new_line = '\n' * new_line
        width = self.terminal_size.columns if width == 0 else int(self.terminal_size.columns * width / 100)
        if align == 'center':
            offset = (self.terminal_size.columns - width) // 2
        elif align == 'right':
            offset = (self.terminal_size.columns - width )
        elif align == 'left':
            offset = 0

        offset_spaces = ' ' * offset
        
        inner_width = width - 2  # Por conta das laterais

        # Se for string única, vira lista
        if isinstance(content, str):
            content = [content]

        total_side_padding = padding.left + padding.right
        max_content_width = max(0, inner_width - total_side_padding)

        # Monta conteúdo com padding lateral e alinhamento
        padded_content = []
        for line in content:
            aligned_line = self.align(line, position=align).strip()
            if len(aligned_line) > max_content_width:
                aligned_line = aligned_line[:max_content_width]
            padded_line = (
                f"{' ' * padding.left}"
                f"{color.content_color}{aligned_line}{Style.RESET_ALL}"
                f"{' ' * (max_content_width - len(aligned_line))}"
                f"{' ' * padding.right}"
            )
            padded_content.append(
                f"{offset_spaces}{color.border_color}{border.border_v}{Style.RESET_ALL}{padded_line}{color.border_color}{border.border_v}{Style.RESET_ALL}"
            )

        # Top border
        self.insert_division( title.top_title, width=width, align=title.align_tt, corner_l=border.corner_tl, corner_r=border.corner_tr, new_line=0 )

        # Top padding
        for _ in range(padding.top):
            self.data += f"{offset_spaces}{color.border_color}{border.border_v}{Style.RESET_ALL}{' ' * inner_width}{color.border_color}{border.border_v}{Style.RESET_ALL}\n"

        # Content
        for line in padded_content:
            self.data += f"{line}"

        # Bottom padding
        for _ in range(padding.bottom):
            self.data += f"{offset_spaces}{color.border_color}{border.border_v}{Style.RESET_ALL}{' ' * inner_width}{color.border_color}{border.border_v}{Style.RESET_ALL}"

        # Bottom border
        self.insert_division( title.bottom_title, width=width, align=title.align_tb, corner_l=border.corner_bl, corner_r=border.corner_br, new_line=0 )



    def insert_division(
            self,
            title:    str = '',
            align:    str = 'center',
            style:    str = '─',
            corner_l: str = '─',
            corner_r: str = '─',
            width:    int = None,
            color:    Color = Color(),
            new_line: int = 1
        ):
        
        width = width if width is not None else self.terminal_size.columns
        title = f' {title} ' if title != '' else ''
        title_len = len(title)

        new_line = '\n' * new_line

        # Espaço disponível para os estilos depois de descontar as bordas
        usable_width = width - len(corner_l) - len(corner_r)

        if align == 'center':
            side_len = (usable_width - title_len) // 2
            line = f"{color.border_color}{style * side_len}{Style.RESET_ALL}{color.content_color}{title}{Style.RESET_ALL}{color.border_color}{style * side_len}{Style.RESET_ALL}"
            if len(line) < usable_width:
                line += style
        elif align == 'left':
            line = f"{color.content_color}{title}{Style.RESET_ALL}{style * (usable_width - title_len)}"
        elif align == 'right':
            line = f"{style * (usable_width - title_len)}{color.content_color}{title}{Style.RESET_ALL}"
        else:
            line = f"{style * usable_width}"  # fallback

        final_line = f"{color.border_color}{corner_l}{Style.RESET_ALL}{line}{color.border_color}{corner_r}{Style.RESET_ALL}"
        # self.informations += final_line + '\n'
        self.data += final_line + new_line


    def align(self, text: str, position: str = 'center'):
        """Alinha um texto à esquerda, centro ou direita."""
        valid_positions = ['left', 'center', 'right']

        if position not in valid_positions:
            return '────> Posicionamento inválido <─────'.center(self.terminal_size.columns)

        aligned_text = {
            'left': text.ljust(self.terminal_size.columns),
            'center': text.center(self.terminal_size.columns),
            'right': text.rjust(self.terminal_size.columns - 1)
        }

        return aligned_text[position]

    def show(self, clear: bool = True):
        """Exibe o conteúdo no terminal."""
        if clear:
            self.clear_screen()
        print(self.data)

    def __str__(self):
        """Retorna as informações armazenadas."""
        return self.data
    
    def __repr__(self):
        return f"<Informations len={len(self.data)}>"