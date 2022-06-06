import pygame
import os
""""
Hier befinden sich die konstanten Einstellungen.
Außerdem sind hier die Listen für die Blöcke und fallenden Objekte(Herz,Münzen).
"""
#init pygame
pygame.init()
clock = pygame.time.Clock()

#Unsere Gamesettings
TITLE = "Breakout"
WIDTH = 1200
HEIGHT = 700
FPS = 70

WHITE = (255, 255, 255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.SCALED)
pygame.display.set_caption(TITLE)

#Hier werden alle sprite Objekte Blöcke gespeichert
sprites = []

#Hier werden alle extra Object gespeichert (Münzen zum Beispiel)
falling_sprites = []

# Dateisystem
game_folder = os.path.dirname(__file__)
