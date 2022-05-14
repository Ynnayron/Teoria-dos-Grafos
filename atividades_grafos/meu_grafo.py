from bibgrafo.grafo_lista_adjacencia import GrafoListaAdjacencia
from bibgrafo.grafo_exceptions import *
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
                        if (v1 == self.A[a].getV1() and v2 == self.A[a].getV2()) or (v2 == self.A[a].getV1()) and v1 == self.A[a].getV2():
                            achei = True
                if  achei is False and v1 != v2:
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

    def dijkstra_drone(self, vi, vf, carga: int, carga_max: int, pontos_recarga: list()):
        pass
