from threading import Thread, RLock
from pygame import *
from Data import *
import time
from InitialisationPartie import *
from pygame.locals import *


verrouAffichageCombat =RLock()


class EcranCombat(Thread):
    ###========================================================================================================###
    def __init__(self,joueur1,joueur2,listeTourUnite):

        Thread.__init__(self)
        # init des données de la classe
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.listeTourUnite = listeTourUnite
        self.combatEnCours = True
        self.texteAAfficher = []
        self.listeTourUnite[0].deplacementPossibleDebutTour(self, self.joueur1, self.joueur2)

        # init de l'écran graphique
        self.ecranCombat = pygame.display.set_mode((1500, 845))
        self.ArrierePlan = pygame.image.load("Fond.jpg").convert_alpha()
        self.ImageSoldat = pygame.image.load("soldat.png").convert_alpha()
        self.ImageSoldatMiroir = pygame.image.load("soldatMiroir.png").convert_alpha()
        self.ImageOrc = pygame.image.load("Orc.png").convert_alpha()
        self.ImageOrcMiroir = pygame.image.load("OrcMiroir.png").convert_alpha()
        self.ImageBouclier = pygame.image.load("bouclier.png").convert_alpha()
        self.ImageSabier = pygame.image.load("sablier.png").convert_alpha()

    ###========================================================================================================###
    def run(self):
        while self.combatEnCours:
            self.ecranCombat.blit(self.ArrierePlan, (0, 0))
            self.ecranCombat.blit(self.ImageBouclier, (1400, 320))
            self.ecranCombat.blit(self.ImageSabier, (1412, 402))
            self.afficheCaseSouris()
            self.affichageOrdreTour()
            self.affichageDeplacementPossibleUnite()
            self.affichageQuiJoue()


            with verrouAffichageCombat:
                self.afficheTexte()
                self.affichageUnite()

            pygame.display.flip()
            time.sleep(TempsRafraichissementEcranCombat)

    ###========================================================================================================###
    def finDeCombat(self):
        self.combatEnCours = False

    ###========================================================================================================###
    def affichageUnite(self):
        for element in self.joueur1.armee + self.joueur2.armee:
            if element.name == soldatString:
                if element.appartenance.sensImage():
                    self.ecranCombat.blit(self.ImageSoldat, (element.x * TailleCases, element.y * TailleCases))
                else:
                    self.ecranCombat.blit(self.ImageSoldatMiroir, (element.x * TailleCases, element.y * TailleCases))
            elif element.name == orcString:
                if element.appartenance.sensImage():
                    self.ecranCombat.blit(self.ImageOrc, (element.x * TailleCases, element.y * TailleCases))
                else:
                    self.ecranCombat.blit(self.ImageOrcMiroir, (element.x * TailleCases, element.y * TailleCases))

    ###========================================================================================================###
    def afficheTexte(self):
        if len(self.texteAAfficher) != 0:
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.texteAAfficher[0]), 1, (10, 10, 10))
            textpos = text.get_rect()
            textpos.centerx = self.ecranCombat.get_rect().centerx
            textpos.centery = 800
            self.ecranCombat.blit(text, textpos)
            self.texteAAfficher[1] -= TempsRafraichissementEcranCombat
            if self.texteAAfficher[1] <= 0:
                self.texteAAfficher = []

    ###========================================================================================================###
    def affichageOrdreTour(self):
        for position in range(len(self.listeTourUnite)):
            if self.listeTourUnite[position].name == soldatString and self.listeTourUnite[position].appartenance == self.joueur1:
                self.ecranCombat.blit(self.ImageSoldat, (TailleCases + position * 2 * TailleCases, 700))
            elif self.listeTourUnite[position].name == orcString and self.listeTourUnite[position].appartenance == self.joueur1:
                self.ecranCombat.blit(self.ImageOrc, (TailleCases + position * 2 * TailleCases, 700))
            elif self.listeTourUnite[position].name == soldatString and self.listeTourUnite[position].appartenance == self.joueur2:
                self.ecranCombat.blit(self.ImageSoldatMiroir, (TailleCases + position * 2 * TailleCases, 700))
            elif self.listeTourUnite[position].name == orcString and self.listeTourUnite[position].appartenance == self.joueur2:
                self.ecranCombat.blit(self.ImageOrcMiroir, (TailleCases + position * 2 * TailleCases, 700))

    ###========================================================================================================###
    def affichageQuiJoue(self):
        x, y = self.listeTourUnite[0].x, self.listeTourUnite[0].y
        selectionCase = pygame.Surface((TailleCases, TailleCases), pygame.SRCALPHA)
        selectionCase.fill((0, 0, 255, 64))
        self.ecranCombat.blit(selectionCase, (x * TailleCases, y * TailleCases))

    ###========================================================================================================###
    def afficheCaseSouris(self):
        pixelX = pygame.mouse.get_pos()[0]
        pixelY = pygame.mouse.get_pos()[1]
        x, y = self.convertitPixelEnCase(pixelX, pixelY)
        if self.DansZone(x, y):
            selection = pygame.Surface((TailleCases, TailleCases), pygame.SRCALPHA)
            selection.fill((0, 255, 0, 64))  # on la remplit en vert transparent
            self.ecranCombat.blit(selection, (x * TailleCases, y * TailleCases))

    ###========================================================================================================###
    def affichageDeplacementPossibleUnite(self):
        # AFAC : todo marche pas actuellement

        """selection = pygame.Surface((TailleCases, TailleCases), pygame.SRCALPHA)
        x = listeUnite[0].getCoord()[0]
        y = listeUnite[0].getCoord()[1]
        case = listeUnite[0].vitesseCourante
        for i in range(case + 1):
            selection.fill((255, 0, 0, 64))"""
        selection = pygame.Surface((TailleCases, TailleCases), pygame.SRCALPHA)
        selection.fill((255, 0, 0, 64))
        for case in self.listeTourUnite[0].listeCasePossible:
            self.ecranCombat.blit(selection, (case[0] * TailleCases, case[1] * TailleCases))

    ###========================================================================================================###
    def DansZone(self, x, y):
        return x >= 0 and x < 20 and y >= 0 and y < 10

    ###========================================================================================================###
    def surBouclier(self, x, y):
        return x >= 1400 and x <= 1480 and y >= 320 and y <= 400

    ###========================================================================================================###
    def surSablier(self, x, y):
        return x >= 1412 and x <= 1467 and y >= 402 and y <= 482

    ###========================================================================================================###
    def convertitPixelEnCase(self, pixelX, pixelY):
        """On créer des tailles de carré à remplir (TailleCases) avant de choisir la couleur de cette sélection si il y'a un clic ou non"""
        x = pixelX // TailleCases
        y = pixelY // TailleCases
        return x, y

    ###========================================================================================================###
    def clicGauche(self):
        self.texteAAfficher = []
        PixelX =pygame.mouse.get_pos()[0]
        PixelY =pygame.mouse.get_pos()[1]
        x, y = self.convertitPixelEnCase(PixelX, PixelY)

        if self.DansZone(x, y):
            oldCoord = self.listeTourUnite[0].getCoord()
            newCoord = (x, y)

            if self.listeTourUnite[0].deplacement(self.listeTourUnite[0].vitesseCourante, oldCoord[0], newCoord[0], oldCoord[1],newCoord[1], self.joueur1, self.joueur2):
                self.listeTourUnite[0].setCoord(x, y)
                plateau[oldCoord] = ['rien', videString]
                self.texteAAfficher.append(self.listeTourUnite[0].name + deplaceString)
                self.texteAAfficher.append(TempsAffichageTexte)
                self.listeTourUnite.remove(self.listeTourUnite[0])

                if (len(self.listeTourUnite)!=0):
                    self.listeTourUnite[0].deplacementPossibleDebutTour(self, self.joueur1, self.joueur2)

            else:
                self.texteAAfficher.append(self.listeTourUnite[0].name + impossibleDeplaceString)
                self.texteAAfficher.append(TempsAffichageTexte)

        elif self.surBouclier(PixelX, PixelY):
            self.clicSurDefense()

        elif self.surSablier(PixelX, PixelY):
            self.clicsurSablier()
        if len(self.listeTourUnite) == 0:
            initieTour(self.joueur1, self.joueur2, self.listeTourUnite)
            self.listeTourUnite[0].deplacementPossibleDebutTour(self, self.joueur1, self.joueur2)

    ###========================================================================================================###
    def clicDroit(self):
        PixelX = pygame.mouse.get_pos()[0]
        PixelY = pygame.mouse.get_pos()[1]
        x, y = self.convertitPixelEnCase(PixelX, PixelY)
        if plateau[x, y][1] == videString:
            print("y'a rien")
        else:
            for element in self.joueur1.armee + self.joueur2.armee:
                if element.x == x and element.y == y:
                    print(element.appartenance.name)

    ###========================================================================================================###
    def clicSurDefense(self):
        self.texteAAfficher.append(self.listeTourUnite[0].name + defenseString)
        self.texteAAfficher.append(TempsAffichageTexte)
        self.listeTourUnite[0].actionDefense()
        self.listeTourUnite.remove(self.listeTourUnite[0])

    ###========================================================================================================###
    def clicsurSablier(self):
        self.texteAAfficher.append(self.listeTourUnite[0].name + attendString)
        self.texteAAfficher.append(TempsAffichageTexte)
        saveUnite = self.listeTourUnite[0]
        self.listeTourUnite.remove(self.listeTourUnite[0])
        self.listeTourUnite.append(saveUnite)

    ###========================================================================================================###
    def uniteEnnemiePresente(self,XCase,YCase, joueur):
        return False