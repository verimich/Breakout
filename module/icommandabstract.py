from abc import ABC, ABCMeta, abstractmethod

#Command abtrakte Klasse für das Command Pattern
class ICommand(metaclass=ABCMeta):

    @abstractmethod
    def execute():
        pass