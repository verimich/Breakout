from turtle import width
import pygame
import os
from abc import ABC, abstractmethod
import time

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

#Hier werden alle sprite Objekte Blöcke gespeichert
sprites = []

#Hier werden alle extra Object gespeichert (Münzen zum Beispiel)
falling_sprites = []


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
        #Leben
        self.leben = 3
        self.leben_list = []
        self.create_hearts()

    #Steuerung 
    def steuerung(self):
        self.bewegung.update(self)
    
    def create_hearts(self):
        for i in range(0,self.leben):
            self.leben_list.append(Leben(i*25 + 25,HEIGHT-25))
    
    def add_heart(self):
        self.leben += 1
        print("HEART ADDED")
        self.leben_list.append(Leben(self.leben*25,HEIGHT-25))
    
    def remove_heart(self):
        if self.leben_list:
            self.leben -= 1
            del self.leben_list[-1]
        
class Ball():
    def __init__(self):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images\meinball3.png')).convert_alpha()
        self.bx = screen.get_rect().centerx
        self.by = HEIGHT - 70 
        
        self.ball_rect = self.image.get_rect(center = (self.bx,self.by))

        self.sx = 4
        self.sy = 4

    def update(self):
        self.ball_rect.x += self.sx
        self.ball_rect.y += self.sy

        linkerRand = 0
        
        rechterRand = WIDTH - self.image.get_width()

        # unterer Rand
        if(self.ball_rect.y >= HEIGHT - self.image.get_height() and self.sy > 0): 
            self.sy *= -1
        
        #Oberer Rand
        if(self.ball_rect.y <= 0 and self.sy < 0): 
            self.sy *= -1
        
        #Bugfixing linker, rechter Rand
        #Nach unten fliegend rechter Rand
        if(self.ball_rect.x >= rechterRand  and self.sx > 0):
            self.sx *= -1
        
        #Nach unten fliegend linker Rand
        if( self.ball_rect.x <= linkerRand  and self.sx < 0):
            self.sx *= -1

class Leben:
    def __init__(self,x,y):
        self.x = x 
        self.y = y 
        self.image = ""
        self.block_rect = ""
        self.create()
    
    def create(self):
        self.image = pygame.image.load(os.path.join(
        game_folder, 'images/heart.png')).convert_alpha() 
        self.leben_rect = self.image.get_rect(center = (self.x,self.y))
        
    

class Muenze:
    def __init__(self,x,y):
        self.x = x 
        self.y = y 
        self.ys = 6
        self.image = ""
        self.block_rect = ""
        self.id = 5
        self.create()

    def create(self):
        self.image = pygame.image.load(os.path.join(
        game_folder, 'images/coin.png')).convert_alpha() 
        self.y += self.image.get_height()/2
        self.muenze_rect = self.image.get_rect(center = (self.x,self.y))
        
    def update(self):
        self.muenze_rect.y += self.ys

class FallendesHerz:
    def __init__(self,x,y):
        self.x = x 
        self.y = y 
        self.ys = 6
        self.image = ""
        self.block_rect = ""
        self.id = 6
        self.create()

    def create(self):
        self.image = pygame.image.load(os.path.join(
        game_folder, 'images/heart.png')).convert_alpha() 
        self.y += self.image.get_height()/2
        self.herz_rect = self.image.get_rect(center = (self.x,self.y))
        
    def update(self):
        self.herz_rect.y += self.ys
        



class Block:
    @abstractmethod
    def __init__(self,bx,by):
        self.bx = bx 
        self.by = by
        self.image = ""
        self.block_rect = ""
        self.id = 0
#Block Klasse
class Block1(Block):
    def __init__(self,bx,by):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/brick1_tile.jpg')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))
        self.id = 1

#Block Klasse
class Block2(Block):
    def __init__(self,bx,by):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/brick2_tile.jpg')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))
        self.id = 2
    
    def hit(self):
        falling_sprites.append(FallendesHerz(self.block_rect.x + self.image.get_width()/2,self.block_rect.y + self.image.get_height()))

#Block Klasse
class Block3(Block):
    def __init__(self,bx,by):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/brick3.png')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))
        self.id = 3

    def change(self):
        self.id = 1
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/brick1_tile.jpg')).convert_alpha()

        
    

#Block Klasse
class Block4(Block):
    def __init__(self,bx,by):
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images/brick4.png')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))
        self.id = 4
    
    def hit(self):
        falling_sprites.append(Muenze(self.block_rect.x + self.image.get_width()/2,self.block_rect.y + self.image.get_height()))



