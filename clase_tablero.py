from config import*
import pygame, time



class Tablero():

    def __init__(self,filas,columnas,fila_in,columna_in,fila_out,columna_out,screen, alto_celda,ancho_celda):
        self.filas = filas
        self.columnas = columnas
        self.tablero = [[celda_libre for fila in range(filas)]for columna in range(columnas)]
        self.fila_in , self.columna_in = fila_in , columna_in
        self.fila_out , self.columna_out = fila_out,columna_out
        self.screen = screen
        self.alto_celda = alto_celda 
        self.ancho_celda = ancho_celda

    def reset(self):
        for i in range(len(self.tablero)):
            for j in range(len(self.tablero[0])):        
                if self.tablero[i][j] == celda_busqueda:
                    self.tablero[i][j]= celda_libre
        self.tablero[self.fila_in][self.columna_in] = celda_inicio
        self.tablero[self.fila_out][self.columna_out] = celda_fin

    def dibujar_tablero(self):
        for fila in range(len(self.tablero)):
            for columna in range(len(self.tablero[0])):
                rect = pygame.Rect(columna*self.alto_celda,fila*self.ancho_celda,self.ancho_celda,self.alto_celda)
                relleno = pygame.Rect(columna*self.alto_celda ,fila*self.ancho_celda ,self.ancho_celda,self.alto_celda)
                if self.tablero[fila][columna] == celda_libre:
                    pygame.draw.rect(self.screen,GRIS,rect,5)
                elif self.tablero[fila][columna] == celda_obstaculo:
                    pygame.draw.rect(self.screen,NEGRO,relleno)
                elif self.tablero[fila][columna] == celda_obstaculo_temporal:
                    pygame.draw.rect(self.screen,GRISGRAFITO,relleno)
                elif self.tablero[fila][columna] == celda_busqueda:
                    pygame.draw.rect(self.screen,CELESTE,relleno)
                elif self.tablero[fila][columna] == celda_inicio:
                    pygame.draw.rect(self.screen,VERDE,relleno)
                elif self.tablero[fila][columna] == celda_fin:
                    pygame.draw.rect(self.screen,ROJO,relleno)
                elif self.tablero[fila][columna] == celda_ruta:
                    pygame.draw.rect(self.screen,AMARILLO,relleno)
    def reset_todo_el_tablero(self):
        self.tablero = [[ 0 for fila in range(self.filas)]for columna in range(self.columnas)]
    def reset_parcial(self):
        for fila in range(len(self.tablero)):
            for columna in range(len(self.tablero[0])):  
                if self.tablero[fila][columna] not in [celda_obstaculo,celda_inicio,celda_fin]:
                    self.tablero[fila][columna] = celda_libre
    def pintar_camino(self,camino):
        if not camino:
            print("NO HAY CAMINO")
        self.reset()
        self.screen.fill("white")
        time.sleep(0.05)
        for cam in camino:
            fila_camino , columna_camino = cam
            self.tablero[fila_camino][columna_camino] = celda_ruta
            self.dibujar_tablero()
            pygame.display.flip()
            time.sleep(0.05)