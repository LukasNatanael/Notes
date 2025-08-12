from services.fhtt                 import fhtt
from services.lentidao             import lentidao
from services.los                  import los
from services.ponto_adicional      import ponto_adicional
from services.roteador_bugado      import roteador_bugado
from services.troca_plano          import troca_plano
from services.vencimento           import vencimento
from services.cancelamento         import cancelamento
from services.paramount            import paramount
from services.troca_senhas         import senha_central, senha_wifi
from services.atendimento_generico import atendimento_generico

from helpers.mac                   import mac

from cli.Cobranca                  import Cobranca
from cli.Notes                     import Notes
from core.Limpar                   import Limpar

def notes():
    Notes().interactive()

def limpar():
    Limpar()

def cobrança():
    Cobranca()

SERVICES = {
    'cobrança':             lambda: cobrança(),
    'notes':                lambda: notes(),
    'mac':                  lambda: mac(),
    'fhtt':                 lambda: fhtt(),
    'lentidao':             lambda: lentidao(),
    'los':                  lambda: los(),
    'ponto_adicional':      lambda: ponto_adicional(),
    'roteador_bugado':      lambda: roteador_bugado(),
    'troca_plano':          lambda: troca_plano(),
    'vencimento':           lambda: vencimento(),
    'cancelamento':         lambda: cancelamento(),
    'senha_central':        lambda: senha_central(),
    'senha_wifi':           lambda: senha_wifi(),
    'neovantagens':         lambda: paramount(),
    'atendimento_generico': lambda: atendimento_generico(),  # fallback
}