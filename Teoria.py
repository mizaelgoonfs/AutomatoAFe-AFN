#   $ - movimento vazio
#   Os estados finais vao ser definidos dentro de uma lista  
from turtle import pos


def LerArquivo(nomeArquivo):
    
    try:
        arquivoArray = open(nomeArquivo, 'r')
        return arquivoArray  # retorna uma lista str com os números

    except:
        print('Erro de abertura do arquivo: ' + nomeArquivo)
        return


def organizarArray(nomeArquivo):
    strLista = LerArquivo(nomeArquivo).readlines()

    for i in range(0, len(strLista) - 1):
        strLista[i] = strLista[i][0:-1] #retirar \n
    #print (strLista)

    automato_AFe = []
    dicionario_aux = {}

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
            
        strLista[i][1] = dicionario_transicoes
        dicionario_aux[strLista[i][0]] = dicionario_transicoes
        automato_AFe.append(dicionario_aux)
        
        #print(strLista[i][0],' - ',strLista[i][1].keys(),' -> ',strLista[i][1].values(), '\n')
        # Estado Qx lendo 'a' -> {Qy,Qz}
    
    #selecionando estados finais
    # estadosFinais =  input('escolha os estados finais [qx,qy]: \n').split(',')
    # print(estadosFinais)
                    
    return dicionario_aux

def extrair_estados(automato):
    estados = []
    for chave in automato.keys():
        estados.append(chave)
    return estados

def extrair_alfabeto(automato):
    alfabeto = set()
    for value in automato.values():
        for chave in value.keys():
            alfabeto.add(chave)
    
    alfabeto.remove('&')
    return sorted(alfabeto)

conjunto_resultante = set() 
# Conjunto resultante da transição vazia de cada estado, em recursão

def transicao_vazia(estado_atual, automato):
    conjunto_resultante.add(estado_atual)

    estados_atingidos = automato.get(estado_atual).get('&')
    print("Atual: ", estado_atual, "-> ", estados_atingidos)

    if(estados_atingidos != None):
        for estado in (estados_atingidos):
            print("Termo estado: ", estado)
            conjunto_resultante.add(estado)
            print("Conjunto Resultante: ", conjunto_resultante)
        
        for estado2 in (estados_atingidos):
            transicao_vazia(estado2, automato)

    return list(conjunto_resultante)

def transicao(simbolo, conjunto_estados, automato):
    conjunto_resultante = set()

    for estado in (conjunto_estados):
        estados_atingidos = automato.get(estado).get(simbolo)
        if(estados_atingidos != None):
            for est in (estados_atingidos):
                conjunto_resultante.add(est)

    return list(conjunto_resultante)

def conversao(alfabeto, estados, automato_AFe):
    automato_AFN = {}
    for estado in estados:
        dicionario_somente_transicoes = {}
        for simbolo in alfabeto:
            print("\n", estado, "lendo ", simbolo)
            conjunto_trasicao_vazia = transicao_vazia(estado, automato_AFe)
            conjunto_resultante.clear()
            print("T-vazias1: ", conjunto_trasicao_vazia)

            conjunto_trasicao = transicao(simbolo, conjunto_trasicao_vazia, automato_AFe)
            print("T-normais: ", conjunto_trasicao)

            conjunto_result = []
            for i in conjunto_trasicao:
                conjunto_result += transicao_vazia(i, automato_AFe)
            conjunto_resultante.clear()
            print("T-vazias2: ", sorted(conjunto_result))

            if(len(conjunto_result) != 0):
                dicionario_somente_transicoes[simbolo] = sorted(conjunto_result)

        automato_AFN[estado] = (dicionario_somente_transicoes)

    print("AFN: ", automato_AFN)
    
nomeArquivo = 'teste.txt'
automato_AFe = organizarArray(nomeArquivo)
print(automato_AFe)

alfabeto = extrair_alfabeto(automato_AFe)
print("Alfabeto: ", alfabeto)

estados = extrair_estados(automato_AFe)
print("Estados: ", estados)

conversao = conversao(alfabeto, estados, automato_AFe)