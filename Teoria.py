#   & - movimento vazio

def LerArquivo(nomeArquivo):
    try:
        arquivoArray = open(nomeArquivo, 'r')
        return arquivoArray  # retorna uma lista str com os números

    except:
        print('Erro de abertura do arquivo: ' + nomeArquivo)
        return

def organizarDict(nomeArquivo):
    strLista = LerArquivo(nomeArquivo).readlines()

    for i in range(0, len(strLista) - 1):
        strLista[i] = strLista[i][0:-1] #retirar \n
    #print (strLista)

    automato_AFNe = {}

    for i in range(0, len(strLista)):
        strLista[i] =  strLista[i].split('|')
        #print (strLista)
        
        dicionario_transicoes = {}
        for j in range(1, len(strLista[i])):
            funcao_transicao = strLista[i][j].split('->')
            #print(funcao_transicao)
            dicionario_transicoes[funcao_transicao[0]] = funcao_transicao[1].split(',')
            # Ex: (a -> Q2) Separando símbolo que aponta pros estados alcançados
            #print(strLista[i][j])
            
        #strLista[i][1] = dicionario_transicoes
        automato_AFNe[strLista[i][0]] = dicionario_transicoes
                    
    return automato_AFNe

def extrair_estados(automato):
    estados = []
    for chave in automato.keys():
        estados.append(chave)
    return sorted(estados)

def extrair_alfabeto(automato):
    alfabeto = set()
    for value in automato.values():
        for chave in value.keys():
            alfabeto.add(chave)
    
    alfabeto.remove('&')
    return sorted(alfabeto)

def reconhecimento(estado_inicial, automato_AFNe, estados_finais_AFNe):
    palavra =  input("Digite a palavra: ")
    print("Palavra: ", palavra)

    lista_de_estados = set()
    lista_de_estados.add(estado_inicial)
    lista_de_estados_consumidos = set()
    lista_de_estados_result = set()

    # Transição vazia
    for estado in lista_de_estados:
        lista_de_estados = lista_de_estados.union(set(transicao_vazia(estado, automato_AFNe)))

    for simbolo in palavra:
        # Consumindo simbolo da fita nos estados
        lista_de_estados_consumidos = lista_de_estados_consumidos.union(set(transicao(simbolo, lista_de_estados, automato_AFNe)))
        #Limpando conjunto global
        conjunto_resultante.clear()

        # Transição vazia
        for estado in lista_de_estados_consumidos:
            lista_de_estados_result = lista_de_estados_result.union(set(transicao_vazia(estado, automato_AFNe)))

        lista_de_estados.clear()
        lista_de_estados_consumidos.clear()
        lista_de_estados = lista_de_estados.union(lista_de_estados_result)
        lista_de_estados_result.clear()
    
    for est in lista_de_estados:
        if(est in estados_finais_AFNe):
            return "ACEITA!"
    return "REJEITA!"    

conjunto_resultante = set() 
# Conjunto resultante da transição vazia de cada estado, em recursão

def transicao_vazia(estado_atual, automato):
    conjunto_resultante.add(estado_atual)

    estados_atingidos = automato.get(estado_atual).get('&')
    # print("Atual: ", estado_atual, "-> ", estados_atingidos)

    if(estados_atingidos != None):
        for estado in (estados_atingidos):
            # print("Termo estado: ", estado)
            conjunto_resultante.add(estado)
            # print("Conjunto Resultante: ", conjunto_resultante)
        
        for est in (estados_atingidos):
            transicao_vazia(est, automato)

    return list(conjunto_resultante)

def transicao(simbolo, conjunto_estados, automato):
    conjunto_resultante = set()

    for estado in (conjunto_estados):
        estados_atingidos = automato.get(estado).get(simbolo)
        if(estados_atingidos != None):
            for est in (estados_atingidos):
                conjunto_resultante.add(est)

    return list(conjunto_resultante)

def conversao(alfabeto, estados, automato_AFNe):
    automato_AFN = {}
    for estado in estados:
        dicionario_somente_transicoes = {}
        for simbolo in alfabeto:
            # print("\n", estado, "lendo ", simbolo)
            conjunto_trasicao_vazia = transicao_vazia(estado, automato_AFNe)
            #Limpando conjunto global
            conjunto_resultante.clear()
            # print("T-vazias1: ", conjunto_trasicao_vazia)

            conjunto_trasicao = transicao(simbolo, conjunto_trasicao_vazia, automato_AFNe)
            # print("T-normais: ", conjunto_trasicao)

            conjunto_result = set()
            for est in conjunto_trasicao:
                conjunto_result = conjunto_result.union(set(transicao_vazia(est, automato_AFNe)))
            #Limpando conjunto global
            conjunto_resultante.clear()
            # print("T-vazias2: ", sorted(conjunto_result))

            if(len(conjunto_result) != 0):
                dicionario_somente_transicoes[simbolo] = sorted(conjunto_result)

        automato_AFN[estado] = (dicionario_somente_transicoes)

    return automato_AFN

def extrair_estados_finais(estados_finais_AFNe, automato_AFNe):
    estados_finais_AFN = set()

    for estado in automato_AFNe.keys():
        estados_transicoes_vazias = transicao_vazia(estado, automato_AFNe)
        for estado_atingido in estados_transicoes_vazias:
            if(estado_atingido in estados_finais_AFNe):
                estados_finais_AFN.add(estado)
        #Limpando conjunto global
        conjunto_resultante.clear()

    return sorted(estados_finais_AFN)
    
nomeArquivo = 'teste.txt'
automato_AFNe = organizarDict(nomeArquivo)
print("\nAFNe: ", automato_AFNe)

alfabeto = extrair_alfabeto(automato_AFNe)
print("Alfabeto: ", alfabeto)

estados = extrair_estados(automato_AFNe)
print("Estados: ", estados)

 #selecionando estados finais
estados_finais_AFNe =  input("Escolha os estados finais [qx,qy]: \n").split(',')
print("Estados finais do AFNe: ", estados_finais_AFNe)

# estado_inicial = estados[0]
# reconhecimento = reconhecimento(estado_inicial, automato_AFNe, estados_finais_AFNe)
# print(reconhecimento)

automato_AFN = conversao(alfabeto, estados, automato_AFNe)
print("\nAFN: ", automato_AFN)

#extraindo estados finais da conversão
estados_finais_AFN = extrair_estados_finais(estados_finais_AFNe, automato_AFNe)
print("Estados finais do AFN: ", estados_finais_AFN)