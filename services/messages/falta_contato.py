from core.Informations import Informations
from pyperclip         import copy

def falta_contato():
    Informations().clear_screen()
    message = '[SAUDACAO_TEMPO], acredito que você esteja ocupado no momento e não conseguiu dar continuidade ao atendimento, e por falta de contato irei finalizar o atendimento. Assim que estiver disponível nos contate novamente para que possamos solucionar seu problema.'
    
    print(message)
    copy(message)