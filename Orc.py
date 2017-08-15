from unite import *
from Data import *

class Orc (unite):
    def __init__(self,joueur):
        unite.__init__(self,joueur)
        self.vitesseMax = 6
        self.vitesseCourante = 6
        self.name = orcString
        self.initiativeCourante = 7
        self.initiativeMax = 7

