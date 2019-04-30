import csv

def gerarSet(string):
    temp_set = set()
    for x in string:
        temp_set.add(x)
    return temp_set

def retirarIgnores(frase, set_ignore):
    for letra in frase:
        if letra in set_ignore:
            frase = frase.replace(letra, '')
    return frase

def palavrasNoDicionario(dicionario, palavrasFrase):
    temp_list_erratas = []
    for palavra in palavrasFrase:
        if palavra not in dicionario:
            temp_list_erratas.append(palavra)
    return temp_list_erratas

def notasIntencoes(dicionarioIntencoes, frase):
    temp_dict_notas = {}
    contador = 1
    for palavra in frase:
        for intencao in dicionarioIntencoes.keys():
            if palavra in dicionarioIntencoes[intencao]:
                if intencao not in temp_dict_notas:
                    temp_dict_notas[intencao] = 0
                temp_dict_notas[intencao] += 1 * contador
        contador += 1
    return temp_dict_notas

def analiseIntecoes(dicionario_notas_intencoes):
    if len(dicionario_notas_intencoes.keys()) == 0:
        return ""
    lista_keys = []
    for i in dicionario_notas_intencoes.keys():
        lista_keys.append(i)
    intencao_atual = lista_keys[0]
    intencao_atual_nota = dicionario_notas_intencoes[lista_keys[0]]
    for intencao in dicionario_notas_intencoes.keys():
        if dicionario_notas_intencoes[intencao] > intencao_atual_nota:
            intencao_atual_nota = dicionario_notas_intencoes[intencao]
            intencao_atual = intencao
    return intencao_atual

str_letras = "abcdefghijklmnopqrstuvwxyz"
str_ignore = "1234567890()*&%$#@!',./?"
set_letras = gerarSet(str_letras)
set_ignore = gerarSet(str_ignore)

with open('pt_br.txt', 'r', encoding='ISO-8859-1') as f:
    palavras = f.read().split('\n')

with open('intencoes.csv', 'r', encoding='utf8') as csv_f:
    csv_reader = csv.reader(csv_f, delimiter=';')
    dict_intencoes = {}
    linha_counter = 0
    for linha in csv_reader:
        if linha_counter == 0:
            linha_counter += 1
            continue
        if linha[0] not in dict_intencoes:
            dict_intencoes[linha[0]] = []
        dict_intencoes[linha[0]].append(linha[1])

sair = False

context = []

def conversa(input):
    input = retirarIgnores(input.lower(), set_ignore)
    dict_retorno = {}
    frase_separada = input.split()
    erratas = palavrasNoDicionario(palavras, frase_separada)
    notas_intencoes = notasIntencoes(dict_intencoes, frase_separada)
    intencao = analiseIntecoes(notas_intencoes)
    if len(erratas) > 0:
        dict_retorno['speelCheck'] = 'error'
        dict_retorno['erratas'] = erratas
    else:
        context.append(intencao)
        dict_retorno['spellChack'] = 'ok'
        dict_retorno['response'] = {}
        dict_retorno['response']['intencao'] = intencao
        dict_retorno['response']['notas'] = notas_intencoes
    return dict_retorno

while sair != True:
    frase = retirarIgnores(input("Input: "), set_ignore).lower()
    response = conversa(frase)

    if 'response' in response:
        if response['response']['intencao'] == 'sair':
            break
        elif response['response']['intencao'] == 'reset':
            context.clear()

    print(str(response) + "\n" + str(context) + "\n")