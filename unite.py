"""ceci est la déclaration de la classe de base des unites servant aux combats
normalement cette classe sert de base aux autres mais ne sert pas à déclarer un objet"""

from Data import *


class unite :
    ###========================================================================================================###
    def __init__(self, joueur):
        """Initialisation des variables de base d'une unité quelconque"""
        self.x = 1  # position par défaut sur l'échiquier
        self.y = 1  # position par défaut sur l'échiquier
        self.hautCase = pygame.Rect((TailleCases * self.x) + (TailleCases / 3), TailleCases * self.y, TailleCases / 3, TailleCases / 3)  # position du haut de la case, pour la def attaque
        self.gaucheCase = pygame.Rect(TailleCases * self.x, TailleCases * self.y + TailleCases / 3,TailleCases / 3, TailleCases / 3)  # position de la gauche de la case, pour la def attaque
        self.droiteCase = pygame.Rect(TailleCases * self.x + TailleCases * 2 / 3, TailleCases * self.y + TailleCases / 3, TailleCases / 3, TailleCases / 3)  # position de la doite de la case, pour la def attaque
        self.basCase = pygame.Rect(TailleCases * self.x + TailleCases / 3, TailleCases * self.y + TailleCases * 2 / 3, TailleCases / 3, TailleCases / 3)  # position du bas de la case, pour la def attaque
        self.name = "unité"  # le nom de base de l'unité
        self.vieCourante = 20  # La santé d'une unité durant le combat
        self.vieMax = 20  # La santé par défaut d'une unité
        self.vitesseCourante = 4  # La vitesse de base d'une unité, en relation avec le nombre de case qu'elle parcourt, pour d'éventuels malus plus tard
        self.vitesseMax = 4  # La vitesse actuelle d'une unité, en relation avec le nombre de case qu'elle parcourt
        self.puissanceCourante = 5  # La puissance de frappe de base d'une unité, pour d'éventuels malus plus tard
        self.puissanceMax = 5  # La puissance de frappe actuelle d'une unité
        self.defenseCourante = 3  # La défense actuelle d'une unité, pour d'éventuels malus plus tard
        self.defenseMax = 3  # La défense de base d'une unité
        self.initiativeCourante = 5  # L'initiative actuelle d'une unité, pour d'éventuels malus plus tard
        self.initiativeMax = 5  # L'initiative de base d'une unité
        self.appartenance = joueur  # Le joueur auquel appartient l'unité
        self.listeCasePossibleDeplacement = []  # La liste des cases où l'unité peut se déplacer
        self.listeCasePossibleDeplacementTempo = []  # Une liste temporaire dûe à la récursivité de la fonction calculCasePossible
        self.listeCasePossibleAttaque = []
        self.listeCasePossibleAttaqueHautCase = []
        self.listeCasePossibleAttaqueBasCase = []
        self.listeCasePossibleAttaqueGaucheCase = []
        self.listeCasePossibleAttaqueDroiteCase = []
        self.listeCasePossibleAttaqueTempo = []
        self.listeUnitePouvantEtreAttaque = []

    ###========================================================================================================###
    def setCoord(self, newX, newY):
        """"Définition de nouvelles coordonées pour une unité quelconque"""
        self.x = newX
        self.y = newY
        self.hautCase = pygame.Rect((TailleCases * self.x) + (TailleCases / 3), TailleCases * self.y, TailleCases / 3,
                                    TailleCases / 3)  # position du haut de la case, pour la def attaque
        self.gaucheCase = pygame.Rect(TailleCases * self.x, TailleCases * self.y + TailleCases / 3, TailleCases / 3,
                                      TailleCases / 3)  # position de la gauche de la case, pour la def attaque
        self.droiteCase = pygame.Rect(TailleCases * self.x + TailleCases * 2 / 3,
                                      TailleCases * self.y + TailleCases / 3, TailleCases / 3,
                                      TailleCases / 3)  # position de la doite de la case, pour la def attaque
        self.basCase = pygame.Rect(TailleCases * self.x + TailleCases / 3, TailleCases * self.y + TailleCases * 2 / 3,
                                   TailleCases / 3, TailleCases / 3)  # position du bas de la case, pour la def attaque

    ###========================================================================================================###
    def getCoord(self):
        """Obtention des coordonnées actuelles d'une unité quelconque"""
        return self.x, self.y


    ###========================================================================================================###
    def deplacement(self, XCaseArrivee, YCaseArrivee, listeUnite):
        """Return une autorisation de déplacement ou non selon la destination voulue par un joueur"""
        for caseDisponible in self.listeCasePossibleDeplacement:
            if (XCaseArrivee, YCaseArrivee) == caseDisponible:
                return True
        return False


    ###========================================================================================================###
    def deplacementPossibleDebutTour(self, ecranCombat, joueur1, joueur2, unite):
        """L'intégralité des cases où une unité quelconque peut se déplacer"""
        self.listeCasePossibleDeplacement = []
        self.listeCasePossibleDeplacementTempo = []
        self.listeCasePossibleAttaque = []
        self.listeCasePossibleAttaqueTempo = []
        self.listeUnitePouvantEtreAttaque = []
        self.calculCasePossible(self.vitesseCourante,self.x, self.y, ecranCombat,unite)
        self.listeCasePossibleDeplacementTempo.remove((self.x, self.y))

        """On enlève toutes les cases présentes plusieurs fois, dûe à la récursivité de la fonction"""
        while len(self.listeCasePossibleDeplacementTempo) != 0:
            for element in self.listeCasePossibleDeplacementTempo:
                if element not in self.listeCasePossibleDeplacement:
                    self.listeCasePossibleDeplacement.append(element)
                self.listeCasePossibleDeplacementTempo.remove(element)

        while len(self.listeCasePossibleAttaqueTempo) != 0:
            for element in self.listeCasePossibleAttaqueTempo:
                if element not in self.listeCasePossibleAttaque:
                    self.listeCasePossibleAttaque.append(element)
                self.listeCasePossibleAttaqueTempo.remove(element)


    ###========================================================================================================###
    def calculCasePossible (self, nbreDeCases, XCase, YCase, ecranCombat, uniteJouant):
        """Calcul des cases où l'unité peut se déplacer"""

        if nbreDeCases < 0:
            """Si l'unité est aux limites de son déplacement dû à son initiative courante"""
            return False

        """Si les cases sont en dehors du plateau"""
        if XCase < 0:
            return False

        if XCase >= 20:
            return False

        if YCase < 0:
            return False

        if YCase >= 10:
            return False

        if ecranCombat.unitePresente(XCase, YCase, uniteJouant, self.listeCasePossibleAttaqueTempo, self.listeUnitePouvantEtreAttaque):
            return False



        self.listeCasePossibleDeplacementTempo += {(XCase, YCase): ((False, 0, 0, 0, 0), (False, 0, 0, 0, 0), (False, 0, 0, 0, 0), (False, 0, 0, 0, 0))}
        """Ajout de la case actuelle """
        nbreDeCases -= 1
        """Suppression d'une case afin de ne pas avoir des déplacements infini"""

        """Récursivité pour executer les cases adjacente à celle actuelle"""
        self.calculCasePossible(nbreDeCases, XCase - 1, YCase, ecranCombat, uniteJouant)
        self.calculCasePossible(nbreDeCases, XCase + 1, YCase, ecranCombat, uniteJouant)
        self.calculCasePossible(nbreDeCases, XCase, YCase - 1, ecranCombat, uniteJouant)
        self.calculCasePossible(nbreDeCases, XCase, YCase + 1, ecranCombat, uniteJouant)


    ###========================================================================================================###
    def initCombat(self):
        """Initialisation du combat lors de la création d'une partie"""
        self.vieCourante = self.vieMax
        self.vitesseCourante = self.vitesseMax
        self.puissanceCourante = self.puissanceMax
        self.defenseCourante = self.defenseMax
        self.initiativeCourante = self.initiativeMax


    ###========================================================================================================###
    def finTourUnite(self):
        """Réinitialise au début du tour les caractéristique d'une unité quelconque excepté la santé"""
        self.vitesseCourante = self.vitesseMax
        self.puissanceCourante = self.puissanceMax
        self.defenseCourante = self.defenseMax
        self.initiativeCourante = self.initiativeMax
        self.listeCasePossibleDeplacement = []
        self.listeCasePossibleDeplacementTempo = []
        self.listeCasePossibleAttaque = []
        self.listeCasePossibleAttaqueTempo = []
        self.listeUnitePouvantEtreAttaque = []

    ###========================================================================================================###
    def actionDefense(self):
        """augmentation de la défense d'une unité quelconque"""
        self.defenseCourante += augmentationDefense


    ###========================================================================================================###
    def actionAttaque(self, uniteEnnemie):
        """enlève une quantité de point de vie à une unité ennemie selon l'attaque d'une unité quelconque et la défense de l'ennemi"""
        uniteEnnemie.vieCourante -= self.puissanceCourante


    ###========================================================================================================###
    def attaque(self, x, y):
        """déplace l'unité quelconque selon l'endroit de l'action attaque, tout en réalisant la def actionAttaque"""
        for unite in self.listeUnitePouvantEtreAttaque:

            if x in range((int(unite.hautCase[0])), int(unite.hautCase[0]+unite.hautCase[2]+1)):
                if y in range((int(unite.hautCase[1])), int(unite.hautCase[1]+unite.hautCase[3]+1)):
                    if (unite.getCoord()[0], unite.getCoord()[1] - 1) in self.listeCasePossibleDeplacement:
                        self.setCoord(unite.getCoord()[0], unite.getCoord()[1] - 1)
                        print(unite.vieCourante)
                        self.actionAttaque(unite)
                        print(unite.vieCourante)
                        return True

            if x in range((int(unite.basCase[0])), int(unite.basCase[0]+unite.basCase[2]+1)):
                if y in range((int(unite.basCase[1])), int(unite.basCase[1]+unite.basCase[3]+1)):
                    if (unite.getCoord()[0], unite.getCoord()[1] + 1) in self.listeCasePossibleDeplacement:
                        self.setCoord(unite.getCoord()[0], unite.getCoord()[1] + 1)
                        print(unite.vieCourante)
                        self.actionAttaque(unite)
                        print(unite.vieCourante)
                        return True

            if x in range((int(unite.gaucheCase[0])), int(unite.gaucheCase[0]+unite.gaucheCase[2]+1)):
                if y in range((int(unite.gaucheCase[1])), int(unite.gaucheCase[1]+unite.gaucheCase[3]+1)):
                    if (unite.getCoord()[0] - 1, unite.getCoord()[1]) in self.listeCasePossibleDeplacement:
                        self.setCoord(unite.getCoord()[0] - 1, unite.getCoord()[1])
                        print(unite.vieCourante)
                        self.actionAttaque(unite)
                        print(unite.vieCourante)
                        return True

            if x in range((int(unite.droiteCase[0])), int(unite.droiteCase[0]+unite.droiteCase[2]+1)):
                if y in range((int(unite.droiteCase[1])), int(unite.droiteCase[1]+unite.droiteCase[3]+1)):
                    if (unite.getCoord()[0] + 1, unite.getCoord()[1]) in self.listeCasePossibleDeplacement:
                        self.setCoord(unite.getCoord()[0] + 1, unite.getCoord()[1])
                        print(unite.vieCourante)
                        self.actionAttaque(unite)
                        print(unite.vieCourante)
                        return True

        return False

    ###========================================================================================================###
    def uniteMorte(self, unite):
        return unite.vieCourante <= 0

    ###========================================================================================================###
    def delReference(self, unite):
        if unite in self.listeCasePossibleDeplacement:
            self.listeCasePossibleDeplacement.remove(unite)
        if unite in self.listeCasePossibleDeplacementTempo:
            self.listeCasePossibleDeplacementTempo.remove(unite)
        if unite in self.listeCasePossibleAttaque:
            self.listeCasePossibleAttaque.remove(unite)
        if unite.hautCase in self.listeUnitePouvantEtreAttaque:
            self.listeUnitePouvantEtreAttaque.remove(unite.hautCase)
        if unite.basCase in self.listeUnitePouvantEtreAttaque:
            self.listeUnitePouvantEtreAttaque.remove(unite.basCase)
        if unite.droiteCase in self.listeUnitePouvantEtreAttaque:
            self.listeUnitePouvantEtreAttaque.remove(unite.droiteCase)
        if unite.gaucheCase in self.listeUnitePouvantEtreAttaque:
            self.listeUnitePouvantEtreAttaque.remove(unite.gaucheCase)


"""
        selection = pygame.Surface((hautCase[2], hautCase[3]), pygame.SRCALPHA)
        selection.fill((0, 255, 0, 64))  # on la remplit en vert transparent
        ecranCombat.blit(selection, (hautCase[0], hautCase[1]))

        selection = pygame.Surface((gaucheCase[2], gaucheCase[3]), pygame.SRCALPHA)
        selection.fill((0, 255, 0, 64))  # on la remplit en vert transparent
        ecranCombat.blit(selection, (gaucheCase[0], gaucheCase[1]))

        selection = pygame.Surface((droiteCase[2], droiteCase[3]), pygame.SRCALPHA)
        selection.fill((0, 255, 0, 64))  # on la remplit en vert transparent
        ecranCombat.blit(selection, (droiteCase[0], droiteCase[1]))

        selection = pygame.Surface((basCase[2], basCase[3]), pygame.SRCALPHA)
        selection.fill((0, 255, 0, 64))  # on la remplit en vert transparent
        ecranCombat.blit(selection, (basCase[0], basCase[1]))"""