from abc import ABC, ABCMeta, abstractmethod
import pygame
import os

import gamesettings
import fallendeherzen
import muenzen

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
            gamesettings.game_folder, 'images/brick1_tile.jpg')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))
        self.id = 1

#Block Klasse
class Block2(Block):
    def __init__(self,bx,by):
        self.image = pygame.image.load(os.path.join(
            gamesettings.game_folder, 'images/brick2_tile.jpg')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))
        self.id = 2
    
    def hit(self):
        gamesettings.falling_sprites.append(fallendeherzen.FallendesHerz(self.block_rect.x + self.image.get_width()/2,self.block_rect.y + self.image.get_height()))

#Block Klasse
class Block3(Block):
    def __init__(self,bx,by):
        self.image = pygame.image.load(os.path.join(
            gamesettings.game_folder, 'images/brick3.png')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))
        self.id = 3

    def change(self):
        self.id = 1
        self.image = pygame.image.load(os.path.join(
            gamesettings.game_folder, 'images/brick1_tile.jpg')).convert_alpha()

        
    

#Block Klasse
class Block4(Block):
    def __init__(self,bx,by):
        self.image = pygame.image.load(os.path.join(
            gamesettings.game_folder, 'images/brick4.png')).convert_alpha() 
        self.block_rect = self.image.get_rect(center = (bx,by))
        self.id = 4
    
    def hit(self):
        gamesettings.falling_sprites.append(muenzen.Muenze(self.block_rect.x + self.image.get_width()/2,self.block_rect.y + self.image.get_height()))
