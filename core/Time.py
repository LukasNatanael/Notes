from datetime    import datetime, timedelta
from collections import namedtuple

class Time:

    dias_semana = [
        'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'
    ]

    meses = [
        'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
        'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
    ]

    @staticmethod
    def data_formatada(offset_dias=0, data_base=None):
        """
        Retorna a data formatada por extenso, com opção de deslocar dias.
        Exemplo: 'Sábado, 13 de Julho de 2025'
        """
                
        data = data_base or datetime.now()
        data += timedelta(days=offset_dias)

        nome_dia = Time.dias_semana[data.weekday()]
        nome_mes = Time.meses[data.month - 1]
        dia = str(data.day).zfill(2)
        mes = str(data.month).zfill(2)
        ano = data.year

        Data = namedtuple( 'Data', [ 'full_date', 'dia', 'mes', 'ano', 'dia_semana', 'nome_mes'])
        
        data = Data(
            f'{dia}/{mes}/{ano}',
            dia, mes, ano,
            nome_dia, nome_mes
        )
        return data

    @staticmethod
    def hora_formatada(offset_horas=0, hora_base=None, incluir_segundos=False):
        """
        Retorna a hora formatada, com opção de deslocar horas.
        Exemplo: '14:35' ou '14:35:00'
        """
        hora = hora_base or datetime.now()
        hora += timedelta(hours=offset_horas)

        Horario = namedtuple( 'Hora', [ 'full_time', 'horas', 'minutos', 'segundos'])
        
        horario = Horario(
            hora.strftime("%H:%M:%S"),
            hora.strftime("%H"),
            hora.strftime("%M"),
            hora.strftime("%S")
        )

        return horario