#Steuerung durch Tastatur    
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

#Steuerung durch Tastatur via Pfeiltasten
class TastaturSteuerung_Arrow_Keys(Tastatur):
    def update(self,spieler: Spieler):
        
        keys = pygame.key.get_pressed()
        rechterRand = WIDTH - spieler.plattform_width
        linkerRand = 0
        if keys[pygame.K_LEFT] and spieler.plattform_rect.x <rechterRand:
            spieler.plattform_rect.x += spieler.speed
        elif keys[pygame.K_RIGHT] and spieler.plattform_rect.x > linkerRand:
            spieler.plattform_rect.x -= spieler.speed


#TileMap Klasse
class Map:
    def __init__(self,filename):
        self.filename = filename
        self.data = []
        with open(self.filename, 'rt') as f:
            for line in f:
                #entfernt unnötige Zeichen
                self.data.append(line.strip())
    
    def new(self):
        self.map = Map(os.path.join(
            game_folder, self.filename))
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
                    
#Scoreboard als class
class Score:
    def __init__(self, x, y, aktueller_score):
        self.aktueller_score = aktueller_score
        self.x = x
        self.y = y
        self.score_font = pygame.font.Font("freesansbold.ttf",24)
        self.score_rendered = self.score_font.render("Score: " + str(self.aktueller_score), True, (255,255,255))
    def update(self):
        self.aktueller_score += 1
        self.score_rendered = self.score_font.render("Score: " + str(self.aktueller_score), True, (255,255,255))

#Highscore 
class HighScore:
    def __init__(self,x,y,filename):
        self.x = x 
        self.y = y 
        self.filename = filename
        self.score = ""
        self.score_font = pygame.font.Font("freesansbold.ttf",24)
        self.highscorepath = os.path.join(game_folder,self.filename)
        self.lesen()
    def lesen(self):
        #In der Highscore Datei steht etwas
        if os.path.getsize(self.highscorepath) > 0:
            with open(self.filename, 'rt') as f:
                self.score = f.read()
                self.score_rendered = self.score_font.render("Highscore: " + self.score, True, (255,255,255))
        #Datei ist leer
        else:
            self.score = "0"
            self.score_rendered = self.score_font.render("Highscore: " + self.score, True, (255,255,255))
    def ueberschreiben(self,newscore):
        with open(self.filename, 'w') as f:
            f.write(str(newscore))
            self.newhighscore_rendered = self.score_font.render("Neuer Highscore: " + str(newscore), True, (0,0,0))



    
