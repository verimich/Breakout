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
class Tastatur(ABC):
    @abstractmethod
    def update(self):
        pass

class Spieler():
    def __init__(self,bewegung: Tastatur):
        #Bild laden
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images\glasspaddle1.png')).convert_alpha()
        #Bildgegröße bestimmen und Position, start x Mitte, y 650
        self.plattform_rect = self.image.get_rect(center = (screen.get_rect().centerx,HEIGHT - 45 ))
        #Bewegungsgeschwindigkeit
        self.speed = 10
        #Plattform Steuerung
        self.bewegung = bewegung
        #Plattform Breite
        self.plattform_width = self.image.get_width()

    #Steuerung 
    def steuerung(self):
        self.bewegung.update(self)

class Ball():
    def __init__(self):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images\meinball3.png')).convert_alpha()
        self.bx = screen.get_rect().centerx
        self.by = HEIGHT - 70 
        print("spawn point",self.by)
        self.ball_rect = self.image.get_rect(center = (self.bx,self.by))

        self.sx = 4
        self.sy = 4

    def update(self):
        self.ball_rect.x += self.sx
        self.ball_rect.y += self.sy

        linkerRand = 0
        rechterRand = WIDTH - self.image.get_width()

        if(self.ball_rect.y >= HEIGHT - self.image.get_height() or self.ball_rect.y <= 0): 
            self.sy *= -1
        
        #Bugfixing linker, rechter Rand
        #Nach unten fliegend rechter Rand
        if(self.ball_rect.x >= rechterRand  and self.sx > 0):
            self.sx *= -1
        
        #Nach unten fliegend linker Rand
        if( self.ball_rect.x <= linkerRand  and self.sx < 0):
            self.sx *= -1
        


    def __del__(self):
        pass
        



        

        
    

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
class TastaturSteuerung_A_D(Tastatur):
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
            for col, tile in enumerate(tiles):
                if tile == '1':
                    sprites.append(Block1(col * 50 + 25,row * 50 + 25))
                if tile == '2':
                    sprites.append(Block2(col * 50 +25,row*50 +25))
                if tile == '3':
                    sprites.append(Block3(col * 50 +25,row*50 +25))
                if tile == '4':
                    sprites.append(Block4(col * 50 +25,row*50 +25))
    
class CollisionDetector:
    def __init__(self,ball: Ball, spieler: Spieler):
        self.ball = ball 
        self.spieler = spieler 


    def collision(self):                                                                                                    #Linke Ecke                                                                #Rechte Ecke
        #Spieler trifft den Ball
        if((self.ball.ball_rect.y + self.ball.image.get_height() >= self.spieler.plattform_rect.y and self.ball.ball_rect.y + self.ball.image.get_height() <= self.spieler.plattform_rect.y + self.spieler.image.get_height()) and (self.ball.ball_rect.x + self.ball.image.get_width() >= self.spieler.plattform_rect.x and  self.ball.ball_rect.x   <= self.spieler.plattform_rect.x + self.spieler.image.get_width() ) and self.ball.sy >= 0):
                #linke Hälfte von links
            if(self.ball.sx > 0 and self.ball.ball_rect.x <= self.spieler.plattform_rect.x + self.spieler.image.get_width()/2 - self.ball.image.get_width() ):
                self.ball.sy *= -1
                self.ball.sx *= -1
                 #rechte Hälfte von rechts
            elif(self.ball.sx < 0 and self.ball.ball_rect.x >= self.spieler.plattform_rect.x + self.spieler.image.get_width()/2 ):
                self.ball.sy *= -1
                self.ball.sx *= -1
            else:
                self.ball.sy *= -1
            
            #Wenn der Ball ganz links außen auf den Spieler trifft ändert sich der Flugverlauf (sx wird zu 6 statt 3)
            if self.ball.ball_rect.x + self.ball.image.get_width() >= self.spieler.plattform_rect.x and self.ball.ball_rect.x <= self.spieler.plattform_rect.x + self.spieler.image.get_width()/10:
                self.ball.sy = -2
                #Bleibt negativ oder positiv
                if self.ball.sx <= 0:
                    self.ball.sx = -6
                else:
                    self.ball.sx = 6
            #Wenn der Ball ganz rechts außen auf den Spieler trifft ändert sich der Flugverlauf(sx wird zu 6 statt 3)
            elif self.ball.ball_rect.x + self.ball.image.get_width() >= self.spieler.plattform_rect.x + self.spieler.image.get_width() - self.spieler.image.get_width()/10:
                self.ball.sy = -2
                #Bleibt negativ oder positiv
                if self.ball.sx <= 0:
                    self.ball.sx = -6
                else:
                    self.ball.sx = 6
            #Falls nicht der Rand des Spielers getroffen wurde bleibt sx bei 3
            else:
                #Bleibt negativ oder positiv
                self.ball.sy = -4
                if self.ball.sx <= 0:
                    self.ball.sx = -4
                else:
                    self.ball.sx = 4


        for sprite in sprites:
            #Ball trifft Block von unten
            if self.ball.sy <= 0 and (self.ball.ball_rect.y >= sprite.block_rect.y and self.ball.ball_rect.y <=  sprite.block_rect.y + sprite.image.get_height() ) and (self.ball.ball_rect.x + self.ball.image.get_width() >= sprite.block_rect.x and self.ball.ball_rect.x <= sprite.block_rect.x + sprite.image.get_width()):
                #Block wird von unten auf der links Seite getroffen, während er von rechts kommt
                if((self.ball.sx > 0) and (self.ball.ball_rect.x + self.ball.image.get_width() <= sprite.block_rect.x + sprite.image.get_width()/2) ):
                    print("self.ball.ball_rect.x",self.ball.ball_rect.x + self.ball.image.get_width())
                    print("sprite.block_rect.x",sprite.block_rect.x + sprite.image.get_width()/2)
                    self.ball.sx *= -1
                #Block wird von unten auf der rechten Seite getroffen, während er von links kommt
                if((self.ball.sx < 0) and (self.ball.ball_rect.x >= sprite.block_rect.x + sprite.image.get_width()/2) ):
                    self.ball.sx *= -1
                self.ball.sy *= -1
                sprites.remove(sprite)
            #Ball trifft Block von oben
            elif self.ball.sy > 0 and (self.ball.ball_rect.y + self.ball.image.get_height() >= sprite.block_rect.y and self.ball.ball_rect.y <=  sprite.block_rect.y + sprite.image.get_height() ) and (self.ball.ball_rect.x + self.ball.image.get_width() >= sprite.block_rect.x and self.ball.ball_rect.x <= sprite.block_rect.x + sprite.image.get_width()):  
                print("von oben")
                #Block wird von unten auf der links Seite getroffen, während er von rechts kommt
                if((self.ball.sx > 0) and (self.ball.ball_rect.x + self.ball.image.get_width() <= sprite.block_rect.x + sprite.image.get_width()/2) ):
                    print("self.ball.ball_rect.x",self.ball.ball_rect.x + self.ball.image.get_width())
                    print("sprite.block_rect.x",sprite.block_rect.x + sprite.image.get_width()/2)
                    self.ball.sx *= -1
                #Block wird von unten auf der rechten Seite getroffen, während er von links kommt
                if((self.ball.sx < 0) and (self.ball.ball_rect.x >= sprite.block_rect.x + sprite.image.get_width()/2) ):
                    self.ball.sx *= -1

                self.ball.sy *= -1
                sprites.remove(sprite)
        






