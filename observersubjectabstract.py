import pygame
from abc import ABC, ABCMeta, abstractmethod

#Observer Pattern OberserverSubject Basisklasse
class ObserverSubject(metaclass=ABCMeta):
    def __init__(self):
        self._observers = []
    
    def register(self, observer):
        self._observers.append(observer)
    
    def unregister(self, observer):
        self._observers.remove(observer)
    
    def _notify(self):
        for observer in self._observers:
            observer.update(self)