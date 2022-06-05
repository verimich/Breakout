from abc import ABC, ABCMeta, abstractmethod
from observersubjectabstract import *

#Basis Klasse für die Observer im Observer Pattern
class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, subject: ObserverSubject):
        pass