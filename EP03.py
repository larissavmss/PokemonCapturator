"""
  AO PREENCHER ESSE CABEÇALHO COM O MEU NOME E O MEU NÚMERO USP, 
  DECLARO QUE SOU O ÚNICO AUTOR E RESPONSÁVEL POR ESSE PROGRAMA. 
  TODAS AS PARTES ORIGINAIS DESSE EXERCÍCIO PROGRAMA (EP) FORAM 
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUÇÕES
  DESSE EP E QUE PORTANTO NÃO CONSTITUEM DESONESTIDADE ACADÊMICA
  OU PLÁGIO.  
  DECLARO TAMBÉM QUE SOU RESPONSÁVEL POR TODAS AS CÓPIAS
  DESSE PROGRAMA E QUE EU NÃO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUIÇÃO. ESTOU CIENTE QUE OS CASOS DE PLÁGIO E
  DESONESTIDADE ACADÊMICA SERÃO TRATADOS SEGUNDO OS CRITÉRIOS
  DIVULGADOS NA PÁGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NÃO SERÃO CORRIGIDOS E,
  AINDA ASSIM, PODERÃO SER PUNIDOS POR DESONESTIDADE ACADÊMICA.

  Nome : Larissa Vitória Medeiros Silva
  NUSP : 11276023
  Turma: 224
  Prof.: Roberto Hirata Junior

  Referências: Com exceção das rotinas fornecidas no enunciado
  e em sala de aula, caso você tenha utilizado alguma refência,
  liste-as abaixo para que o seu programa não seja considerado
  plágio ou irregular.
"""

import math

DELTA_T = 0.1
GRAVIDADE = 2
g = GRAVIDADE

#Funções não obrigatorias

def criaCopia(matriz,m,n):
    ''' 
    Cria uma cópia da matriz fornecida
    Entrada: matriz que deseja copiar
    Saída: copia da matriz de entrada
    '''
    copia = []
    for i in range(m):
        linha = []
        for j in range(n):
            num = matriz[i][j]
            linha.append(num)
        copia.append(linha)
    return copia

def HouveColisao(matriz, xpokebola, ypokebola):
    '''Indica se a pokebola colidiu com algum pokemon presente na matriz
    Entrada: Matriz preenchida com os pokemons restantes e o local de lançamento
            da pokebola
    Saída: Retorna True caso a colisão tenha ocorrido, juntamente com o id do
            pokemon atingido. Caso contrário retorna False e 0 como id
    '''
    Colisao = False

    if matriz[round(ypokebola)][round(xpokebola)] == 0 or matriz[round(ypokebola)][round(xpokebola)] == 'T' or matriz[round(ypokebola)][round(xpokebola)] == 'o':
        return Colisao, 0

    else:
        id = matriz[round(ypokebola)][round(xpokebola)]
        Colisao = True
        return Colisao, id


def simula_lancamento(matriz,xpokebola, ypokebola,
                      vlancamento, angulolancamento, m, n):
    '''
    Esta função simula o lançamento da bola até que ela atinja o
    pokemon, o solo ou saia da matriz por x.
    Entrada:Matriz com os pokemons e local de lancamento da pokebola
            Coordenadas do treinador
            Velocidade escalar em metros por segundo
            Ângulo de lançamento em graus e número de linhas e colunas da
            matriz
    Saída: Quatro valores: Um booleano (True se o lançamento teve sucesso
    e acertou o pokemon, ou False caso contrário), a matriz do lançamento,
    o id do pokemon atingido e a coordenada x final da pokebola
    '''
    angulolancamento = grau2Radiano(angulolancamento)
    sen_angulo = math.sin(angulolancamento)
    cos_angulo = math.cos(angulolancamento)
    vx = vlancamento * cos_angulo
    vy = vlancamento * sen_angulo

    xpokebola, ypokebola = atualizaPosicao(xpokebola, ypokebola, vx, vy, DELTA_T)
    atingiu, id = HouveColisao(matriz, xpokebola, ypokebola)
    if matriz[round(ypokebola)][round(xpokebola)] != 'T':
        matriz[round(ypokebola)][round(xpokebola)] = 'o'
    vx, vy = atualizaVelocidade(vx, vy, DELTA_T)

    while not (atingiu) and ypokebola >= 0 and xpokebola>=0 and xpokebola <= n-1:
        if ypokebola > m-1:
            xpokebola, ypokebola = atualizaPosicao(xpokebola, ypokebola, vx, vy, DELTA_T)
            vx, vy = atualizaVelocidade(vx, vy, DELTA_T)
        else:
            xpokebola, ypokebola = atualizaPosicao(xpokebola, ypokebola, vx, vy, DELTA_T)
            if round(xpokebola) >= 0 and round(xpokebola) <= n - 1 and round(ypokebola) < m:
                atingiu, id = HouveColisao(matriz, xpokebola, ypokebola)
                if matriz[round(ypokebola)][round(xpokebola)] != 'T':
                    matriz[round(ypokebola)][round(xpokebola)] = 'o'
            vx, vy = atualizaVelocidade(vx, vy, DELTA_T)

    return atingiu, matriz, id, xpokebola

