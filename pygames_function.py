import pygame
from config import*

def pantalla_config():

    pygame.display.init()

    return pygame.display.set_mode((ancho_pantalla,alto_pantalla))

def font_config():

    pygame.font.init()

    return pygame.font.SysFont(None, 46)

def clock_config():
    
    return pygame.time.Clock()