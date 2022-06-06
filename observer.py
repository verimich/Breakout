from observerabstract import *
import gamesettings 
import leben 


#Leben hinzufügen Observer
class UnterMaximalenLeben(Observer):
    def update(self, subject: ObserverSubject,message):
        #Gibt ein Herz hinzu
        if subject.leben <= subject.maxhealth and message == "add":
            subject.leben_list.append(leben.Leben(subject.leben*25,gamesettings.HEIGHT-25))
        elif message == "add":
            subject.leben = subject.maxhealth

#Leben verlieren Observer
class LebenVerlierenMoeglich(Observer):
    def update(self,subject,message):
        if subject.leben > 0 and message == "remove":
            del subject.leben_list[-1]
        elif message == "remove":
            subject.verloren = True

#Observer für Highscore
class HighScoreUeberschritten(Observer):
    def update(self, subject:ObserverSubject, highscore):
        if subject.aktueller_score > int(highscore.score):
            highscore.ueberschreiben(subject.aktueller_score) 
            #Am Ende des Spiels im MenuEnd wird überprüft, ob der neue Highscore angezeigt werden kann
            highscore.uebertroffen = True           
