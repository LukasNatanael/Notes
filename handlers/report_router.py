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


def router(report_name: str, notes: dict, extra_notes: list):
    
    routes = {
        'fhtt':                 lambda: fhtt(notes, extra_notes),
        'lentidao':             lambda: lentidao(notes, extra_notes),
        'los':                  lambda: los(notes, extra_notes),
        'ponto_adicional':      lambda: ponto_adicional(notes, extra_notes),
        'roteador_bugado':      lambda: roteador_bugado(notes, extra_notes),
        'troca_plano':          lambda: troca_plano(notes, extra_notes),
        'vencimento':           lambda: vencimento(notes, extra_notes),
        'cancelamento':         lambda: cancelamento(notes, extra_notes),
        'senha_central':        lambda: senha_central(notes),
        'senha_wifi':           lambda: senha_wifi(notes),
        'neovantagens':         lambda: paramount(notes),
        'atendimento_generico': lambda: atendimento_generico(notes, extra_notes),  # fallback
    }

    service = report_name.lower() if report_name else report_name

    alarmes = [ 'dying_gasp', 'link_loss', 'los', 'pon piscando' ]

    if service in alarmes:
        service = 'los'
    elif service in [ 'roteador bugado' ]:
        service = 'roteador_bugado'
    elif service in [ 'fhtt', 'mudança de cômodo', 'mudança de comodo' ]:
        service = 'fhtt'
    elif service in [ 'lentidão', 'oscilação', 'quedas' ]:
        service = 'lentidao'
    elif service in [ 'ponto adicional', 'adicional' ]:
        service = 'ponto_adicional'
    elif service in [ 'vencimento' ]:
        service = 'vencimento'
    elif service in [ 'upgrade', 'downgrade', 'troca de plano' ]:
        service = 'troca_plano'
    elif service in [ 'cancelamento' ]:
        service = 'cancelamento'
    elif service in [ 'senha wi-fi', 'troca de senha wi-fi', 'wi-fi' ]:
        service = 'senha_wifi'
    elif service in [ 'senha central', 'troca de senha da central', 'central do assinante', 'central' ]:
        service = 'senha_central'
    elif service in [ 'paramount+', 'paramount', 'watch brasil', 'watch', 'neovantagens', 'neovantagem' ]:
        service = 'neovantagens'
    else:
        service = 'atendimento_generico'

    service = routes.get(service) or routes.get('atendimento_generico')
    
    if service:
        return service()
