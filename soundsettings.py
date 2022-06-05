import pygame

#Hintergrundmusik und Sounds #pygame.mixer.music.stop() falls ausstellfunktion
hit_sound = pygame.mixer.Sound("sounds/Ball_Bounce-Popup_Pixels-172648817.wav")
heart_sound = pygame.mixer.Sound("sounds/success-1-6297.wav")
brick_sound = pygame.mixer.Sound("sounds/Large Thump Or Bump-SoundBible.com-395560493.wav")
muenze_sound = pygame.mixer.Sound("sounds/announcement-sound-4-21464.wav")
backroundplaylist = list()
backroundplaylist.append ("sounds/LevelIV.wav")
backroundplaylist.append ("sounds/LevelII.wav")
backroundplaylist.append ("sounds/LevelIII.wav")
backroundplaylist.append ("sounds/LevelIV.wav")
backroundplaylist.append ("sounds/LevelI.wav")
backround_sound = pygame.mixer.music.load(backroundplaylist.pop())
pygame.mixer.music.queue (backroundplaylist.pop()) #queque den nächsten backroundsong