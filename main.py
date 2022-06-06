import pygame
import os

#Meine Module

import gamesettings 

#Command pattern imports
import tastaturinvoker 
from icommandabstract import *
import icommand

#Observer pattern
import scores
import observer
from observersubjectabstract import *
from observerabstract import *
import highscors
import leben as myleben

import collisiondetectors
import player
import balls
import maps

#Startet das Spiel
import menustart

def game_loop():
    gamesettings.sprites.clear()

    #Musik spielen
    pygame.mixer.music.play(-1,0.0)
    #Lautstärke Hintergrundmusik
    pygame.mixer.music.set_volume(.6)

    #init spieler receiver
    spieler = player.Player()
    #Invoker
    tastatur = tastaturinvoker.Tastatur()

    #Kommandos
    move_left = icommand.MoveLeft(spieler)
    move_right = icommand.MoveRight(spieler)

    #Commands werden registriert im Invoker
    tastatur.register(move_right,pygame.K_d)
    tastatur.register(move_left,pygame.K_a)

    #Observer Pattern registrieren
    spieler.register(observer.UnterMaximalenLeben())
    spieler.register(observer.LebenVerlierenMoeglich())

    #highscore
    highscore = highscors.HighScore(gamesettings.WIDTH - 200,gamesettings.HEIGHT-36,'highscore/highscore.txt')
    #my_score Objekt wird erstellt
    my_score = scores.Score(gamesettings.WIDTH/2, gamesettings.HEIGHT-36, 0, highscore)
    #Observer Pattern HighScore
    my_score.register(observer.HighScoreUeberschritten())

    #Ball
    ball = balls.Ball()

    #highscore
    highscore = highscors.HighScore(gamesettings.WIDTH - 200,gamesettings.HEIGHT-36,'highscore/highscore.txt')
    
    #my_score Objekt wird erstellt
    my_score = scores.Score(gamesettings.WIDTH/2, gamesettings.HEIGHT-36, 0, highscore)
    #Observer Pattern HighScore
    my_score.register(observer.HighScoreUeberschritten())


    #Collision
    collision = collisiondetectors.CollisionDetector(ball,spieler, my_score)

    #Map Liste
    map_liste = ['tile/map.txt','tile/map1.txt','tile/map2.txt','tile/map3.txt']

    #Blöcke werden erstellt
    map_counter = 0
    map = maps.Map(os.path.join(
                gamesettings.game_folder, map_liste[map_counter]))
    map.new()
    
    
    
    #Game Loop 
    
    running = True
    while running:

        #Max. FPS
        gamesettings.clock.tick(gamesettings.FPS)
        # Schwarzer Hintergrund
        gamesettings.screen.fill(gamesettings.BLACK)

        #Unsere Tastatur wird ausgelöst
        keys = pygame.key.get_pressed()
        tastatur.execute(keys)

        #Ball Bewegung
        ball.update()

        #collision
        collision.collision()

        #zeigt Highscore an
        gamesettings.screen.blit(highscore.score_rendered, (highscore.x,highscore.y))

        #zeigt Score an
        gamesettings.screen.blit(my_score.score_rendered, (my_score.x - my_score.text_width/2, my_score.y))

        #Malt die Plattform auf unsere Oberfläche mit den jeweiligen rect Werten Spieler
        gamesettings.screen.blit(spieler.image, spieler.plattform_rect)    

        gamesettings.screen.blit(ball.image, ball.ball_rect)  

        #Blöcke werden gezeichnet
        for sprite in gamesettings.sprites:
            gamesettings.screen.blit(sprite.image,sprite.block_rect)

        #Fallende Objekte werden gemalt
        for sprite in gamesettings.falling_sprites:
            sprite.update()
            #Münze
            if sprite.id == 5:
                gamesettings.screen.blit(sprite.image,sprite.muenze_rect)
            #Herz
            elif sprite.id == 6:
                gamesettings.screen.blit(sprite.image,sprite.herz_rect)

        #Leben werden gemalt unten links
        for myleben.leben in spieler.leben_list:
             gamesettings.screen.blit(myleben.leben.image,myleben.leben.leben_rect)

        #Display wird geupdatet    
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
                pygame.quit()
                break
        
        #Nächste Level werden geladen
        if not gamesettings.sprites:
            map_counter += 1
            if map_counter < len(map_liste):
                map = maps.Map(os.path.join(
                gamesettings.game_folder,map_liste[map_counter] ))
                #Mitte des Spielers
                ball.ball_rect.x = spieler.plattform_rect.x + spieler.image.get_width() / 2 - ball.image.get_width() / 2
                ball.ball_rect.y = spieler.plattform_rect.y - 20
                map.new()
                
            #Alle Level durchgespielt, Spiel ist zu Ende
            else:
                running = False
                #Am Ende werden alle fallenden Objekte gelöscht.!!!
                gamesettings.falling_sprites.clear()  
                menustart.menuEnds.start(my_score,highscore)

        #Verloren
        if spieler.verloren:
            running = False
            gamesettings.falling_sprites.clear()
            menustart.menuEnds.start(my_score,highscore)


            
        
                
