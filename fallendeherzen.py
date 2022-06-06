import pygame
import os
import gamesettings
import soundsettings

""""
Dies ist die Klasse der fallenden Herzen, welche in falling_sprites gespiechert wird.
Die Fallgeschwindkeit für y beträgt 6px und kann angepasst werden.
"""
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
        pygame.mixer.Sound.play(soundsettings.muenze_sound)
        self.image = pygame.image.load(os.path.join(
        gamesettings.game_folder, 'images/heart.png')).convert_alpha() 
        self.y += self.image.get_height()/2
        self.herz_rect = self.image.get_rect(center = (self.x,self.y))
        
    def update(self):
        self.herz_rect.y += self.ys