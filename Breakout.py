import pygame
import os
from abc import ABC, abstractmethod

#init pygame
pygame.init()
clock = pygame.time.Clock()

#Pygame Init
TITLE = "Pong"
WIDTH = 1280
HEIGHT = 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0,0,0)

screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption(TITLE)

# Dateisystem
game_folder = os.path.dirname(__file__)


#abstrakte Klasse für die Bewegung
class IBewegung(ABC):
    @abstractmethod
    def update(self):
        pass

class Spieler():
    def __init__(self,bewegung: IBewegung):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images\glasspaddle2.png')).convert_alpha()
        #Startposition
        self.plattform_rect = self.image.get_rect(center = (screen.get_rect().centerx,HEIGHT - 50 ))
        #Bewegungsgeschwindigkeit
        self.speed = 10
        #Plattform Steuerung
        self.bewegung = bewegung
        #Plattform Breite
        self.plattform_width = self.image.get_width()

    #Steuerung 
    def steuerung(self):
        self.bewegung.update(self)

#Steuerung durch Statatur    
class TastaturSteuerung_A_D():
    def __init__(self):
        pass

    #Bewegung der Plattform
    def update(self,spieler: Spieler):
        keys = pygame.key.get_pressed()

        rechterRand = WIDTH - spieler.plattform_width
        linkerRand = 0
        if keys[pygame.K_d] and spieler.plattform_rect.x < rechterRand:
            spieler.plattform_rect.x += spieler.speed 
        elif keys[pygame.K_a] and spieler.plattform_rect.x > linkerRand:
            spieler.plattform_rect.x -= spieler.speed
#init
spieler = Spieler(TastaturSteuerung_A_D())

#Game Loop 
running = True
while running:

    #berechnet Zeit zwischen zwei Frames und limitiert diesen
    dt = clock.tick(FPS)
    # SChwarzer Hintergrund
    screen.fill(BLACK)
    spieler.steuerung()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    



    screen.blit(spieler.image, spieler.plattform_rect)      
    #Display wird geupdatet    
    pygame.display.flip()

# Game Exit 
pygame.quit()
