import pygame

import player
import balls
import scores
import gamesettings
import soundsettings


class CollisionDetector:
    def __init__(self,ball: balls.Ball, spieler: player.Player, my_score: scores.Score):
        self.ball = ball 
        self.spieler = spieler
        self.my_score = my_score
        self.time1 = 0
        self.time2 = 0

    def collision(self):          
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



        for sprite in gamesettings.sprites:
        
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
                    gamesettings.sprites.remove(sprite)
                #Block 1 und Block 3 Sound
                if(sprite.id == 3 or sprite.id ==1):
                    pygame.mixer.Sound.play(soundsettings.hit_sound)
                    
                
                
               
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
                    gamesettings.sprites.remove(sprite)
                #Block 1 und Block 3 Sound
                if(sprite.id == 3 or sprite.id ==1):
                    pygame.mixer.Sound.play(soundsettings.hit_sound)

            #Fallende Objekte Kollision mit Spieler oder unterem Rand
            for sprite in gamesettings.falling_sprites:
                #id der Münze
                if sprite.id == 5:
                    muenze_y = sprite.muenze_rect.y + sprite.image.get_height()
                    if muenze_y >= gamesettings.HEIGHT:
                        gamesettings.falling_sprites.remove(sprite)
                    elif muenze_y >= self.spieler.plattform_rect.y and muenze_y <= self.spieler.plattform_rect.y + self.spieler.image.get_height() and sprite.muenze_rect.x + sprite.image.get_width() >= self.spieler.plattform_rect.x and sprite.muenze_rect.x <= self.spieler.plattform_rect.x + self.spieler.image.get_width():
                        gamesettings.falling_sprites.remove(sprite)
                        self.my_score.update()
                elif sprite.id == 6:
                    herz_y = sprite.herz_rect.y + sprite.image.get_height()
                    if herz_y >= gamesettings.HEIGHT:
                        gamesettings.falling_sprites.remove(sprite)
                    elif herz_y >= self.spieler.plattform_rect.y and herz_y <= self.spieler.plattform_rect.y + self.spieler.image.get_height() and sprite.herz_rect.x + sprite.image.get_width() >= self.spieler.plattform_rect.x and sprite.herz_rect.x <= self.spieler.plattform_rect.x + self.spieler.image.get_width():
                        gamesettings.falling_sprites.remove(sprite)
                        self.spieler.add_heart()
            
        #Leben werden abgezogen und der Ball ändert Position ausgerichtet nach dem Spieler
        if(self.ball.ball_rect.y >= gamesettings.HEIGHT - self.ball.image.get_height()):
            self.spieler.remove_heart()
            #Mitte des Spielers
            self.ball.ball_rect.x = self.spieler.plattform_rect.x + self.spieler.image.get_width() / 2 - self.ball.image.get_width() / 2
            self.ball.ball_rect.y = self.spieler.plattform_rect.y - 20
            #Sound Lebensverlust
            pygame.mixer.Sound.play(soundsettings.brick_sound)
                

        
        