def InverteHorizontal(matriz, m, n):
    '''
    Inverção horizontal da matriz para considerar y=0 como o chão
    Entrada: matriz que deseja inverter e o número de linhas e o de colunas
    Saída: matriz invertida horizontalmente
    '''
    i = 0
    x = m - 1
    matrizInvertida = []
    for i in range(m):
        linha = []
        for j in range(n):
            linha.append(matriz[x][j])
        matrizInvertida.append(linha)
        i = i + 1
        x = x - 1
    return matrizInvertida

# ======================================================================
# FUNÇÕES OBRIGATÓRIAS
# Implemente neste bloco as funções obrigatórias do EP3.
# NÃO modifique os nomes e parâmetros dessas funções.
# ======================================================================

def leArquivo(nomeArquivo='entrada.txt'):
    '''
    Esta função lê um arquivo ('entrada.txt' por default) e
    retorna uma lista de listas.
    Entrada: arquivo cujo nome está armazenado em nomeArquivo.
             Por default, é 'entrada.txt'
    Saída: uma lista de listas, onde o primeiro elemento é uma
           lista de inteiros [m, n] (dimensões da matriz) e os
           elementos subsequentes são listas que representam as
           característica lidas dos Pokémons na forma:
                [nome, raio, x, y]
    '''
    arquivo = open(nomeArquivo, 'r')
    listaSaida = []
    for linha in arquivo:
        listas = linha.split()
        listaSaida.append(listas)
    arquivo.close()

    return listaSaida

def criaMatriz(m, n):
    '''
    Esta função cria e retorna uma lista de listas.
    Entrada: dois inteiros que representam o número de linhas e
             o número de colunas da matriz.
    Saída: uma lista de m listas, cada uma com n elementos, todos
           inicializados com zeros.
    '''
    M = []
    for i in range(m):
        linhas = []
        for j in range(n):
            linhas.append(0)
        M.append(linhas)
        
    return M

def populaMatriz(matriz, pokemons):
    '''
    Esta função recebe uma matriz e uma lista contendo listas que
    representam os pokémons na forma [nome, raio, x, y] e preenche-a
    os pokémons conforme a representação retangular considerando os
    raios da representação.
    Entrada: matriz representada por uma lista de listas
    Saída: A matriz fornecida é modificada.
    '''
    m, n = len(matriz), len(matriz[0])
    id = 1
    for pokemon in pokemons:
        nome = pokemon[0]
        r = int(pokemon[1])
        x = int(pokemon[2])
        y = int(pokemon[3])
        preenchePokemon(matriz, id, x, y, r)
        id = id + 1

    return matriz

def preenchePokemon(matriz, id, x, y, raio):
    '''
    Esta função é auxiliar da função populaMatriz. Ela insere
    um Pokémon na matriz de acordo com sua representação retangular
    baseada no raio ao redor do ponto central (x,y)
    Entrada: matriz representada por uma lista de listas
             id é o número a preencher a matriz; para o
             primeiro pokémon na lista (de índice zero),
             usa-se 1 e assim subsequentemente.
             x,y são as coordenadas do ponto central
             raio é a distância a ser guardada a partir do
             ponto central.
    Saída: A matriz fornecida é modificada.
    '''
    m, n = len(matriz), len(matriz[0])
    r = raio

    for i in range(m):
        for j in range(n):
            if (x - r) <= j <= (x + r) and (y - r) <= i <= (y + r):
                matriz[i][j] = id

    return matriz


