def input_multiline(content:str) -> str:
    palavras = []
    texto_unificado = ''

    print(content)
    while True:
        texto = input('').strip()
        if len(texto) != 0:
            texto_unificado += f'{texto} '
            palavras.append( texto )
        else:
            break
    
    return texto_unificado