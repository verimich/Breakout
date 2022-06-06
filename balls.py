import pygame
import os

import gamesettings

class Ball():
    def __init__(self):
        self.image = pygame.image.load(os.path.join(
            gamesettings.game_folder, 'images\meinball3.png')).convert_alpha()
        self.bx = gamesettings.screen.get_rect().centerx
        self.by = gamesettings.HEIGHT - 70 
        
        self.ball_rect = self.image.get_rect(center = (self.bx,self.by))

        self.sx = 4
        self.sy = 4

    def update(self):
        self.ball_rect.x += self.sx
        self.ball_rect.y += self.sy

        linkerRand = 0
        
        rechterRand = gamesettings.WIDTH - self.image.get_width()

        # unterer Rand
        if(self.ball_rect.y >= gamesettings.HEIGHT - self.image.get_height() and self.sy > 0): 
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