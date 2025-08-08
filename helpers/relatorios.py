from core.Informations import Informations, Color
from time              import sleep

def sucess_message(content:str = 'Atendimento copiado para área de transferência', time=1.5 ):
    message = Informations()
    sucess  = Color( 'green', 'green' )

    message.new_line()
    message.insert_division(content, color=sucess, new_line=1)
    message.show(clear=False)
    sleep(time)

def error_message(content:str = 'Erro desconhecido! Atendimento finalizado', time=0 ):
    message = Informations()
    error  = Color( 'red', 'red' )

    message.new_line()
    message.insert_division(content, color=error, new_line=1)
    message.show()
    sleep(time)

def show_extra_notes(extra_notes:list = []):
    import shutil
    size = shutil.get_terminal_size()

    terminal_width = size.columns
    padding_space  = terminal_width - 4

    green = Color(content_color='green')
    infos_extra   = Informations()

    if extra_notes:
        infos_extra.insert_division('Informações extras registradas', color=green, corner_l='┌', corner_r='┐', align='left')
        infos_extra.empty_line()
        
        for note in extra_notes:
            note = note.strip()
            if note != '':
                note_str = note.ljust(padding_space)
                infos_extra.insert_division(note_str, corner_l='│', corner_r='│')

        infos_extra.empty_line()
        infos_extra.insert_division(corner_l='└', corner_r='┘', new_line=1)

    infos_extra.show()