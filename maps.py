import os

import gamesettings
import bloecke

#TileMap Klasse erstellt die jeweiligen Blöcke
class Map:
    def __init__(self,filename):
        self.filename = filename
        self.data = []
        with open(self.filename, 'rt') as f:
            for line in f:
                #entfernt unnötige Zeichen
                self.data.append(line.strip())
    
    def new(self):
        self.map = Map(os.path.join(
            gamesettings.game_folder, self.filename))
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    gamesettings.sprites.append(bloecke.Block1(col * 50 + 25,row * 50 + 25))
                if tile == '2':
                    gamesettings.sprites.append(bloecke.Block2(col * 50 +25,row*50 +25))
                if tile == '3':
                    gamesettings.sprites.append(bloecke.Block3(col * 50 +25,row*50 +25))
                if tile == '4':
                    gamesettings.sprites.append(bloecke.Block4(col * 50 +25,row*50 +25))