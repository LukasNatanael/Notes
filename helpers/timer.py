from time              import sleep
from win10toast        import ToastNotifier
from core.Validate     import Validate
from core.Informations import Informations
from helpers           import relatorios

def timer():
    """
    Inicia um cronômetro regressivo com base no tempo em minutos.
    Mostra a contagem no terminal e uma notificação quando o tempo expira.
    """

    infos = Informations()
    toaster = ToastNotifier()

    try:
        minutos = int(Validate.ask('Deseja definir um timer de quanto tempo (minutos)', 'Por favor, informe algo!', infos))
        total_segundos = minutos * 60

        while total_segundos >= 0:
            min_restante, seg_restante = divmod(total_segundos, 60)
            tempo_formatado = f"{str(min_restante).zfill(2)}:{str(seg_restante).zfill(2)}"

            infos.clear_screen()
            print(f"⏳ Tempo restante: {tempo_formatado}")

            sleep(1)
            total_segundos -= 1

        # Notificação final
        toaster.show_toast(
            "⏱️ Timer Finalizado",
            f"Seu timer de {minutos} minuto{'s' if minutos > 1 else ''} acabou!",
            duration=3,
            threaded=True
        )

        infos.clear_screen()
        print(f"✅ Você aguardou por {minutos} minuto{'s' if minutos > 1 else ''}")

    except KeyboardInterrupt:
        relatorios.error_message('Timer interrompido pelo usuário')
    except:
        relatorios.error_message()
