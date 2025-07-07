import pygame
from config import *
from pygames_function import font_config

font = font_config()

def solicitar_dimension():

    while True:
            
            filas_input = input("Ingrese tamaño de filas desado: ")
            columnas_input= input("Ingrese tamaño de columnas desado: ")

            if filas_input.isdigit() and columnas_input.isdigit():
                filas = int(filas_input)
                columnas = int(columnas_input)
                if filas > 0 and columnas > 0:
                    return filas , columnas
                
            else:
                print("Solo se admiten valores numericos")

def dibujar_botones(texto,x,y,screen):
    #Obtenemos el tamaño del texto
    ancho_texto , alto_texto = font.size(texto)
    #Calculamos el tamaño del boton
    ancho_boton = ancho_texto + 5
    alto_boton = alto_texto + 5
    #Posicion del boton 
    pos_x_boton = x
    pos_y_boton = y
    #Creamos el cuadro para el boton
    cuadro_boton = pygame.Rect(pos_x_boton,pos_y_boton,ancho_boton,alto_boton)
    #Se renderiza el texto
    texto_renderizado = font.render(texto,True,NEGRO,GRIS)
    #Se calcula la posicion centrada del texto dentro del boton
    texto_x = x + (ancho_boton - ancho_texto) 
    texto_y = y 
    #
    pygame.draw.rect(screen,GRISGRAFITO,cuadro_boton)
    #
    screen.blit(texto_renderizado,(texto_x,texto_y))
    
    return cuadro_boton
