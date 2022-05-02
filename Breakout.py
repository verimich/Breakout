import pygame
import os
from abc import ABC, abstractmethod

#init pygame
pygame.init()
clock = pygame.time.Clock()

#Pygame Init
TITLE = "Breakout"
WIDTH = 1200
HEIGHT = 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.SCALED)
pygame.display.set_caption(TITLE)

#Hier werden alle sprite Objekte gespeichert
sprites = []

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
#
class Block:
    @abstractmethod
    def __init__(self,bx,by):
        self.bx = bx 
        self.by = by
        self.image = ""
        self.block_rect = ""
#Block Klasse
class Block1(Block):
    def __init__(self,bx,by):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/brick1_tile.jpg')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))

#Block Klasse
class Block2(Block):
    def __init__(self,bx,by):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/brick2_tile.jpg')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))

#Block Klasse
class Block3(Block):
    def __init__(self,bx,by):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/brick3.png')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))

#Block Klasse
class Block4(Block):
    def __init__(self,bx,by):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/brick4.png')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))



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

#TileMap Klasse
class Map:
    def __init__(self,filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                #entfernt unnötige Zeichen
                self.data.append(line.strip())
    
    def new(self):
        self.map = Map(os.path.join(
            game_folder, 'tile/map.txt'))
        for row, tiles in enumerate(self.map.data):
            print(type(tiles))
            for col, tile in enumerate(tiles):
                if tile == '1':
                    sprites.append(Block1(col * 50 + 25,row * 50 + 25))
                if tile == '2':
                    sprites.append(Block2(col * 50 +25,row*50 +25))
                if tile == '3':
                    sprites.append(Block3(col * 50 +25,row*50 +25))
                if tile == '4':
                    sprites.append(Block4(col * 50 +25,row*50 +25))



#init
spieler = Spieler(TastaturSteuerung_A_D())

#Blöcke werden erstellt
map = Map(os.path.join(
            game_folder, 'tile/map.txt'))
map.new()

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
