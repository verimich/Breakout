from icommandabstract import *
import player

""""
Hier befinden sich die Commands für das CommandPattern.
"""
#Bewegung nach links
class MoveLeft(ICommand):
    def __init__(self,spieler: player.Player):
        self.spieler = spieler
    
    def execute(self):
        self.spieler.move_left()

#Bewegung nach rechts
class MoveRight(ICommand):
    def __init__(self,spieler: player.Player):
        self.spieler = spieler
    
    def execute(self):
        self.spieler.move_right()