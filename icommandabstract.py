from abc import ABC, ABCMeta, abstractmethod

""""
Dies ist die abstrakte Klasse für die Commands im Command Pattern
"""
class ICommand(metaclass=ABCMeta):
    @abstractmethod
    def execute():
        pass