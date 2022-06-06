
""""
Dies ist der Invoker im CommandPattern. Alle Kommandos werden registriert im dictionary.
Falls die gedrückte Taste vorhanden ist, wird der jeweilige command aufgerufen.
"""
#Invoker für Command Pattern
class Tastatur:

    def __init__(self):
        self.commands = {}

    def register(self,command,command_taste):
        self.commands[command] = command_taste

    def execute(self,keys):
        for command,command_taste in self.commands.items():
            if keys[command_taste]:
                command.execute()