import pygame
import os

import gamesettings

#Herzen unten nicht zu verwechseln mit fallenden Herzen, da sie das gleiche Bild haben
class Leben:
    def __init__(self,x,y):
        self.x = x 
        self.y = y 
        self.image = ""
        self.block_rect = ""
        self.create()
    
    def create(self):
        self.image = pygame.image.load(os.path.join(
        gamesettings.game_folder, 'images/heart.png')).convert_alpha() 
        self.leben_rect = self.image.get_rect(center = (self.x,self.y))
        