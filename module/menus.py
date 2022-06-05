import pygame 

import buttons
import gamesettings

import main





class MenuStart:
    def __init__(self):
        print("init")
        pass

    def start(self):
        pygame.mixer.music.stop()
        run = True
        buttonStart = buttons.button(gamesettings.WIDTH/2,100,"images/start.jpg")
        buttonEnd = buttons.button(gamesettings.WIDTH/2,400,"images/end.jpg")

        while run:

            gamesettings.screen.fill((192,192,192))

            gamesettings.screen.blit(buttonStart.image, buttonStart.button_rect)
            gamesettings.screen.blit(buttonEnd.image, buttonEnd.button_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                    pygame.quit()
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_x,position_y = pygame.mouse.get_pos()
                    if buttonStart.button_rect.collidepoint(position_x,position_y):
                        
                        run = False
                        main.game_loop()
                    
                    elif buttonEnd.button_rect.collidepoint(position_x,position_y):
                        run = False
                        pygame.quit()
                        break


class MenuEnd:
    def __init__(self):
        pass

    def start(self,score,highscore):
        pygame.mixer.music.stop()
        run = True
        buttonStart = buttons.button(gamesettings.WIDTH/2,100,"images/nochmal.jpg")
        buttonEnd = buttons.button(gamesettings.WIDTH/2,400,"images/end.jpg")
        score.score_rendered = score.score_font.render("Score: " + str(score.aktueller_score), True, (0,0,0))
        highscore.score_rendered = highscore.score_font.render("Highscore: " + highscore.score, True, (0,0,0))


        while run:

            gamesettings.screen.fill((192,192,192))
            gamesettings.screen.blit(buttonStart.image, buttonStart.button_rect)
            gamesettings.screen.blit(buttonEnd.image, buttonEnd.button_rect)
            #Highscore und score anzeigen
            gamesettings.screen.blit(highscore.score_rendered, (gamesettings.WIDTH/2 - buttonStart.image.get_width()/2,500))
            gamesettings.screen.blit(score.score_rendered, (gamesettings.WIDTH/2- buttonStart.image.get_width()/2,550))
            #Wenn der Highscore geknackt wurde
            if highscore.uebertroffen: 
                gamesettings.screen.blit(highscore.newhighscore_rendered, (gamesettings.WIDTH/2 - buttonStart.image.get_width()/2,600))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                    pygame.quit()
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_x,position_y = pygame.mouse.get_pos()
                    if buttonStart.button_rect.collidepoint(position_x,position_y):
                        print('clicked on image')
                        run = False
                        main.game_loop()
                    
                    elif buttonEnd.button_rect.collidepoint(position_x,position_y):
                        run = False
                        pygame.quit()
                        break