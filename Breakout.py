from tkinter import CENTER
import pygame
import os
from abc import ABC, abstractmethod

#init pygame
pygame.init()
clock = pygame.time.Clock()

#Pygame Init
TITLE = "Breakout"
WIDTH = 1200
HEIGHT = 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.SCALED)
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
        #Bild laden
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images\glasspaddle2.png')).convert_alpha()
        #Bildgegröße bestimmen und Position
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
#Blöcke Klasse
class Block():
    def __init__(self,bx,by):
        self.bx = bx 
        self.by = by
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/brick1.jpg')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))

        print("x-Wert: ",self.block_rect.x)
        print("y-Wert: ",self.block_rect.y)



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


sprites = []
#Zwei Reihen der 50px Höhe Blöcke, 10px Abstand
for r in range(25,145,60):
    #Mitte der 100px Blöcke, 1200 Rand, 10px Abstand pro Block
    for i in range(50,1200,110):
        print("mittiger Startwert x: ",i)
        print("mittiger Startwert y: ",r)
        sprites.append(Block(i,r))

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
    
    

    #Malt die Plattform auf unsere Oberfläche mit den jeweiligen rect Werten Spieler
    screen.blit(spieler.image, spieler.plattform_rect)      

    for sprite in sprites:
        screen.blit(sprite.image,sprite.block_rect)
    #Display wird geupdatet    
    pygame.display.flip()

# Game Exit 
pygame.quit()
