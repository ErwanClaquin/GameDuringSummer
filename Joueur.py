from Orc import *
from Soldat import *

class joueur :
    def __init__(self, couleur, name, leftPlateau):
        self.couleur = couleur
        self.armee = []
        self.armeeMax = 3
        self.name = name
        self.leftPlateau = leftPlateau

    def addUnite(self, type, x, y, joueur):
        if len(self.armee) <= self.armeeMax:
            if type == orcString:
                orc = Orc(joueur)
                orc.setCoord(x, y)
                self.armee.append(orc)


            elif type == soldatString:
                soldat = Soldat(joueur)
                soldat.setCoord(x, y)
                self.armee.append(soldat)


    def sensImage(self):
        return self.leftPlateau