def removePokemon(matriz, id, pokemons):
    '''
    Esta função recebe uma matriz, o numeral que representa o pokémon
    a ser removido da matriz (id) e a lista contendo as listas que
    representam pokémons, substituindo os numerais id por zero
    Entrada: matriz representada por uma lista de listas;
             id é o número a preencher a matriz, para o
             primeiro pokémon na lista (de índice zero),
             usa-se 1 e assim subsequentemente;
             pokemons lista contendo as listas que representam pokémons.
    Saída: A matriz fornecida é modificada.
    '''
    m, n = len(matriz), len(matriz[0])
    for i in range(m):
        for j in range(n):
            if matriz[i][j] == id:
                matriz[i][j] = 0
                    
    return matriz


def imprimeMatriz(matriz):
    '''
    Esta função imprime a matriz dada.
    Note que a matriz deve ser impressa com espelhamento vertical,
    pois a primeira linha representa o chão.
    Entrada: matriz representada por uma lista de listas.
    '''
    m, n = len(matriz), len(matriz[0])
    matriz = InverteHorizontal(matriz, m, n)
    for i in range(m):
        for j in range(n):
            if matriz[i][j] == 0:
                matriz[i][j] = '.'
            print(matriz[i][j], end='')
        print()


def atualizaPosicao(x, y, vx, vy, dt=DELTA_T):
    '''
    Esta função calcula as atualizações das posições de x e y usando
    as velocidades escalares respectivamente dadas por vx e vy.
    Entrada: As posições x e y dadas em metros, as velocidades vx e
    vy em metros por segundo e o intervalo de tempo em segundos.
    Saída: Dois valores: o valor atualizado de x e o valor atualizado de y.
    '''
    x = x + vx*DELTA_T
    y = y + vy*DELTA_T - (g / 2) * DELTA_T**2
    return x, y


def atualizaVelocidade(vx, vy, dt=DELTA_T):
    '''
    Esta função calcula e atualiza as velocidades vx e vy para o
    próximo intervalo de tempo.
    Entrada: As velocidades vx e vy em metros por segundo e o
    intervalo de tempo em segundos.
    Saída: Dois valores: o valor atualizado de vx e o valor atualizado de vy.
    '''
    vy = vy - g*DELTA_T
    return vx, vy


def grau2Radiano(theta):
    '''
    Esta função converte o ângulo theta em graus para radianos.
    Entrada: ângulo theta.
    Saída: ângulo theta em radianos.
    '''
    pi = math.pi
    return (theta * pi/180)

def main():
    nome = input("Digite o nome do arquivo: ")
    N = int(input("Digite o numero N de pokebolas: "))
    xt = int(input("Digite a coordenada x do treinador: "))
    xpokebola = xt
    ypokebola = 0

    # Dados para criação da matriz:
    dadosPokemon = leArquivo(nome)
    m = int(dadosPokemon[0][0])
    n = int(dadosPokemon[0][1])
    matriz = criaMatriz(m, n)
    pokemons = dadosPokemon[1:]
    numPokemons = len(pokemons)

    # Matriz com os pokemons:
    matrizPreenchida = populaMatriz(matriz, pokemons)

    # Comecemos os lançamentos:
    while numPokemons > 0 and N > 0:
        # Matriz com o treinador:
        matrizPreenchida[0][xt] = 'T'

        # Estado do jogo atual
        print("pokebolas disponiveis = ", N)
        N = N - 1
        print("Estado atual do jogo:")
        imprimeMatriz(matrizPreenchida)

        #Lancamento
        Vlancamento = float(input("Digite a velocidade de lancamento em m/s: "))
        anguloLancamento = int(input("Digite o angulo de lancamento em graus: "))
        print("Representacao grafica do lancamento:")
        matrizLancamento = criaCopia(matrizPreenchida, m, n)
        atingiu, matrizLancamento, id, xpokebola = simula_lancamento(matrizLancamento, xt, ypokebola, Vlancamento,  anguloLancamento, m, n)
        imprimeMatriz(matrizLancamento)
        matrizPreenchida[0][xt] = 0

        #Comandos para se atingiu ou não algum pokemon
        if atingiu:
            matrizPreenchida = removePokemon(matrizPreenchida, id, pokemons)
            nomePokemonRemovido = pokemons[id-1][0]
            print(f"Um {nomePokemonRemovido} foi capturado!")
            numPokemons = numPokemons - 1
            xt = round(xpokebola)
        else:
            print("O lancamento nao capturou pokemon algum")
            if N > 0:
                xt = int(input("Digite a coordenada x do treinador: "))
    if numPokemons > 0:
        print("Jogo encerrado")
    else:
        print("Parabens! Todos pokemons foram capturados")

main()