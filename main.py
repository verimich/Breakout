from turtle import width
import pygame
import os
from abc import ABC, ABCMeta, abstractmethod
import time


from gamesettings import *
from soundsettings import *
from observersubjectabstract import *
from observerabstract import *

from leben import *
import observer
import player

#Command pattern imports
from tastaturinvoker import *
from icommandabstract import *
import icommand

import balls

import maps

#Observer pattern
import scores

import highscors
import collisiondetectors


import starting

def game_loop():
    sprites.clear()

    #Musik spielen
    pygame.mixer.music.play(-1,0.0)
    #Lautstärke Hintergrundmusik
    pygame.mixer.music.set_volume(.6)

    #init spieler
    spieler = player.Player()
    #Invoker
    tastatur = Tastatur()

    #Kommandos
    move_left = icommand.MoveLeft(spieler)
    move_right = icommand.MoveRight(spieler)

    #Commands werden registriert im Invoker
    tastatur.register(move_right,pygame.K_d)
    tastatur.register(move_left,pygame.K_a)

    #Observer Pattern registrieren
    spieler.register(observer.UnterMaximalenLeben())
    spieler.register(observer.LebenVerlierenMoeglich())
    

    #Ball
    ball = balls.Ball()

    #highscore
    highscore = highscors.HighScore(WIDTH - 200,HEIGHT-36,'highscore/highscore.txt')
    
    #my_score Objekt wird erstellt
    my_score = scores.Score(WIDTH/2, HEIGHT-36, 0, highscore)

    

    #Observer Pattern HighScore
    my_score.register(observer.HighScoreUeberschritten())


    #Collision
    collision = collisiondetectors.CollisionDetector(ball,spieler, my_score)

    #Map Liste
    map_liste = ['tile/map.txt','tile/map1.txt','tile/map2.txt']

    #Blöcke werden erstellt
    map_counter = 0
    map = maps.Map(os.path.join(
                gamesettings.game_folder, map_liste[map_counter]))
    map.new()
    
    
    
    #Game Loop 
    
    running = True
    while running:

        #berechnet Zeit zwischen zwei Frames und limitiert diesen
        dt = clock.tick(FPS)
        # Schwarzer Hintergrund
        screen.fill(BLACK)

        #Unsere Tastatur wird ausgelöst
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
                map = maps.Map(os.path.join(
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
                starting.menuEnds.start(my_score,highscore)

        #Verloren
        if spieler.verloren:
            running = False
            falling_sprites.clear()
            print("überprüfung")
            print("Highscore: ",int(highscore.score),"score: ",my_score.aktueller_score)
            starting.menuEnds.start(my_score,highscore)


            
        
                
