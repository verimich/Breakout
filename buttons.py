import pygame
import os

import gamesettings

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
            gamesettings.game_folder, self.pfad)).convert_alpha() 
        self.button_rect = self.image.get_rect(center = (self.x,self.y))
