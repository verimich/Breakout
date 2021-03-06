from observersubjectabstract import *
import observer

""""
Unser Score wird jedes mal erhöht, wenn der Ball einen Block trifft, oder eine Münze gefangen wird. 
Subject im Observer Pattern.
Enthält die typischen Methoden.
"""
class Score(ObserverSubject):
    def __init__(self, x, y, aktueller_score, highscore):
        self.highscore = highscore
        ObserverSubject.__init__(self)
        self.aktueller_score = aktueller_score
        self.x = x
        self.y = y
        self.score_font = pygame.font.Font("freesansbold.ttf",24)
        self.text_width, self.text_height = self.score_font.size("Score:  ")
        self.score_rendered = self.score_font.render("Score: " + str(self.aktueller_score), True, (255,255,255))
    def update(self):
        self.aktueller_score += 1
        self.score_rendered = self.score_font.render("Score: " + str(self.aktueller_score), True, (255,255,255))
        self._notify()

    def register(self, observer:observer.Observer):
        self._observers.append(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self, self.highscore)