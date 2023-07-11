import numpy as np
from queue import PriorityQueue

#Vr = vermelho
#Vd = verde
#Az = azul
#Am = amarelo

#feijao = Nula
#partida = nodo inicio
#saida = nodo final
dist = {}
pais = {}
CustoDeTrocaDeEstação = 4.0  # cada baldeação "gasta" 4 minutos


def TrocaDeEstação(noAtual, proxNo, proxEst):
  antigaEst = pais[noAtual][1]
  if antigaEst != proxEst and antigaEst != "feijao":  # "feijão foi uma forma de "anular" a cor inicial da estação, pois teoricamente não tem porquê escolher uma cor ao entrar inicialmente em uma estação!
    #print(f'{antigaEst} ---> {proxEst}') acabava printando muitas trocas inúteis
    return True
  else:
    return False


def Distancia_att(noAtual, paiAtual, estAtual):
  if estAtual != 'feijao':
    distAtual, x = Dist_real[paiAtual][noAtual]
    # distAtual -> dist entre no atual e pai
    dist[noAtual] = dist[paiAtual] + distAtual
    if TrocaDeEstação(paiAtual, noAtual, estAtual):
      dist[noAtual] += CustoDeTrocaDeEstação
  #else:
    #dist[noAtual] = 0.0


def H(pai, filho):  # função para cálculo Heurística
  #função basicamente para olhar na matriz
  indexpai, indexfilho = int(pai) - 1, int(filho) - 1
  #agora vamos acessar a matriz de distância e retornar a distância heurística
  Euclidiana = DistanciaHeuristica[indexpai][indexfilho]
  return Euclidiana


def G(pai, filho, atual, linha_next):  # função para
  #função para cálculo do custo
  custo = dist[pai]  # ele irá buscar esse custo na matriz de custos mínimos
  if TrocaDeEstação(pai, filho, linha_next):
    # 4 minutos de espera a cada estação que TROCA DE LINHA
    custo += CustoDeTrocaDeEstação
  #agora resta somar com o custo do array de custos reais
  custo += Dist_real[pai][filho][0]
  return custo


def F(pai, filho, atual, destino, linha_next):
  custo_G = G(pai, filho, atual, linha_next)
  #print(custo_G)
  custo_H = H(filho, destino)
  #print(custo_H)
  custo_F = custo_G + custo_H
  return custo_F


def Astar(inicio, fim):
  dist[inicio] = 0.00
  Dist_real[inicio][inicio] = (0.0, "feijao")
  custo = H(inicio, fim)
  q = PriorityQueue()
  pais[inicio] = (inicio, "feijao")
  q.put((custo, inicio, inicio, "feijao"))
  i = 0
  print("({0} Geracao): {1}".format(i, list(q.queue)))
  print("\n\n")
  i += 1
  while q.queue[0][1] != fim:
    curr_cost, noAtual, paiAtual, curr_linha = q.get()
    if noAtual not in pais:
      pais[noAtual] = (paiAtual, curr_linha)
      Distancia_att(noAtual, paiAtual, curr_linha)
    fronteira = Dist_real[noAtual]
    for estacoes in fronteira:
        if estacoes not in pais:
          next_line = fronteira[estacoes][1]
          new_cost = F(noAtual, estacoes, paiAtual, fim, next_line)
          new_cost = round(new_cost, 2)
          #print(new_cost)
          q.put((new_cost, estacoes, noAtual, next_line))
    print("geraçao({0}): {1}\n".format(i, list(q.queue)))
    i += 1
  last_node = q.get()  # last node
  last_cost, last_node_name, last_parent, last_line = last_node
  pais[last_node_name] = (last_parent, last_line)
  Distancia_att(last_node_name, last_parent, last_line)
  curr = fim
  path = [curr] #apenas inicializando logo com o fim
  #trocas = []
  trocas = [pais[fim][1]]
  while pais[curr][0] != inicio:
    curr = pais[curr][0]
    cor = pais[curr][1]
    path.append(curr)
    trocas.append(cor)
  path.append(inicio)
  inicio = "START"
  trocas.append(inicio)
  
  path.reverse()
  trocas.reverse()
  return path, dist[fim], trocas 



