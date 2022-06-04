from turtle import width
import pygame
import os
from abc import ABC, ABCMeta, abstractmethod
import time

#init pygame
pygame.init()
clock = pygame.time.Clock()

#Hintergrundmusik und Sounds #pygame.mixer.music.stop() falls ausstellfunktion
hit_sound = pygame.mixer.Sound("sounds/Ball_Bounce-Popup_Pixels-172648817.wav")
heart_sound = pygame.mixer.Sound("sounds/success-1-6297.wav")
brick_sound = pygame.mixer.Sound("sounds/Large Thump Or Bump-SoundBible.com-395560493.wav")
muenze_sound = pygame.mixer.Sound("sounds/announcement-sound-4-21464.wav")
backroundplaylist = list()
backroundplaylist.append ("sounds/LevelIV.wav")
backroundplaylist.append ("sounds/LevelII.wav")
backroundplaylist.append ("sounds/LevelIII.wav")
backroundplaylist.append ("sounds/LevelIV.wav")
backroundplaylist.append ("sounds/LevelI.wav")
backround_sound = pygame.mixer.music.load(backroundplaylist.pop())
pygame.mixer.music.queue (backroundplaylist.pop()) #queque den nächsten backroundsong

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

#Observer Pattern OberserverSubject Basisklasse
class ObserverSubject(metaclass=ABCMeta):
    def __init__(self):
        self._observers = []
    
    def register(self, observer):
        self._observers.append(observer)
    
    def unregister(self, observer):
        self._observers.remove(observer)
    
    def _notify(self):
        for observer in self._observers:
            observer.update(self)

#Basis Klasse für die Observer im Observer Pattern
class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, subject: ObserverSubject):
        pass

#Leben hinzufügen Observer
class UnterMaximalenLeben(Observer):
    def update(self, subject: ObserverSubject,message):
        if subject.leben <= subject.maxhealth and message == "add":
            print(subject.maxhealth," ",subject.leben)
            print("HEART ADDED UnterMaximalenLeben")
            subject.leben_list.append(Leben(subject.leben*25,HEIGHT-25))
        elif message == "add":
            subject.leben = subject.maxhealth
        

#Leben verlieren Observer
class LebenVerlierenMoeglich(Observer):
    def update(self,subject,message):
        if subject.leben > 0 and message == "remove":
            del subject.leben_list[-1]
        elif message == "remove":
            subject.verloren = True


#Im Observer Pattern ist dies das ObserverSubject
#Im Command Pattern ist dies der Receiver
class Spieler(ObserverSubject):
    def __init__(self):
        self._observers = []
        #Bild laden
        self.image = pygame.image.load(os.path.join(
            game_folder, 'images\glasspaddle1.png')).convert_alpha()
        #Bildgegröße bestimmen und Position, start x Mitte, y 650
        self.plattform_rect = self.image.get_rect(center = (screen.get_rect().centerx,HEIGHT - 45 ))
        #Bewegungsgeschwindigkeit
        self.speed = 10
        #Plattform Breite
        self.plattform_width = self.image.get_width()
        #Leben
        self.leben = 3
        self.leben_list = []
        self.maxhealth = 6
        #Spiel verloren
        self.verloren = False
        #message für das Observer pattern
        self.message = ""
        #Herzen werden einmal erstellt
        self._create_hearts()

    #Bewegung nach rechts für das Command Pattern
    def move_right(self):
        rechterRand = WIDTH - self.plattform_width
        if self.plattform_rect.x < rechterRand:
            self.plattform_rect.x += self.speed 
    
    #Bewegung nach links für das Command Pattern
    def move_left(self):
        linkerRand = 0
        if self.plattform_rect.x > linkerRand:
            self.plattform_rect.x -= self.speed
    
    def _create_hearts(self):
        for i in range(0,self.leben):
            self.leben_list.append(Leben(i*25 + 25,HEIGHT-25))
    
    def add_heart(self):
        self.leben += 1
        self.message = "add"
        print("HEART ADDED in Spieler Klasse")
        self._notify()
    
    def remove_heart(self):
        self.leben -= 1
        self.message = "remove"
        self._notify()
    
    #Methoden für das Observer Pattern
    def register(self, observer):
        self._observers.append(observer)
    
    def unregister(self, observer):
        self._observers.remove(observer)
    
    def _notify(self):
        for observer in self._observers:
            observer.update(self,self.message)


#Invoker für Command Pattern
class Tastatur:

    def __init__(self):
        self.commands = {}

    def register(self,command,command_taste):
        self.commands[command] = command_taste

    def execute(self,keys):
        for command,command_taste in self.commands.items():
            if keys[command_taste]:
                command.execute()

