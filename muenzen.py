import pygame
import os
from abc import ABC, ABCMeta, abstractmethod

import soundsettings
import gamesettings

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
        
        pygame.mixer.Sound.play(soundsettings.muenze_sound)  
        self.image = pygame.image.load(os.path.join(
        gamesettings.game_folder, 'images/coin.png')).convert_alpha() 
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
        pygame.mixer.Sound.play(soundsettings.muenze_sound)
        self.image = pygame.image.load(os.path.join(
        gamesettings.game_folder, 'images/heart.png')).convert_alpha() 
        self.y += self.image.get_height()/2
        self.herz_rect = self.image.get_rect(center = (self.x,self.y))
        
    def update(self):
        self.herz_rect.y += self.ys

