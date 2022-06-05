import pygame

import gamesettings
import leben
import os
from observersubjectabstract import *

#Im Observer Pattern ist dies das ObserverSubject
#Im Command Pattern ist dies der Receiver
class Player(ObserverSubject):
    def __init__(self):
        self._observers = []
        #Bild laden
        self.image = pygame.image.load(os.path.join(
            gamesettings.game_folder, 'images\glasspaddle1.png')).convert_alpha()
        #Bildgegröße bestimmen und Position, start x Mitte, y 650
        self.plattform_rect = self.image.get_rect(center = (gamesettings.screen.get_rect().centerx,gamesettings.HEIGHT - 45 ))
        #Bewegungsgeschwindigkeit
        self.speed = 10
        #Plattform Breite
        self.plattform_width = self.image.get_width()
        #Leben
        self.leben = 3
        self.leben_list = []
        self.maxhealth = 6
        #Spiel verloren
        self.verloren = False
        #message für das Observer pattern
        self.message = ""
        #Herzen werden einmal erstellt
        self._create_hearts()

    #Bewegung nach rechts für das Command Pattern
    def move_right(self):
        rechterRand = gamesettings.WIDTH - self.plattform_width
        if self.plattform_rect.x < rechterRand:
            self.plattform_rect.x += self.speed 
    
    #Bewegung nach links für das Command Pattern
    def move_left(self):
        linkerRand = 0
        if self.plattform_rect.x > linkerRand:
            self.plattform_rect.x -= self.speed
    
    def _create_hearts(self):
        for i in range(0,self.leben):
            self.leben_list.append(leben.Leben(i*25 + 25,gamesettings.HEIGHT-25))
    
    def add_heart(self):
        self.leben += 1
        self.message = "add"
        print("HEART ADDED in Spieler Klasse")
        self._notify()
    
    def remove_heart(self):
        self.leben -= 1
        self.message = "remove"
        self._notify()
    
    #Methoden für das Observer Pattern
    def register(self, observer):
        self._observers.append(observer)
    
    def unregister(self, observer):
        self._observers.remove(observer)
    
    def _notify(self):
        for observer in self._observers:
            observer.update(self,self.message)