
import os , pygame, sys
from clase_algortimos import Algortimo_A_star, Algoritmo_Djisktra, Algoritmo_BFS
from config import *
from pygames_function import pantalla_config,clock_config
from funciones import solicitar_dimension, dibujar_botones
from clase_tablero import Tablero

pygame.init()
pygame.display.set_caption("Mapa XP")


filas , columnas = solicitar_dimension()


screen = pantalla_config() #creamos el objeto screen y definimos su ancho y alto 
clock = clock_config() #creamos el objeto clock 
running = True

ancho_celda = int(ancho//filas) #Usamos abs para evitar valores negativos
alto_celda = int(alto//columnas)

fila_in , columna_in = None,None
fila_out,columna_out = None,None

objeto_tablero =Tablero(filas,columnas,fila_in,columna_in,fila_out,columna_out,screen,alto_celda,ancho_celda)

while running:

    for event in pygame.event.get():
        #condicional para salir del bucle al presionar la tecla exit de la interfaz
        #------------------------------------------------
        if event.type == pygame.QUIT:
            running = False
        #------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN : #Condicional para cuando se presiona el mouse

            try: #Se usa try para  atrapar el error de presionar fuera del tablero 

                if event.button == 1: #Si la tecla presionada es la izquierda
                    if boton_rest.collidepoint(event.pos):
                        print("RESET")
                        objeto_tablero.reset_todo_el_tablero()
                        run = True
                        continue #Consigue que el programa no agarre el click como un 'error para atrapar'
                    if boton_a_estrella.collidepoint(event.pos):
                        objeto_tablero.reset()
                        algoritmo_A_star = Algortimo_A_star(objeto_tablero)
                        camino = algoritmo_A_star.resolver_tablero()
                        objeto_tablero.dibujar_tablero()
                        objeto_tablero.pintar_camino(camino)
                        continue
                    elif boton_Djikstra.collidepoint(event.pos):
                        algoritmo_Djisktra = Algoritmo_Djisktra(objeto_tablero)
                        camino = algoritmo_Djisktra.resolver_tablero()
                        objeto_tablero.dibujar_tablero()
                        objeto_tablero.pintar_camino(camino)
                        continue
                    elif boton_BFS.collidepoint(event.pos):
                        algoritmo_BFS = Algoritmo_BFS(objeto_tablero)
                        camino = algoritmo_BFS.resolver_tablero()
                        objeto_tablero.dibujar_tablero()
                        objeto_tablero.pintar_camino(camino)
                        continue
                    elif boton_reset_parcial.collidepoint(event.pos):
                        print("RESET PARCIAL")
                        objeto_tablero.reset_parcial()
                        continue
                    elif boton_resize.collidepoint(event.pos):
                        os.system('clear') #Para limpiar la terminal antes
                        objeto_tablero.filas , objeto_tablero.columnas = solicitar_dimension()
                        ancho_celda = int(ancho//objeto_tablero.filas) #Usamos abs para evitar valores negativos
                        alto_celda = int(alto//objeto_tablero.columnas)
                        objeto_tablero.reset_todo_el_tablero()
                    columna_cursor , fila_cursor = pygame.mouse.get_pos() #! Toma la posicion del cursor 
                    columna_celda , fila_celda = int(columna_cursor// ancho_celda), int(fila_cursor//alto_celda)

                    if objeto_tablero.tablero[fila_celda][columna_celda] == celda_libre:
                        objeto_tablero.tablero[fila_celda][columna_celda] = celda_obstaculo

                    elif objeto_tablero.tablero[fila_celda][columna_celda] == celda_obstaculo:
                        objeto_tablero.tablero[fila_celda][columna_celda] = celda_libre

            except: #Agarramos el error y imprimimos cada vez que se imprima fuera del tablero
                print("Se preciono fuera del tablero")

        elif event.type == pygame.KEYDOWN: #Condicional para cuando se presiona el una tecla del keyboard

            try:
                columna_cursor , fila_cursor = pygame.mouse.get_pos()
                columna_celda , fila_celda = int(columna_cursor// ancho_celda), int(fila_cursor//alto_celda)

                if event.key == pygame.K_e: #Si la tecla presionada es "e". Nuestro inicio
                    celda_inicio_ya_existe = any(celda_inicio in fila for fila in objeto_tablero.tablero) #Evalua si ya existe la celda de entrada en el tablero
                    if objeto_tablero.tablero[fila_celda][columna_celda] == celda_inicio and celda_inicio_ya_existe:
                        objeto_tablero.tablero[fila_celda][columna_celda] = celda_libre
                    elif objeto_tablero.tablero[fila_celda][columna_celda] == celda_libre and not celda_inicio_ya_existe:
                        objeto_tablero.tablero[fila_celda][columna_celda] = celda_inicio
                        fila_in,columna_in = fila_celda ,columna_celda
                        objeto_tablero.fila_in , objeto_tablero.columna_in = fila_celda,columna_celda

                if event.key == pygame.K_s: #Si la tecla presionada es "s".Nuestra salida
                    celda_fin_ya_existe = any(celda_fin in fila for fila in objeto_tablero.tablero) #Evalua si ya existe la celda de salida en el tablero
                    if objeto_tablero.tablero[fila_celda][columna_celda] == celda_fin and celda_fin_ya_existe:
                        objeto_tablero.tablero[fila_celda][columna_celda] = celda_libre
                    elif objeto_tablero.tablero[fila_celda][columna_celda] == celda_libre and not celda_fin_ya_existe:
                        objeto_tablero.tablero[fila_celda][columna_celda] = celda_fin
                        fila_out,columna_out = fila_celda ,columna_celda
                        objeto_tablero.fila_out , objeto_tablero.columna_out = fila_celda, columna_celda

            except:
                print("Se presiono fuera del tablero")

    screen.fill("white") #Se usa para: Limpiar la pantalla antes de dibujar cada nuevo frame. Darle color de fondo al juego o interfaz.
    objeto_tablero.dibujar_tablero()
    boton_rest = dibujar_botones("Reset",100,810,screen)
    boton_reset_parcial = dibujar_botones("Reset parcial", 220,810,screen)
    boton_resize= dibujar_botones("Resize",450,810,screen)
    boton_a_estrella = dibujar_botones("Algoritmo A-Star",810,100,screen)
    boton_Djikstra = dibujar_botones("Algorito Djikstra",810,200,screen)
    boton_BFS = dibujar_botones("Algortimo BFS",810,300,screen)

    pygame.display.flip() #Permite mostrar en pantalla lo que se actualiza. Pygame no dibuja en la ventana automáticamente. Primero dibuja en memoria, y cuando hacés display.flip(), muestra todo eso en la pantalla de golpe.
    clock.tick(60)  # Limita el bucle a 60 FPS (frames por segundo)

pygame.quit()
sys.exit()