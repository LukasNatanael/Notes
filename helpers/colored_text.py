from colorama import Fore, Style

def colored_text(content: str, color: str) -> str:
    """
    Aplica cor ao texto usando códigos ANSI do colorama.
    
    Args:
        content (str): Texto a ser colorido.
        color (str): Nome da cor. Deve estar em VALID_COLORS.
    
    Returns:
        str: Texto colorido com reset automático.
    
    Raises:
        ValueError: Se a cor fornecida não for válida.
    """
    VALID_COLORS = ['red', 'green', 'blue', 'yellow', 'pink', 'cyan', 'white']
    COLORS = {
        'red':    Fore.RED,
        'green':  Fore.GREEN,
        'blue':   Fore.BLUE,
        'yellow': Fore.YELLOW,
        'pink':   Fore.MAGENTA,
        'cyan':   Fore.CYAN,
        'white':  Fore.WHITE,
    }

    if color not in VALID_COLORS:
        raise ValueError(
            f"Cor inválida: {color}. Escolha entre {VALID_COLORS}"
        )

    return f"{COLORS[color]}{content}{Style.RESET_ALL}"
