"""ceci est la déclaration de la classe de base des unites servant aux combats
normalement cette classe sert de base aux autres mais ne sert pas a déclarer un objet"""
from Data import *


class unite :
    ###========================================================================================================###
    def __init__(self, joueur):
        self.x=1 # position par défaut sur l'échiquier
        self.y=1 # position par défaut sur l'échiquier
        self.name = "unité"
        self.vieCourante = 20 # La santé d'une unité durant le combat
        self.vieMax = 20 # La santé par défaut d'une unité
        self.vitesseCourante = 4 # La vitesse de base d'une unité, en relation avec le nombre de case qu'elle parcourt
        self.vitesseMax = 4
        self.puissanceCourante = 5 # La puissance de frappe de base d'une unité
        self.puissanceMax = 5
        self.defenseCourante = 3
        self.defenseMax = 3
        self.initiativeCourante = 5
        self.initiativeMax = 5
        self.appartenance = joueur
        self.listeCasePossible = []
        self.listeCasePossibleTempo = []

    ###========================================================================================================###
    def setCoord(self, newX, newY):
        self.x = newX
        self.y = newY

    ###========================================================================================================###
    def getCoord(self):
        return(self.x, self.y)

    ###========================================================================================================###
    def deplacement(self,NbreDeCases, XCaseDepart, XCaseArrivee, YCaseDepart, YCaseArrivee, joueur1, joueur2):

        if (abs(XCaseArrivee - XCaseDepart) + abs(YCaseArrivee - YCaseDepart)) <= NbreDeCases:
            presence = False
            for unite in joueur1.armee + joueur2.armee:
                if (XCaseArrivee, YCaseArrivee) == unite.getCoord():
                        presence = True
            if not presence:
                return True
        return False

    ###========================================================================================================###
    def deplacementPossibleDebutTour(self, ecranCombat, joueur1, joueur2):

        self.listeCasePossible = []
        self.listeCasePossibleTempo = []
        self.calculCasePossible(self.vitesseCourante,self.x, self.y, ecranCombat)
        self.listeCasePossibleTempo.remove((self.x, self.y))

        """On enlève toutes les cases présentes plusieurs fois"""
        while len(self.listeCasePossibleTempo) != 0:
            for element in self.listeCasePossibleTempo:
                if element not in self.listeCasePossible:
                    self.listeCasePossible.append(element)
                self.listeCasePossibleTempo.remove(element)

        """On enlève les cases amies"""

        for case in self.listeCasePossible:
            for unite in joueur1.armee + joueur2.armee:
                if case == unite.getCoord():
                    if unite.appartenance == self.appartenance:
                        self.listeCasePossible.remove(case)



    ###========================================================================================================###
    def calculCasePossible (self, nbreDeCases, XCase, YCase, ecranCombat):
        if nbreDeCases < 0:
            return False
        if XCase < 0:
            return False

        if XCase >= 20:
            return False

        if YCase < 0:
            return False

        if YCase >= 10:
            return False

        if ecranCombat.uniteEnnemiePresente(XCase, YCase, self.appartenance):
            return False

        self.listeCasePossibleTempo += {(XCase, YCase): ((False, 0, 0, 0, 0), (False, 0, 0, 0, 0), (False, 0, 0, 0, 0), (False, 0, 0, 0, 0))}

        nbreDeCases -= 1


        self.calculCasePossible(nbreDeCases, XCase - 1, YCase, ecranCombat)
        self.calculCasePossible(nbreDeCases, XCase + 1, YCase, ecranCombat)
        self.calculCasePossible(nbreDeCases, XCase, YCase - 1, ecranCombat)
        self.calculCasePossible(nbreDeCases, XCase, YCase + 1, ecranCombat)


    ###========================================================================================================###
    def initCombat(self):
        self.vieCourante = self.vieMax
        self.vitesseCourante = self.vitesseMax
        self.puissanceCourante = self.puissanceMax
        self.defenseCourante = self.defenseMax
        self.initiativeCourante = self.initiativeMax

    ###========================================================================================================###
    def actionDefense(self):
        self.defenseCourante += augmentationDefense

    ###========================================================================================================###
    def debutTourUnite(self):
        self.vitesseCourante = self.vitesseMax
        self.puissanceCourante = self.puissanceMax
        self.defenseCourante = self.defenseMax
        self.initiativeCourante = self.initiativeMax

    ###========================================================================================================###

