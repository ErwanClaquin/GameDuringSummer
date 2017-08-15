from unite import *
from Data import *

class Soldat (unite):

    def __init__(self,joueur):
        unite.__init__(self, joueur)
        self.vitesseCourante = 7
        self.vitesseMax = 7
        self.name = soldatString
        self.initiativeCourante = 8
        self.initiativeMax = 8

