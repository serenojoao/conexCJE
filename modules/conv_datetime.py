# -*- coding: utf-8 -*-
def conv_date(datetime_db, formato_saida='%d de %B de %Y', force=False):
    import time
    if force:
        try:
            tempo = time.strptime(str(datetime_db),'%Y-%m-%d')
        except:
            return ""
    else:
        tempo = time.strptime(str(datetime_db),'%Y-%m-%d')
    resultado = time.strftime(formato_saida, tempo)
    if "%B" in formato_saida:
        ingles = ['January','February','March','April','May','June', 'July', 'August', 'September', 'October', 'November', 'December']
        equivalente = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
        indice = tempo[1]-1
        resultado = resultado.replace(ingles[indice], equivalente[indice])
    if "%b" in formato_saida:
        ingles = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        equivalente = ['jan', 'fev', 'mar', 'abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        indice = tempo[1]-1
        resultado = resultado.replace(ingles[indice], equivalente[indice])

    return resultado
    
def conv_datetime(datetime_db, formato_saida='%d de %B de %Y, %H:%M:%S', force=False):
    import time
    if force:
        try:
            tempo = time.strptime(str(datetime_db),'%Y-%m-%d %H:%M:%S')
        except:
            return ""
    else:
        tempo = time.strptime(str(datetime_db),'%Y-%m-%d %H:%M:%S')
    resultado = time.strftime(formato_saida, tempo)
    if "%B" in formato_saida:
        ingles = ['January','February','March','April','May','June', 'July', 'August', 'September', 'October', 'November', 'December']
        equivalente = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
        indice = tempo[1]-1
        resultado = resultado.replace(ingles[indice], equivalente[indice])
    if "%b" in formato_saida:
        ingles = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        equivalente = ['jan', 'fev', 'mar', 'abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        indice = tempo[1]-1
        resultado = resultado.replace(ingles[indice], equivalente[indice])

    return resultado

def calc_idade(data_nascimento, formato_entrada='%Y-%m-%d %H:%M:%S', data_base=None, _aniversariante=False, _aniversariante_mes=False):
    import time
    try:
        tempo = time.strptime(str(data_nascimento),formato_entrada)
    except:
        return "?"
    ano_nasc = tempo.tm_year
    mes_nasc = tempo.tm_mon
    dia_nasc = tempo.tm_mday
    hora_nasc = tempo.tm_hour
    minuto_nasc = tempo.tm_min
    segundos_nasc = tempo.tm_sec
    if not data_base:
        agora = time.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    else:
        agora = time.strptime(data_base, formato_entrada)
    ano = agora.tm_year
    mes = agora.tm_mon
    dia = agora.tm_mday
    hora = agora.tm_hour
    minuto = agora.tm_min
    segundos = agora.tm_sec

    if mes > mes_nasc:
        idade = ano-ano_nasc
    elif mes==mes_nasc:
        if _aniversariante_mes:
            return True
        if dia > dia_nasc:
            idade = ano-ano_nasc
        elif dia==dia_nasc:
            if _aniversariante:
                return True
            if hora>hora_nasc:
                idade = ano-ano_nasc
            elif hora==hora_nasc:
                if minuto>minuto_nasc:
                    idade = ano-ano_nasc
                elif minuto==minuto_nasc:
                    if segundos>segundos_nasc:
                        idade = ano-ano_nasc
                    else:
                        idade = ano-ano_nasc-1
                else:
                    idade = ano-ano_nasc-1
            else:
                idade = ano-ano_nasc-1
        else:
            idade = ano-ano_nasc-1
    else:
        idade = ano-ano_nasc-1
    if _aniversariante:
        return False
    elif _aniversariante_mes:
        return False
    else:  
        return idade

class aniversario(object):
    def __init__(self, data_nascimento, formato_entrada='%Y-%m-%d %H:%M:%S'):
        self.anivarsariante_mes = calc_idade(data_nascimento, _aniversariante_mes=True)
        self._anivesariante = calc_idade(data_nascimento, _aniversariante=True)
        self.idade =  calc_idade(data_nascimento)

if __name__ == '__main__':


    print calc_idade("15/01/1980", formato_entrada="%d/%m/%Y", _aniversariante_mes=True)
    print calc_idade("15/01/1980", formato_entrada="%d/%m/%Y", _aniversariante=True)
    print calc_idade("22/05/1978", formato_entrada="%d/%m/%Y")

