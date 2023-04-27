from bibgrafo.grafo_exceptions import *
from math import inf
from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from sys import maxsize
import unittest


class MeuGrafo(GrafoListaAdjacencia):

    def vertices_nao_adjacentes(self):
        '''
        Provê uma lista de vértices não adjacentes no grafo. A lista terá o seguinte formato: [X-Z, X-W, ...]
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Uma lista com os pares de vértices não adjacentes
        '''
        vna = set()

        for v1 in self.N:
            for v2 in self.N:
                achei = False
                for a in self.A:
                    if v1 != v2:
                        if (v1 == self.A[a].getV1() and v2 == self.A[a].getV2()) or (v2 == self.A[a].getV1()) and v1 == \
                                self.A[a].getV2():
                            achei = True
                if achei is False and v1 != v2:
                    vna.add("{}-{}".format(v1, v2))

        return vna
        pass

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        for i in self.A:
            if ((self.A[i].v1) == (self.A[i].v2)):
                return True
        return False
        pass

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        grau = 0
        if V not in self.N:
            raise VerticeInvalidoException("O vértice passado como parametro é inválido")
        for i in self.A:
            if self.A[i].v1 == V:
                grau += 1
            if self.A[i].v2 == V:
                grau += 1
        return grau

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        arestas = self.A
        for i in arestas:
            A1 = arestas[i]
            for j in arestas:
                A2 = arestas[j]
                if A1 == A2:
                    continue
                if A1.getV1() == A2.getV1():
                    if A1.getV2() == A2.getV2():
                        return True

        return False

        pass

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: O vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        lista = {}
        arestas = self.A
        if V not in self.N:
            raise VerticeInvalidoException("O vértice passado como parametro é inválido")
        for i in arestas:
            if arestas[i].getV1() == V or arestas[i].getV2() == V:
                lista[i] = (arestas[i].getRotulo())

        return lista.keys()

        pass

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''

        count = len(self.A)
        count2 = len(self.N)
        if count == count2 * (count2 - 1) / 2:
            return True

        return False
        pass

    def recursividade_dfs(self, visitados, grafo_dfs, V=" "):
        for a in self.arestas_sobre_vertice(V):
            visitados.append(V)
            if V == self.A[a].getV1() or V == self.A[a].getV2():
                if V== self.A[a].getV1():analisado = self.A[a].getV2()
                else: analisado = self.A[a].getV1()
                if analisado not in visitados and a not in grafo_dfs.A:
                    visitados.append(analisado)
                    grafo_dfs.adicionaAresta(a,V,analisado)
                    self.recursividade_dfs( visitados, grafo_dfs, analisado)

    def dfs(self, V=''):

        Ha_Vertice = False
        for v in self.N:
            if v == V:
                Ha_Vertice = True
        grafo_dfs = MeuGrafo(self.N[::])
        visitados = []
        self.recursividade_dfs(visitados, grafo_dfs, V)
        if Ha_Vertice == False:
            raise VerticeInvalidoException("O vértice não existe no grafo")
        else:
            return grafo_dfs

    def bfs(self, V=''):

        bfs = MeuGrafo(self.N[::])
        Ha_Vertice = False

        vertices_visitados = [V]
        fila = [V]

        for v in self.N:
            if v == V:
                Ha_Vertice = True

        while (len(fila) != 0):
            for a in self.A:
                vertice_analisado = fila[0]

                if self.A[a].getV1() == vertice_analisado or self.A[a].getV2() == vertice_analisado:
                    vertice_adjacente = self.A[a].getV2() if vertice_analisado == self.A[a].getV1() else self.A[
                        a].getV1()

                    if vertice_adjacente not in vertices_visitados:
                        fila.append(vertice_adjacente)
                        vertices_visitados.append(vertice_adjacente)
                        bfs.adicionaAresta(a, vertice_analisado, vertice_adjacente)

            fila.pop(0)

        if Ha_Vertice == False:
            raise VerticeInvalidoException("O vértice não existe no grafo")
        else:
            return bfs

    def conexo(self):
        '''
        Verifica se o grafo é conexo
        :return: Um valor booleano que indica se o grafo é ou não conexo
        '''
        arestas = list()
        for i in self.A:
            arestas.append(self.A[i].getV1() + "-" + self.A[i].getV2())

        vertices = self.N

        listaadj = []

        for vertice in vertices:

            if len(listaadj) < 1:
                listaadj.append(vertice)

            if vertice in listaadj:
                for aresta in arestas:
                    # Perguntamos se o vertice atual esta presente na aresta atual
                    if vertice in aresta:
                        if vertice == aresta[0] and aresta[2] not in listaadj:
                            listaadj.append(aresta[2])
                        elif vertice == aresta[2] and aresta[0] not in listaadj:
                            listaadj.append(aresta[0])
        if len(listaadj) == len(self.N):
            return True
        else:
            return False
        pass

    def total_v(self, lis):
        lista_v = self.N
        cont = 0
        for a in lis:
            if a in lista_v:
                cont += 1
        return cont

    def caminho_dois_v(self, x, y):
        lista_a = self.A
        for aresta in lista_a:
            if (lista_a[aresta].getV1() == x) and (lista_a[aresta].getV2() == y):
                return aresta

    def ha_ciclo(self):
        lista = []
        lista2 = []
        v = self.N
        self.ha_ciclo_recursiva(v[0], lista)
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                if lista[i] == lista[j]:
                    lista2 = lista[i:j + 1:]
                    if lista2:
                        return True
        return False

        pass

    def ha_ciclo_recursiva(self, v, lista):
        lista_aresta = self.A
        lista_v = self.arestas_sobre_vertice(v)

        if v not in lista:
            lista.append(v)
        else:
            lista.append(v)
            return

        for i in lista_v:
            if i not in lista:
                v1 = lista_aresta[i].getV1()
                v2 = lista_aresta[i].getV2()
                if v1 != v:
                    lista.append(i)
                    self.ha_ciclo_recursiva(v1, lista)
                if v2 != v:
                    lista.append(i)
                    self.ha_ciclo_recursiva(v2, lista)
        pass

    #def caminho(self,tamanho):
     #   lista = []
      # v = lista_v[0]
       # lista = self.caminho_rec(v, tamanho, lista)
        #if lista is None:
         #   return False
        #return lista"
    def caminho(grafo, v1, v2):
        g = grafo.bfs(v1)
        for i in g.A:
            if g.A[i].v1 == v2 or g.A[i].v2 == v2:
                return True
        return False

    def caminho_rec(self, v, tam, lis):
        lista_aresta = self.A
        keys = list(lista_aresta.keys())
        n = 0
        if v not in lis:
            if len(lis) > 0:
                ar = self.caminho_dois_v(lis[(len(lis) - 1)], v)
                lis.append(ar)
            lis.append(v)
            for aresta in lista_aresta:
                v1 = lista_aresta[aresta].getV1()
                v2 = lista_aresta[aresta].getV2()
                paralela = self.ha_paralelas()
                if paralela:
                    v1 = lista_aresta[keys[n + 1]].getV1()
                    v2 = lista_aresta[keys[n + 1]].getV2()
                    if n == len(keys):
                        n = 0
                    if tam == self.total_v(lis):
                        return lis
                    if v1 != v:
                        self.caminho_rec(v1, tam, lis)
                    elif v2 != v:
                        self.caminho_rec(v2, tam, lis)
                else:
                    if n == len(keys):
                        n = 0
                    if tam == self.total_v(lis):
                        return lis
                    if v1 != v:
                        self.caminho_rec(v1, tam, lis)
                    elif v2 != v:
                        self.caminho_rec(v2, tam, lis)
        pass

    def dijkstra_drone(self, vi, vf):
        beta = {x: maxsize if x != vi else 0 for x in self.N}
        alpha = {x: 0 if x != vi else 1 for x in self.N}
        omega = {x: "Nulo" if x == vi else "" for x in self.N}

        percurso = vi
        destino = vf

        while percurso != destino:

            verticesAdjacntes = list(self.arestas_sobre_vertice(percurso))

            for x in verticesAdjacntes:
                if self.A[x].getV1() == percurso:
                    if beta[self.A[x].getV2()] > self.A[x].getPeso() and alpha[self.A[x].getV2()] == 0:
                        beta[self.A[x].getV2()] = self.A[x].getPeso() + beta[self.A[x].getV1()]
                        omega[self.A[x].getV2()] = self.A[x].getV1()
                else:
                    if beta[self.A[x].getV1()] > self.A[x].getPeso() and alpha[self.A[x].getV1()] == 0:
                        beta[self.A[x].getV1()] = self.A[x].getPeso() + beta[self.A[x].getV2()]
                        omega[self.A[x].getV1()] = self.A[x].getV2()

            alpha[percurso] = 1
            menorBeta = maxsize
            for y in self.N:
                if alpha[y] != 1 and beta[y] < menorBeta:
                    menorBeta = beta[y]
                    percurso = y
        listaFinal = self.dijkstraImpressao(omega, destino)

        return listaFinal

        pass

    def dijkstraImpressao(self, omega, destino):
        percurso2 = destino
        listaFinal = [percurso2]
        while percurso2 != "Nulo":
            listaFinal.append(omega[percurso2])
            percurso2 = omega[percurso2]
        listaFinal.pop()
        return listaFinal

        pass

    def arestaMenorPeso(self):
        listaArestas = list(self.A)
        menorPeso = listaArestas[0]

        for a in self.A:
            if (self.A[a].getPeso() < self.A[menorPeso].getPeso()):
                menorPeso = a

        return self.A[menorPeso].getV1()

        pass

    def prim(self):
        verticeInicial = self.arestaMenorPeso()

        novoGrafo = MeuGrafo([verticeInicial])
        listaDeVertices = list(verticeInicial)

        while len(self.N) != len(listaDeVertices):
            vMenorPeso = inf
            verticeForaDaArvore = 0
            arestaMenorPeso = 0

            for a in self.A:
                arestaAtual = self.A[a]
                vertice1 = arestaAtual.getV1()
                vertice2 = arestaAtual.getV2()

                if vertice1 in listaDeVertices and vertice2 not in listaDeVertices:
                    if arestaAtual.getPeso() < vMenorPeso:
                        vMenorPeso = arestaAtual.getPeso()
                        arestaMenorPeso = a
                        verticeForaDaArvore = vertice2

                elif vertice2 in listaDeVertices and vertice1 not in listaDeVertices:
                    if arestaAtual.getPeso() < vMenorPeso:
                        vMenorPeso = arestaAtual.getPeso()
                        arestaMenorPeso = a
                        verticeForaDaArvore = vertice1

            if arestaMenorPeso == 0:
                return False

            arestaMenorPeso = self.A[arestaMenorPeso]
            listaDeVertices.append(verticeForaDaArvore)
            novoGrafo.adicionaVertice(verticeForaDaArvore)

            aresta = arestaMenorPeso.getRotulo()
            v1 = arestaMenorPeso.getV1()
            v2 = arestaMenorPeso.getV2()
            peso = arestaMenorPeso.getPeso()

            novoGrafo.adicionaAresta(aresta, v1, v2, peso)

        return novoGrafo

    def kruskal(self):
        arvore = MeuGrafo(self.N)
        arestas = {}

        for a in self.A:
            arestas[self.A[a].rotulo] = self.A[a].peso

        arestas = sorted(arestas, key=arestas.get)
        cont = 0

        while True:
            if not arvore.caminho(self.A[arestas[cont]].v1, self.A[arestas[cont]].v2):
                arvore.adicionaAresta(self.A[arestas[cont]].rotulo, self.A[arestas[cont]].v1, self.A[arestas[cont]].v2,
                                      self.A[arestas[cont]].peso)
            cont += 1
            if arvore.conexo():
                break

        return arvore

