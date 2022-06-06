import pygame
import os

import gamesettings
#Highscore 
class HighScore:
    def __init__(self,x,y,filename):
        self.x = x 
        self.y = y 
        self.filename = filename
        self.score = ""
        self.score_font = pygame.font.Font("freesansbold.ttf",24)
        self.highscorepath = os.path.join(gamesettings.game_folder,self.filename)
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
    #Highscore wird überschrieben
    def ueberschreiben(self,newscore):
        with open(self.filename, 'w') as f:
            f.write(str(newscore))
            self.newhighscore_rendered = self.score_font.render("Neuer Highscore: " + str(newscore), True, (0,0,0))
