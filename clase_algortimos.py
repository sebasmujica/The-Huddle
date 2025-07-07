import time , heapq,os, pygame
from config import *
from collections import deque

class Algoritmo():

    def __init__(self,objeto_tablero):

        self.cola = {}
        self.objeto_tablero = objeto_tablero
        self.tablero = objeto_tablero.tablero
        self.filas = objeto_tablero.filas
        self.columnas = objeto_tablero.columnas
        self.nodo_inicial = (objeto_tablero.fila_in , objeto_tablero.columna_in)
        self.nodo_final = (objeto_tablero.fila_out , objeto_tablero.columna_out)

    def obtener_vecino(self,nodo):

        vecinos = []
        x, y = nodo

        for dx, dy, cost in [(-1, 0, 10), (1, 0, 10), (0, -1, 10), (0, 1, 10)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.filas and 0 <= ny < self.columnas and self.tablero[nx][ny] != celda_obstaculo and self.tablero[nx][ny] != celda_obstaculo_temporal:
                vecinos.append(((nx, ny), cost))

        return vecinos
    
    def heuristica(self,nodo_actual):

        #Se restan las coordenadas en x e y del nodo visitado y el nodo de la salida
        dx = abs(nodo_actual[0] - self.nodo_final[0])
        dy = abs(nodo_actual[1] - self.nodo_final[1])
        D1 = 10  # Costo de moverse horizontal o verticalmente
        return D1 * (dx + dy) 
    
    def reconstruir_camino(self,viene_de, actual):

        camino = []

        while actual in viene_de:
            camino.append(actual)
            actual = viene_de[actual]

        #Invierte la lista camino
        camino.reverse()
        #Elimina el ultimo elemente para que visualmente no afecte a la casilla pintada de salida
        camino.pop()
        return camino
    
    def print_busqueda(self,nodo):

        os.system("clear")
        x,y = nodo

        if (x,y) != self.nodo_inicial:
            self.tablero[x][y]= celda_busqueda

        self.objeto_tablero.dibujar_tablero()
        pygame.display.flip()


class Algoritmo_Djisktra(Algoritmo):

    def __init__(self,objeto_tablero):

        super().__init__(objeto_tablero)
        self.lista_abierta = []
        self.lista_cerrada = []
        self.puntos_g = {}

    def resolver_tablero(self):

        heapq.heappush(self.lista_abierta,(0,self.nodo_inicial))
        self.puntos_g[self.nodo_inicial] = 0

        while self.lista_abierta:

            if not self.lista_abierta:
                return []
            _,nodo_actual = heapq.heappop(self.lista_abierta)
            self.lista_cerrada.append(nodo_actual)

            if nodo_actual ==self.nodo_final:
                camino = self.reconstruir_camino(self.cola,nodo_actual)
                return camino
            
            vecinos = self.obtener_vecino(nodo_actual)
            for vecino,costo in vecinos:

                if vecino in self.lista_cerrada:
                    continue

                punto_g = self.puntos_g[nodo_actual] + costo

                if vecino not in self.puntos_g or punto_g < self.puntos_g[vecino]:
                    self.cola[vecino] = nodo_actual
                    self.puntos_g[vecino] = punto_g
                    punto_f = punto_g
                    heapq.heappush(self.lista_abierta,(punto_f,vecino))
                    self.print_busqueda(vecino)   


class Algortimo_A_star(Algoritmo):

    def __init__(self, objeto_tablero):
        super().__init__(objeto_tablero)
        self.lista_abierta = []
        self.lista_cerrada = []
        self.puntos_g = {}
        self.puntos_h ={}

    def resolver_tablero(self):
        heapq.heappush(self.lista_abierta,(0,self.nodo_inicial))
        self.puntos_g[self.nodo_inicial] = 0

        while self.lista_abierta:

            if not self.lista_abierta:
                return []
            _,nodo_actual = heapq.heappop(self.lista_abierta)
            self.lista_cerrada.append(nodo_actual)

            if nodo_actual ==self.nodo_final:
                print("Se llego")
                camino = self.reconstruir_camino(self.cola,nodo_actual)
                return camino
            
            vecinos = self.obtener_vecino(nodo_actual)

            for vecino,costo in vecinos:

                if vecino in self.lista_cerrada:
                    continue

                punto_g = self.puntos_g[nodo_actual] + costo
                punto_h = self.heuristica(vecino)

                if vecino not in self.puntos_g or punto_g < self.puntos_g[vecino]:
                    self.cola[vecino] = nodo_actual
                    self.puntos_g[vecino] = punto_g
                    self.puntos_h[vecino] = punto_h
                    punto_f = punto_g + punto_h*1.5
                    heapq.heappush(self.lista_abierta,(punto_f,vecino))

                self.print_busqueda(vecino)
                time.sleep(0.05)


class Algoritmo_BFS(Algoritmo):

    def __init__(self, objeto_tablero):
        super().__init__(objeto_tablero)
        self.lista_abierta = deque([self.nodo_inicial])
        self.lista_cerrada = set()

    def resolver_tablero(self):

        while self.lista_abierta:

            if not self.lista_abierta:
                return []
            
            nodo_actual = self.lista_abierta.popleft()
            self.lista_cerrada.add(nodo_actual)

            if nodo_actual == self.nodo_final:
                camino = self.reconstruir_camino(self.cola,nodo_actual)
                return camino
            
            vecinos = self.obtener_vecino(nodo_actual)

            for vecino,costo in vecinos:
                if vecino not in self.lista_cerrada and vecino not in self.lista_abierta:
                    self.cola[vecino] = nodo_actual
                    self.lista_abierta.append(vecino)
                    self.print_busqueda(vecino)