class CollisionDetector:
    def __init__(self,ball: Ball, spieler: Spieler, my_score: Score):
        self.ball = ball 
        self.spieler = spieler
        self.my_score = my_score
        self.time1 = 0
        self.time2 = 0


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
                self.my_score.update()
               
                #Block wird von unten auf der links Seite getroffen, während er von rechts kommt
                if((self.ball.sx > 0) and (self.ball.ball_rect.x + self.ball.image.get_width() <= sprite.block_rect.x + sprite.image.get_width()/2) ):
                    
                    
                    self.ball.sx *= -1
                #Block wird von unten auf der rechten Seite getroffen, während er von links kommt
                if((self.ball.sx < 0) and (self.ball.ball_rect.x >= sprite.block_rect.x + sprite.image.get_width()/2) ):
                    

                    self.ball.sx *= -1
                    
                
                #offset 1 nach unten
                self.ball.ball_rect.y += 4

                self.ball.sy *= -1
                
                #Block4 mit der Muenze wird getroffen, oder Block2 lässt Herzen fallen
                if sprite.id == 4 or sprite.id == 2:
                    sprite.hit()


                #Alle Blöcke werden zerstört außer Block3 ändert seine ID
                if(sprite.id == 3):
                    sprite.change()
                else:
                    sprites.remove(sprite)
                    
                
                
               
            #Ball trifft Block von oben
            elif self.ball.sy > 0 and (self.ball.ball_rect.y + self.ball.image.get_height() >= sprite.block_rect.y and self.ball.ball_rect.y <=  sprite.block_rect.y + sprite.image.get_height() ) and (self.ball.ball_rect.x + self.ball.image.get_width() >= sprite.block_rect.x and self.ball.ball_rect.x <= sprite.block_rect.x + sprite.image.get_width()):  
                self.my_score.update()
               
                
                #Block wird von unten auf der links Seite getroffen, während er von rechts kommt
                if((self.ball.sx > 0) and (self.ball.ball_rect.x + self.ball.image.get_width() <= sprite.block_rect.x + sprite.image.get_width()/2) ):
                    self.ball.sx *= -1
                #Block wird von unten auf der rechten Seite getroffen, während er von links kommt
                if((self.ball.sx < 0) and (self.ball.ball_rect.x >= sprite.block_rect.x + sprite.image.get_width()/2) ):
                    self.ball.sx *= -1

                #offset 1 nach oben
                self.ball.ball_rect.y -= 4
                self.ball.sy *= -1
                #Block4 mit der Muenze wird getroffen, oder Block2 lässt Herzen fallen
                if sprite.id == 4 or sprite.id == 2:
                    sprite.hit()

        
                #Alle Blöcke werden zerstört außer Block3 ändert seine ID
                if(sprite.id == 3):
                    
                    sprite.change()
                else:                   
                    sprites.remove(sprite)


                

            #Fallende Objekte Kollision mit Spieler oder unterem Rand
            for sprite in falling_sprites:
                #id der Münze
                if sprite.id == 5:
                    muenze_y = sprite.muenze_rect.y + sprite.image.get_height()
                    if muenze_y >= HEIGHT:
                        falling_sprites.remove(sprite)
                        print("HIT GROUND")
                    elif muenze_y >= self.spieler.plattform_rect.y and muenze_y <= self.spieler.plattform_rect.y + self.spieler.image.get_height() and sprite.muenze_rect.x + sprite.image.get_width() >= self.spieler.plattform_rect.x and sprite.muenze_rect.x <= self.spieler.plattform_rect.x + self.spieler.image.get_width():
                        falling_sprites.remove(sprite)
                        print("SCORE+1")
                        self.my_score.update()
                elif sprite.id == 6:
                    herz_y = sprite.herz_rect.y + sprite.image.get_height()
                    if herz_y >= HEIGHT:
                        falling_sprites.remove(sprite)
                        print("HIT GROUND")
                    elif herz_y >= self.spieler.plattform_rect.y and herz_y <= self.spieler.plattform_rect.y + self.spieler.image.get_height() and sprite.herz_rect.x + sprite.image.get_width() >= self.spieler.plattform_rect.x and sprite.herz_rect.x <= self.spieler.plattform_rect.x + self.spieler.image.get_width():
                        falling_sprites.remove(sprite)
                        print("HEART+1")
                        #maximal 6 Herzen
                        if self.spieler.leben < 6:
                            self.spieler.add_heart()
            
        #Leben werden abgezogen und der Ball ändert Position ausgerichtet nach dem Spieler
        if(self.ball.ball_rect.y >= HEIGHT - self.ball.image.get_height()):
            self.spieler.remove_heart()
            #Mitte des Spielers
            self.ball.ball_rect.x = self.spieler.plattform_rect.x + self.spieler.image.get_width() / 2 - self.ball.image.get_width() / 2
            self.ball.ball_rect.y = self.spieler.plattform_rect.y - 20
                

        
        






