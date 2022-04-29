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

class Plattform():
    def __init__(self,bewegung: IBewegung):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images\glasspaddle2.png')).convert_alpha()
        #Startposition
        self.paddle_rect = self.image.get_rect(center = (screen.get_rect().centerx,HEIGHT - 50 ))
        #Bewegungsgeschwindigkeit
        self.speed = 10
        #Paddle Steuerung
        self.bewegung = bewegung
        #Paddle Breite
        self.paddle_width = self.image.get_width()

    #Steuerung 
    def steuerung(self):
        self.bewegung.update(self)

#Steuerung durch Statatur    
class TastaturSteuerung_A_D():
    def __init__(self):
        pass

    #Bewegung des Paddles
    def update(self,plattform: Plattform):
        keys = pygame.key.get_pressed()

        rechterRand = WIDTH - plattform.paddle_width
        linkerRand = 0
        if keys[pygame.K_d] and plattform.paddle_rect.x < rechterRand:
            plattform.paddle_rect.x += plattform.speed 
        elif keys[pygame.K_a] and plattform.paddle_rect.x > linkerRand:
            plattform.paddle_rect.x -= plattform.speed
#init
plattform = Plattform(TastaturSteuerung_A_D())

#Game Loop 
running = True
while running:

    #berechnet Zeit zwischen zwei Frames und limitiert diesen
    dt = clock.tick(FPS)
    # Blauer Hintergrund
    screen.fill(BLACK)
    plattform.steuerung()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    



    screen.blit(plattform.image, plattform.paddle_rect)      
    #Display wird geupdatet    
    pygame.display.flip()

# Game Exit 
pygame.quit()