#Command abtrakte Klasse für das Command Pattern
class ICommand(metaclass=ABCMeta):

    @abstractmethod
    def execute():
        pass

#Bewegung nach links
class MoveLeft(ICommand):
    def __init__(self,spieler: Spieler):
        self.spieler = spieler
    
    def execute(self):
        self.spieler.move_left()

#Bewegung nach rechts
class MoveRight(ICommand):
    def __init__(self,spieler: Spieler):
        self.spieler = spieler
    
    def execute(self):
        self.spieler.move_right()
        
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
        #Sound bei Muenzgeneration
        
        pygame.mixer.Sound.play(muenze_sound)  
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
        #Sound Herz wird generiert
        pygame.mixer.Sound.play(muenze_sound)
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
#Observersubject im Comandpattern
class Score(ObserverSubject):
    def __init__(self, x, y, aktueller_score, highscore):
        self.highscore = highscore
        ObserverSubject.__init__(self)
        self.aktueller_score = aktueller_score
        self.x = x
        self.y = y
        self.score_font = pygame.font.Font("freesansbold.ttf",24)
        self.score_rendered = self.score_font.render("Score: " + str(self.aktueller_score), True, (255,255,255))
    def update(self):
        self.aktueller_score += 1
        self.score_rendered = self.score_font.render("Score: " + str(self.aktueller_score), True, (255,255,255))

    def register(self, observer:Observer):
        self._observers.append(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self, self.highscore)

class HighScoreUeberschritten(Observer):
    def update(self, subject:ObserverSubject, highscore):
        if subject.aktueller_score > int(highscore.score):
            highscore.ueberschreiben(subject.aktueller_score) 
            highscore.uebertroffen = True           


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
        self.uebertroffen = False
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


    def collision(self):        
        #Musik ersetzen durch Sound
        #pygame.mixer.music.stop()
        #pygame.mixer.Sound.play(hit_sound)  
                                                                                              #Linke Ecke                                                                #Rechte Ecke
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
                #Block 1 und Block 3 Sound
                if(sprite.id == 3 or sprite.id ==1):
                    pygame.mixer.Sound.play(hit_sound)
                    
                
                
               
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
                #Block 1 und Block 3 Sound
                if(sprite.id == 3 or sprite.id ==1):
                    pygame.mixer.Sound.play(hit_sound)


                

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
                    
                        self.spieler.add_heart()
            
        #Leben werden abgezogen und der Ball ändert Position ausgerichtet nach dem Spieler
        if(self.ball.ball_rect.y >= HEIGHT - self.ball.image.get_height()):
            print("REMOVE_HEART()")
            self.spieler.remove_heart()
            #Mitte des Spielers
            self.ball.ball_rect.x = self.spieler.plattform_rect.x + self.spieler.image.get_width() / 2 - self.ball.image.get_width() / 2
            self.ball.ball_rect.y = self.spieler.plattform_rect.y - 20
            #Sound Lebensverlust
            pygame.mixer.Sound.play(brick_sound)
                

        
        






def game_loop():
    sprites.clear()

    #Musik spielen
    pygame.mixer.music.play(-1,0.0)
    #Lautstärke Hintergrundmusik
    pygame.mixer.music.set_volume(.6)

    #init spieler
    spieler = Spieler()
    #Invoker
    tastatur = Tastatur()

    #Kommandos
    move_left = MoveLeft(spieler)
    move_right = MoveRight(spieler)

    #Commands werden registriert im Invoker
    tastatur.register(move_right,pygame.K_d)
    tastatur.register(move_left,pygame.K_a)

    #Observer Pattern registrieren
    spieler.register(UnterMaximalenLeben())
    spieler.register(LebenVerlierenMoeglich())
    

    #Ball
    ball = Ball()

    #highscore
    highscore = HighScore(WIDTH - 200,HEIGHT-36,'highscore/highscore.txt')
    
    #my_score Objekt wird erstellt
    my_score = Score(WIDTH/2, HEIGHT-36, 0, highscore)

    

    #Observer Pattern HighScore
    my_score.register(HighScoreUeberschritten())


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

        #Unser Tastatur wird ausgelöst
        keys = pygame.key.get_pressed()
        tastatur.execute(keys)

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
                menuEnd.start(my_score,highscore)

        #Verloren
        if spieler.verloren:
            running = False
            falling_sprites.clear()
            print("überprüfung")
            print("Highscore: ",int(highscore.score),"score: ",my_score.aktueller_score)
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
        pygame.mixer.music.stop()
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
        pygame.mixer.music.stop()
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
            if highscore.uebertroffen: 
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

