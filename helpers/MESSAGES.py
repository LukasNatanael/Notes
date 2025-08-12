from helpers.acordo   import acordo
from helpers.cep      import cep
from helpers.multa    import multa
from helpers.timer    import timer
from helpers.unm      import unm
from helpers.comparar import comparar

from services.messages.falta_contato       import falta_contato
from services.messages.agendamento         import agendamento
from services.messages.desbloqueio         import desbloqueio
from services.messages.pagamento_invertido import invertido
from services.messages.pagamento           import pagamento
from services.messages.suspensão           import suspensão
from services.messages.pagamento_CNPJ      import cnpj
from services.messages.prorata             import prorata

MESSAGES = {
    'prorata':       lambda: prorata(),
    'acordo':        lambda: acordo(),
    'cep':           lambda: cep(),
    'multa':         lambda: multa(),
    'timer':         lambda: timer(),
    'unm':           lambda: unm(),
    'comparar':      lambda: comparar(),
    'falta_contato': lambda: falta_contato(),

    'agendado':      lambda: agendamento(),
    'desbloqueio':   lambda: desbloqueio(),
    'invertido':     lambda: invertido(),
    'pagamento':     lambda: pagamento(),
    'suspensão':     lambda: suspensão(),
    'cnpj':          lambda: cnpj(),
}