#Matriz utilizada para distância euclidiana
DistanciaHeuristica = np.array([
    [0.0, 10.0, 18.5, 24.8, 36.4, 38.8, 35.8, 25.4,
     17.6, 9.1, 16.7, 27.3, 27.6, 29.8],  # e1X
    [10.0, 0.0, 8.5, 14.8, 26.6, 29.1, 26.1, 17.3,
     10.0, 3.5, 15.5, 20.9, 19.1, 21.8],  # e2X
    [18.5, 8.5, 0.0, 6.3, 18.2, 20.6, 17.6, 13.6,
     9.4, 10.3, 19.5, 19.1, 12.1, 16.6],  # e3X
    [24.8, 14.8, 6.3, 0.0, 12.0, 14.4, 11.5, 12.4,
     12.6, 16.7, 23.6, 18.6, 10.6, 15.4],  # e4X
    [36.4, 26.6, 18.2, 12.0, 0.0, 3.0, 2.4, 19.4,
     23.3, 28.2, 34.2, 24.8, 14.5, 17.9],  # e5X
    [38.8, 29.1, 20.6, 14.4, 3.0, 0.0, 3.3, 22.3,
     25.7, 30.3, 36.7, 27.6, 15.2, 18.2],  # e6X
    [35.8, 26.1, 17.6, 11.5, 2.4, 3.3, 0.0, 20.0,
     23.0, 27.3, 34.2, 25.7, 12.4, 15.6],  # e7x
    [25.4, 17.3, 13.6, 12.4, 19.4, 22.3, 20.0, 0.0,
     8.2, 20.3, 16.1, 6.4, 22.7, 27.6],  # e8x
    [17.6, 10.0, 9.4, 12.6, 23.3, 25.7, 23.0, 8.2,
     0.0, 13.5, 11.2, 10.9, 21.2, 26.6],  # e9x
    [9.1, 3.5, 10.3, 16.7, 28.2, 30.3, 27.3, 20.3,
     13.5, 0.0, 17.6, 24.2, 18.7, 21.2],  # e10x
    [16.7, 15.5, 19.5, 23.6, 34.2, 36.7, 34.2, 16.1,
     11.2, 17.6, 0.0, 14.2, 31.5, 35.5],  # e11x
    [27.3, 20.9, 19.1, 18.6, 24.8, 27.6, 25.7, 6.4,
     10.9, 24.2, 14.2, 0.0, 28.8, 33.6],  # e12x
    [27.6, 19.1, 12.1, 10.6, 14.5, 15.2, 12.4, 22.7,
     21.2, 18.7, 31.5, 28.8, 0.0, 5.1],  # e13x
    [29.8, 21.8, 16.6, 15.4, 17.9, 18.2, 15.6, 27.6,
     26.6, 21.2, 35.5, 33.6, 5.1, 0.0],  # e14x
])




DistanciaHeuristica = DistanciaHeuristica * 2

#Agora as distâncias multiplicadas por 2, já que precisamos converter pra minutos

Dist_real = {
    1: {
        2: (20.0, "Az"),
    },
    2: {
        1: (20.0, "Az"),
        3: (17.0, "Az"),
        9: (20.0, "Am"),
        10: (7.0, "Am"),
    },
    3: {
        2: (17.0, "Az"),
        4: (12.6, "Az"),
        9: (18.8, "Vr"),
        13: (37.4, "Vr"),
    },
    4: {
        3: (12.6, "Az"),
        5: (26.0, "Az"),
        8: (30.6, "Vd"),
        13: (25.6, "Vd"),
    },
    5: {
        4: (26.0, "Az"),
        6: (6.0, "Az"),
        7: (4.8, "Am"),
        8: (60.0, "Am"),
    },
    6: {
        5: (6.0, "Az"),
    },
    7: {
        5: (4.8, "Am"),
    },
    8: {
        5: (60.0, "Am"),
        9: (19.2, "Am"),
        12: (12.8, "Vd"),
    },
    9: {
        2: (20.0, "Am"),
        3: (18.8, "Vr"),
        8: (19.2, "Am"),
        11: (24.4, "Vr"),
    },
    10: {
        2: (7.0, "Am"),
    },
    11: {
        9: (24.4, "Vr"),
    },
    12: {
        8: (12.8, "Vd"),
    },
    13: {
        3: (37.4, "Vr"),
        4: (24.6, "Vd"),
        14: (10.2, "Vd"),
    },
    14: {
        13: (10.2, "Vd"),
    },
}

partida = int(input('selecione o local de partida: '))
saida = int(input('selecione o local de saida: '))
print('\n\n')
resultado, custo, cores = Astar(partida, saida)
print("\n\n\n\nO melhor caminho encontrado pelo Astar é:")
estacoes = len(resultado)
seta = 0
for i in resultado:
  seta += 1
  print(i, end=" --> ")
print(round(custo,2))

for i in cores:
  print(i, end=" --> ")
print("END")



print("\n\nIAN É UM VERME")

#vc colocou no github ja?
#n, nem vou seu preguiçoso
# to debugando
# PARA DE ME ESPECTAAAAAR
