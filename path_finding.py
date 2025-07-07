import pygame
import sys
import os
import time
import random
import heapq



pygame.init()
pygame.display.set_caption("Mapa XP")
#! Definimos el tamano de pantalla que sera inicializada.
ancho_pantalla = 800
alto_pantalla = 800
ancho = 600
alto = 600

#Solicitamos al usuario la cantidad de filas y columnas deseadas.
def solicitar_dimension():
    try:
        global filas, columnas
        filas = abs(int(input("Ingrese tamaño de filas desado: ")))
        columnas = abs(int(input("Ingrese tamaño de columnas desado: ")))
        #Cálculo de las dimensiones de cada celda de la matriz 
        #------------------------------------------------
        global ancho_celda, alto_celda
        ancho_celda = int(ancho//filas) #Usamos abs para evitar valores negativos
        alto_celda = int(alto//columnas)
    except:
        if not isinstance(filas,int):
            print("La cantidad de filas no esta definida")
            filas = int(input("Ingrese tamaño de filas desado: "))
        if not isinstance(columnas,int):
            print("La cantidad de columnas no esta definida")
            columnas = int(input("Ingrese tamaño de columnas desado: "))
    finally:
        ancho_celda = int(ancho//filas)
        alto_celda = int(alto//columnas)


#Realizamos el setup basico de un proyecto de pygame
#------------------------------------------------
screen = pygame.display.set_mode((ancho_pantalla,alto_pantalla)) #creamos el objeto screen y definimos su ancho y alto 
clock = pygame.time.Clock() #creamos el objeto clock 
running = True
run = True
font = pygame.font.SysFont(None, 46) #Objeto font para los textos y botones
#------------------------------------------------
#Definimos los colores que se usarán
AZUL = (0, 0, 255)
BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
GRISGRAFITO = (80, 80, 80)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
CELESTE = (173, 216, 230)
#------------------------------------------------
ultimo_momento = time.time()
celda_libre = 0
celda_obstaculo = 1
celda_agua = 2
celda_inicio = 3
celda_fin = 4
celda_obstaculo_temporal = 5
celda_ruta = 6
solicitar_dimension()
tablero = [[celda_libre for columna in range(columnas)]for fila in range(filas)]


#Funcion que dibuja el tablero 
def dibujar_tablero():
    for fila in range(filas):
        for columna in range(columnas):
            rect = pygame.Rect(columna*alto_celda,fila*ancho_celda,ancho_celda,alto_celda)
            relleno = pygame.Rect(columna*alto_celda ,fila*ancho_celda ,ancho_celda,alto_celda)
            if tablero[fila][columna] == celda_libre:
                pygame.draw.rect(screen,GRIS,rect,5)
            elif tablero[fila][columna] == celda_obstaculo:
                pygame.draw.rect(screen,NEGRO,relleno)
            elif tablero[fila][columna] == celda_obstaculo_temporal:
                pygame.draw.rect(screen,GRISGRAFITO,relleno)
            elif tablero[fila][columna] == celda_agua:
                pygame.draw.rect(screen,AZUL,relleno)
            elif tablero[fila][columna] == celda_inicio:
                pygame.draw.rect(screen,VERDE,relleno)
            elif tablero[fila][columna] == celda_fin:
                pygame.draw.rect(screen,ROJO,relleno)
            elif tablero[fila][columna] == celda_ruta:
                pygame.draw.rect(screen,CELESTE,relleno)
            

def dibujar_botones(texto,x,y):
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

def reset_todo():
    global tablero #Decimos que tablero es una variable global
    tablero = [[celda_libre for columna in range(columnas)]for fila in range(filas)]
coordenadas_de_obstaculos = []
tiempo_de_creacion = 0
def obstaculo_temporal():
    global tablero , filas,columnas , tiempo_de_creacion
    fila_random = 0
    columna_random = 0
    fila_random_1 = 0
    columna_random_1 = 0 
    check = 1
    if check == 1:
        fila_random = random.randint(0,filas-1)
        columna_random = random.randint(0,columnas-1)
        fila_random_1 = random.randint(0,filas-1)
        columna_random_1 = random.randint(0,columnas-1)
        tiempo_de_creacion = time.time()
        coordenadas_de_obstaculos.append((fila_random,columna_random))
        coordenadas_de_obstaculos.append((fila_random_1,columna_random_1))
        if tablero[fila_random][columna_random] == celda_libre:
            tablero[fila_random][columna_random] = celda_obstaculo_temporal
        if tablero[fila_random_1][columna_random_1] == celda_libre:
            tablero[fila_random_1][columna_random_1] = celda_obstaculo_temporal    
def quitar_obstaculo():
    global coordenadas_de_obstaculos
    for coordenada in coordenadas_de_obstaculos:
        fila_random , columna_random = coordenada
        if tablero[fila_random][columna_random] == celda_obstaculo_temporal:
            tablero[fila_random][columna_random] = celda_libre


def algoritmo():
    global entrada_fila , entrada_columna , salida_fila , salida_columna
    #Crear la listaAbierta como una lista de nodo vacia
    lista_Abierta = []
    #Crear la listaCerrada como una lista de nodos vacia
    lista_Cerrada = []
    punto_g = {}#Diccionario clave: nodo valor : punto g
    punto_h = {}
    cola = {}
    camino = {}
    nodo_actual = None
    nodo_inicial = (entrada_fila,entrada_columna)
    nodo_final = (salida_fila, salida_columna)
    #Poner el nodoInicial en la listaAbierta(asignarle un costo f igual  a 0)
    heapq.heappush(lista_Abierta,(0,nodo_inicial))
    punto_g[nodo_inicial] = 0
    #Bucle que corre mientras listaAbierta no este vacia
    while lista_Abierta:
        #Obtener el nodoActual a partrir del nodo con el costo f mas bajop de la listaAbierta 
        if nodo_actual is None:
            if not lista_Abierta:
                return []
        #Sacamos el nodo con menor f
        _,nodo_actual = heapq.heappop(lista_Abierta)
        #Poner el nodoActual en la listaCerrada
        lista_Cerrada.append(nodo_actual)
        #Si el nodoActual es igual al nodoFinal:
        if nodo_actual == nodo_final:
            #Enviamos la cola y a la funcion para recontruir el camino
            camino = reconstruir_camino(cola,nodo_actual)
            return camino
        #Crear una lista de nodos vecinos del nodoActual
        nodos_vecinos = obtener_vecinos(nodo_actual)
        #Recorrer los vecinos del nodoActual
        for vecino , costo in nodos_vecinos:
            #Si el vecino esta en listCerrada saltamos al siguiente
            if vecino in lista_Cerrada:
                continue
            #Hacer los calculos de 'g' ,'h' y 'f' 
            costo_g = punto_g[nodo_actual] + costo
            costo_h = heuristica(vecino, nodo_final)
            #Si el Vecino no posee un valor g o si su valor g guardado es mayor
            if vecino not in punto_g or costo_g < punto_g[vecino]:
                cola[vecino] = nodo_actual # Vecino viene de nodoActual
                punto_g[vecino] = costo_g
                punto_h[vecino] = costo_h
                puntaje_f = costo_g + costo_h
                #agregamos el vecino a la lista abierta
                heapq.heappush(lista_Abierta,(puntaje_f, vecino))
                print_busqueda(vecino)

def obtener_vecinos(nodo):
    vecinos = []
    x, y = nodo
    for dx, dy, cost in [(-1, 0, 10), (1, 0, 10), (0, -1, 10), (0, 1, 10)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < columnas and 0 <= ny < filas and tablero[nx][ny] != celda_obstaculo and tablero[nx][ny] != celda_obstaculo_temporal:
            vecinos.append(((nx, ny), cost))
    return vecinos

def heuristica(a, b):
    #Se restan las coordenadas en x e y del nodo visitado y el nodo de la salida
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    D1 = 10  # Costo de moverse horizontal o verticalmente
    D2 = 14  # Costo de moverse en diagonal
    return D1 * (dx + dy) + (D2 - 2 * D1) * min(dx, dy)

def reconstruir_camino(viene_de, actual):
    camino = []
    while actual in viene_de:
        camino.append(actual)
        actual = viene_de[actual]
    #Invierte la lista camino
    camino.reverse()
    #Elimina el ultimo elemente para que visualmente no afecte a la casilla pintada de salida
    camino.pop()
    return camino

def pintar_camino(camino):
    if not camino:
        print("NO HAY CAMINO")
    for cam in camino:
        fila_camino , columna_camino = cam
        tablero[fila_camino][columna_camino] = celda_ruta
        dibujar_tablero()
        pygame.display.flip()
        time.sleep(0.05)
        #Pausa la ejecucion para darle un efecto 
        
def print_busqueda(nodo):
        os.system("clear")
        x,y = nodo
        if (x,y) != (entrada_fila,entrada_columna):
            pass
        tablero[x][y]= celda_agua
        dibujar_tablero()
        pygame.display.flip()
#! Considerar la realcion x ---> columnas ; y ---> filas al usar el get_pos(). Ya que el get_pos() devuelve tupla (x(ancho de celda),y(alto de celda))
#*Tambien considerar que el click izquierdo --->1 ; click del scroll ---> 2; click derecho ----> 3
while running:
    
    #Bloque enfocado en el manejo de los obstaculos temporales
    if run:
        ahora = time.time()
        if ahora - ultimo_momento >= 5 :
            #print("pasaron 5 seg")
            obstaculo_temporal()
            ultimo_momento = ahora
        if ahora - tiempo_de_creacion >= 3 and tiempo_de_creacion != 0:
            #print("se quiere quitar")
            quitar_obstaculo()
            tiempo_de_creacion = 0
    for event in pygame.event.get():
        #condicional para salir del bucle al presionar la tecla exit de la interfaz
        #------------------------------------------------
        if event.type == pygame.QUIT:
            running = False
        #------------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN : #Condicional para cuando se presiona el mouse
            try: #Se usa try para  atrapar el error de presionar fuera del tablero 
                if event.button == 1: #Si la tecla presionada es la izquierda
                    boton_rest = dibujar_botones("Reset",100,700)
                    boton_resolver = dibujar_botones("Resolver",300,700)
                    boton_resize= dibujar_botones("Resize",500,700)
                    if boton_rest.collidepoint(event.pos):
                        reset_todo()
                        run = True
                        continue #Consigue que el programa no agarre el click como un 'error para atrapar'
                    if boton_resolver.collidepoint(event.pos):
                        camino = algoritmo()
                        pintar_camino(camino)
                        run = False
                        continue
                    if boton_resize.collidepoint(event.pos):
                        os.system('clear') #Para limpiar la terminal antes
                        solicitar_dimension()
                        reset_todo()
                        run = True
                        continue
                    columna_cursor , fila_cursor = pygame.mouse.get_pos() #! Toma la posicion del cursor 
                    columna_celda , fila_celda = int(columna_cursor// ancho_celda), int(fila_cursor//alto_celda)
                    if tablero[fila_celda][columna_celda] == celda_libre:
                        tablero[fila_celda][columna_celda] = celda_obstaculo
                    elif tablero[fila_celda][columna_celda] == celda_obstaculo:
                        tablero[fila_celda][columna_celda] = celda_libre
                elif event.button == 3: #Si la tecla presionada es la derecha
                    columna_cursor , fila_cursor = pygame.mouse.get_pos()
                    columna_celda , fila_celda = int(columna_cursor// ancho_celda), int(fila_cursor//alto_celda)
                    if tablero[fila_celda][columna_celda] == celda_libre:
                        tablero[fila_celda][columna_celda] = celda_agua
                    elif tablero[fila_celda][columna_celda] == celda_agua:
                        tablero[fila_celda][columna_celda] = celda_libre
            except: #Agarramos el error y imprimimos cada vez que se imprima fuera del tablero
                print("Se preciono fuera del tablero")
        elif event.type == pygame.KEYDOWN: #Condicional para cuando se presiona el una tecla del keyboard
            try:
                columna_cursor , fila_cursor = pygame.mouse.get_pos()
                columna_celda , fila_celda = int(columna_cursor// ancho_celda), int(fila_cursor//alto_celda)
                if event.key == pygame.K_e: #Si la tecla presionada es "e". Nuestro inicio
                    celda_inicio_ya_existe = any(celda_inicio in fila for fila in tablero) #Evalua si ya existe la celda de entrada en el tablero
                    if tablero[fila_celda][columna_celda] == celda_inicio and celda_inicio_ya_existe:
                        tablero[fila_celda][columna_celda] = celda_libre
                    elif tablero[fila_celda][columna_celda] == celda_libre and not celda_inicio_ya_existe:
                        tablero[fila_celda][columna_celda] = celda_inicio
                        entrada_fila, entrada_columna = fila_celda ,columna_celda
                if event.key == pygame.K_s: #Si la tecla presionada es "s".Nuestra salida
                    celda_fin_ya_existe = any(celda_fin in fila for fila in tablero) #Evalua si ya existe la celda de salida en el tablero
                    if tablero[fila_celda][columna_celda] == celda_fin and celda_fin_ya_existe:
                        tablero[fila_celda][columna_celda] = celda_libre
                    elif tablero[fila_celda][columna_celda] == celda_libre and not celda_fin_ya_existe:
                        tablero[fila_celda][columna_celda] = celda_fin
                        salida_fila, salida_columna = fila_celda ,columna_celda
            except:
                print("Se presiono fuera del tablero")

    screen.fill("white") #Se usa para: Limpiar la pantalla antes de dibujar cada nuevo frame. Darle color de fondo al juego o interfaz.
    dibujar_tablero()
    boton_rest = dibujar_botones("Reset",100,700)
    boton_resolver = dibujar_botones("Resolver",300,700)
    boton_resize= dibujar_botones("Resize",500,700)
    
    pygame.display.flip() #Permite mostrar en pantalla lo que se actualiza. Pygame no dibuja en la ventana automáticamente. Primero dibuja en memoria, y cuando hacés display.flip(), muestra todo eso en la pantalla de golpe.
    clock.tick(60)  # Limita el bucle a 60 FPS (frames por segundo)
pygame.quit()
sys.exit()