def game_loop():

    #init
    spieler = Spieler(TastaturSteuerung_A_D())

    #Ball
    ball = Ball()

    #Collision
    collision = CollisionDetector(ball,spieler)

    #Blöcke werden erstellt
    map = Map(os.path.join(
                game_folder, 'tile/map.txt'))
    map.new()
    #Game Loop 
    print("loop game started")
    running = True
    while running:

        #berechnet Zeit zwischen zwei Frames und limitiert diesen
        dt = clock.tick(FPS)
        # Shhwarzer Hintergrund
        screen.fill(BLACK)

        #Spieler Bewegung
        spieler.steuerung()

        #Ball Bewegung
        ball.update()

        #collision
        collision.collision()


        #Malt die Plattform auf unsere Oberfläche mit den jeweiligen rect Werten Spieler
        screen.blit(spieler.image, spieler.plattform_rect)    

        screen.blit(ball.image, ball.ball_rect)  

        for sprite in sprites:
            screen.blit(sprite.image,sprite.block_rect)
        #Display wird geupdatet    
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
                pygame.quit()

    # Game Exit 
    pygame.quit()


class button():
    def __init__(self,x,y):
        self.x = x 
        self.y = y
        self.button_rect = ""
        self.image = ""
        self.create()

    def create(self):
        
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/start.jpg')).convert_alpha() 
        self.button_rect = self.image.get_rect(center = (self.x,self.y))

class buttonEnding:
    def __init__(self,x,y):
        self.x = x 
        self.y = y
        self.button_rect = ""
        self.image = ""
        self.create()

    def create(self):
        
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/end.jpg')).convert_alpha() 
        self.button_rect = self.image.get_rect(center = (self.x,self.y))



class menu():
    def __init__(self):
        self.start()

    def start(self):
        run = True
        buttonStart = button(WIDTH/2,100)
        buttonEnd = buttonEnding(WIDTH/2,400)

        while run:

            screen.fill(WHITE)

            screen.blit(buttonStart.image, buttonStart.button_rect)
            screen.blit(buttonEnd.image, buttonEnd.button_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_x,position_y = pygame.mouse.get_pos()
                    if buttonStart.button_rect.collidepoint(position_x,position_y):
                        print('clicked on image')
                        run = False
                        game_loop()
                    
                    elif buttonEnd.button_rect.collidepoint(position_x,position_y):
                        run = False
                        pygame.quit()
                


menu1 = menu()