def game_loop():
    sprites.clear()
    #init
    spieler = Spieler(TastaturSteuerung_A_D())

    #Ball
    ball = Ball()
    
    #my_score Objekt wird erstellt
    my_score = Score(WIDTH/2, HEIGHT-36, 0)

    #highscore
    highscore = HighScore(WIDTH - 200,HEIGHT-36,'highscore/highscore.txt')

    #Collision
    collision = CollisionDetector(ball,spieler, my_score)

    #Map Liste
    map_liste = ['tile/map.txt','tile/map1.txt','tile/map2.txt']

    #Blöcke werden erstellt
    map_counter = 0
    map = Map(os.path.join(
                game_folder, map_liste[map_counter]))
    map.new()
    
    
    
    #Game Loop 
    
    running = True
    while running:

        #berechnet Zeit zwischen zwei Frames und limitiert diesen
        dt = clock.tick(FPS)
        # Schwarzer Hintergrund
        screen.fill(BLACK)

        #Spieler Bewegung
        spieler.steuerung()

        #Ball Bewegung
        ball.update()

        #collision
        collision.collision()

        #zeigt Highscore an
        screen.blit(highscore.score_rendered, (highscore.x,highscore.y))

        #zeigt Score an
        screen.blit(my_score.score_rendered, (my_score.x, my_score.y))

        #Malt die Plattform auf unsere Oberfläche mit den jeweiligen rect Werten Spieler
        screen.blit(spieler.image, spieler.plattform_rect)    

        screen.blit(ball.image, ball.ball_rect)  

        #Blöcke werden gemalt
        for sprite in sprites:
            screen.blit(sprite.image,sprite.block_rect)

        #Fallende Objekte werden gemalt
        for sprite in falling_sprites:
            sprite.update()
            #Münze
            if sprite.id == 5:
                screen.blit(sprite.image,sprite.muenze_rect)
            #Herz
            elif sprite.id == 6:
                screen.blit(sprite.image,sprite.herz_rect)

        #Leben werden gemalt
        for leben in spieler.leben_list:
             screen.blit(leben.image,leben.leben_rect)

        #Display wird geupdatet    
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
                pygame.quit()
                break
        
        #Nächste Level werden geladen
        if not sprites:
            map_counter += 1
            if map_counter < len(map_liste):
                map = Map(os.path.join(
                game_folder,map_liste[map_counter] ))
                #Mitte des Spielers
                ball.ball_rect.x = spieler.plattform_rect.x + spieler.image.get_width() / 2 - ball.image.get_width() / 2
                ball.ball_rect.y = spieler.plattform_rect.y - 20
                map.new()
                
            #Alle Level durchgespielt, Spiel ist zu Ende
            else:
                running = False
                print(running,"!!!!!!!!!!!!!!!!!")
                #Am Ende werden alle fallenden Objekte gelöscht.!!!
                falling_sprites.clear()
                #Neuer Highscore überprüft
                if my_score.aktueller_score > int(highscore.score):
                    highscore.ueberschreiben(my_score.aktueller_score)
                menuEnd.start(my_score,highscore)

        #Verloren
        if not spieler.leben_list:
            running = False
            falling_sprites.clear()
            print("überprüfung")
            print("Highscore: ",int(highscore.score),"score: ",my_score.aktueller_score)
            #Neuer Highscore überprüft
            if my_score.aktueller_score > int(highscore.score):
                print("überschrieben")
                highscore.ueberschreiben(my_score.aktueller_score)
            menuEnd.start(my_score,highscore)


            
            



class button:
    def __init__(self,x,y,pfad):
        self.x = x 
        self.y = y
        self.button_rect = ""
        self.image = ""
        self.pfad = pfad
        self.create()

    def create(self):
        
        self.image = pygame.image.load(os.path.join(
            game_folder, self.pfad)).convert_alpha() 
        self.button_rect = self.image.get_rect(center = (self.x,self.y))


class MenuStart:
    def __init__(self):
        pass

    def start(self):
        run = True
        buttonStart = button(WIDTH/2,100,"images/start.jpg")
        buttonEnd = button(WIDTH/2,400,"images/end.jpg")

        while run:

            screen.fill((192,192,192))

            screen.blit(buttonStart.image, buttonStart.button_rect)
            screen.blit(buttonEnd.image, buttonEnd.button_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                    pygame.quit()
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_x,position_y = pygame.mouse.get_pos()
                    if buttonStart.button_rect.collidepoint(position_x,position_y):
                        
                        run = False
                        game_loop()
                    
                    elif buttonEnd.button_rect.collidepoint(position_x,position_y):
                        run = False
                        pygame.quit()
                        break
class MenuEnd:
    def __init__(self):
        pass

    def start(self,score,highscore):
        run = True
        buttonStart = button(WIDTH/2,100,"images/nochmal.jpg")
        buttonEnd = button(WIDTH/2,400,"images/end.jpg")
        score.score_rendered = score.score_font.render("Score: " + str(score.aktueller_score), True, (0,0,0))
        highscore.score_rendered = highscore.score_font.render("Highscore: " + highscore.score, True, (0,0,0))


        while run:

            screen.fill((192,192,192))
            screen.blit(buttonStart.image, buttonStart.button_rect)
            screen.blit(buttonEnd.image, buttonEnd.button_rect)
            #Highscore und score anzeigen
            screen.blit(highscore.score_rendered, (WIDTH/2 - buttonStart.image.get_width()/2,500))
            screen.blit(score.score_rendered, (WIDTH/2- buttonStart.image.get_width()/2,550))
            #Wenn der Highscore geknackt wurde
            if score.aktueller_score > int(highscore.score):
                screen.blit(highscore.newhighscore_rendered, (WIDTH/2 - buttonStart.image.get_width()/2,600))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                    pygame.quit()
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_x,position_y = pygame.mouse.get_pos()
                    if buttonStart.button_rect.collidepoint(position_x,position_y):
                        print('clicked on image')
                        run = False
                        game_loop()
                    
                    elif buttonEnd.button_rect.collidepoint(position_x,position_y):
                        run = False
                        pygame.quit()
                        break
                


menuStart = MenuStart()
menuEnd = MenuEnd()
menuStart.start()

