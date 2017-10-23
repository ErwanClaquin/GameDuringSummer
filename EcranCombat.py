from threading import Thread, RLock
from pygame import *
from Data import *
import time
from InitialisationPartie import *
from pygame.locals import *
verrouAffichageCombat = RLock()


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
        self.listeTourUnite[0].deplacementPossibleDebutTour(self, self.joueur1, self.joueur2, self.listeTourUnite[0])

        # init de l'écran graphique
        self.ecranCombat = pygame.display.set_mode((1500, 845))
        self.tailleEcran = self.ecranCombat.get_rect
        self.ArrierePlan = pygame.image.load("Fond.jpg").convert_alpha()
        self.ImageSoldat = pygame.image.load("soldat.png").convert_alpha()
        self.ImageSoldatMiroir = self.img = pygame.transform.flip(self.ImageSoldat, True, False)
        self.ImageOrc = pygame.image.load("Orc.png").convert_alpha()
        self.ImageOrc = pygame.transform.scale(self.ImageOrc, (40, 60))
        self.ImageOrcMiroir = self.img = pygame.transform.flip(self.ImageOrc, True, False)
        self.ImageBouclier = pygame.image.load("bouclier.png").convert_alpha()
        self.ImageSabier = pygame.image.load("sablier.png").convert_alpha()
        self.ImagesourisGlove = pygame.image.load("gloveTailleJeu.png").convert_alpha()
        self.ImagesourisBoots = pygame.image.load("bootTailleJeu.png").convert_alpha()
        self.ImageEpeeVersBas = pygame.image.load("EpeeVersBas.jpg").convert_alpha()
        self.ImageEpeeVersBas = pygame.transform.scale(self.ImageEpeeVersBas, (40, 100)) #pygame.transform.scale(image preload,(taille des x, taille des y))

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
            self.afficheTypeSouris()


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
            self.texteAAfficher[1] -= TempsAEnlever
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
    def afficheTypeSouris(self):
        pixelX = pygame.mouse.get_pos()[0]
        pixelY = pygame.mouse.get_pos()[1]
        x, y = self.convertitPixelEnCase(pixelX, pixelY)
        if (x, y) in self.listeTourUnite[0].listeCasePossibleDeplacement:
            self.ecranCombat.blit(self.ImagesourisBoots, (pixelX - 4, pixelY - 11))

        elif (x, y) not in self.listeTourUnite[0].listeCasePossibleDeplacement:
                for unite in self.listeTourUnite[0].listeUnitePouvantEtreAttaque:
                    if pixelX in range(int(unite.hautCase[0]), int(unite.hautCase[0] + unite.hautCase[2]) + 1):
                        if pixelY in range(int(unite.hautCase[1]), int(unite.hautCase[1] + unite.hautCase[3]) + 1):
                            self.ecranCombat.blit(self.ImageEpeeVersBas, (pixelX - 4, pixelY - 11))

                """
                elif (pixelX, pixelY) in self.listeTourUnite[0].listeCasePossibleAttaque:
                    self.ecranCombat.blit(self.ImageEpeeVersBas, (pixelX - 4, pixelY - 11))
                    for indent in range(0, len(self.listeTourUnite[0].listeCasePossibleAttaque)):
                        print("2")
                        for unite in self.listeTourUnite[0].listeUnitePouvantEtreAttaque[indent].hautCase:
                            print("3")
                            if pixelX in range((int(unite.hautCase[0])), int(unite.hautCase[0] + unite.hautCase[2]) + 1):
                                print("4")
                                if pixelY in range((int(unite.hautCase[1])), int(unite.hautCase[1] + unite.hautCase[3]) + 1):
                                    print("5")
                                    self.ecranCombat.blit(self.ImageEpeeVersBas, (pixelX - 4, pixelY - 11))"""

        elif self.DansEcran(pixelX, pixelY):
            self.ecranCombat.blit(self.ImagesourisGlove, (pixelX - 4, pixelY - 11))


    ###========================================================================================================###
    def afficheCaseSouris(self):
        pixelX = pygame.mouse.get_pos()[0]
        pixelY = pygame.mouse.get_pos()[1]
        x, y = self.convertitPixelEnCase(pixelX, pixelY)
        if self.DansZoneDeCombat(x, y):
            selection = pygame.Surface((TailleCases, TailleCases), pygame.SRCALPHA)
            selection.fill((0, 255, 0, 64))  # on la remplit en vert transparent
            self.ecranCombat.blit(selection, (x * TailleCases, y * TailleCases))

    ###========================================================================================================###
    def affichageDeplacementPossibleUnite(self):
        selection = pygame.Surface((TailleCases, TailleCases), pygame.SRCALPHA)
        selection.fill((255, 0, 0, 64))
        for case in self.listeTourUnite[0].listeCasePossibleDeplacement:
            self.ecranCombat.blit(selection, (case[0] * TailleCases, case[1] * TailleCases))

        for unite in self.listeTourUnite[0].listeUnitePouvantEtreAttaque:
            selection = pygame.Surface((unite.hautCase[2], unite.hautCase[3]), pygame.SRCALPHA)
            selection.fill((0, 255, 0, 64))  # on la remplit en vert transparent
            self.ecranCombat.blit(selection, (unite.hautCase[0], unite.hautCase[1]))

            selection = pygame.Surface((unite.gaucheCase[2], unite.gaucheCase[3]), pygame.SRCALPHA)
            selection.fill((0, 255, 0, 64))  # on la remplit en vert transparent
            self.ecranCombat.blit(selection, (unite.gaucheCase[0], unite.gaucheCase[1]))

            selection = pygame.Surface((unite.droiteCase[2], unite.droiteCase[3]), pygame.SRCALPHA)
            selection.fill((0, 255, 0, 64))  # on la remplit en vert transparent
            self.ecranCombat.blit(selection, (unite.droiteCase[0], unite.droiteCase[1]))

            selection = pygame.Surface((unite.basCase[2], unite.basCase[3]), pygame.SRCALPHA)
            selection.fill((0, 255, 0, 64))  # on la remplit en vert transparent
            self.ecranCombat.blit(selection, (unite.basCase[0], unite.basCase[1]))


    ###========================================================================================================###
    def DansZoneDeCombat(self, x, y):
        return x >= 0 and x < 20 and y >= 0 and y < 10

    ###========================================================================================================###
    def DansEcran(self,x,y):
        return x >= 0 and x < 1500 and y >= 0 and y < 845

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

        if self.DansZoneDeCombat(x, y):
            oldCoord = self.listeTourUnite[0].getCoord()
            newCoord = (x, y)

            if self.listeTourUnite[0].deplacement(newCoord[0], newCoord[1], self.joueur1.armee + self.joueur2.armee):
                self.listeTourUnite[0].setCoord(x, y)
                plateau[oldCoord] = ['rien', videString]
                self.texteAAfficher.append(self.listeTourUnite[0].name + deplaceString)
                self.texteAAfficher.append(TempsAffichageTexte)
                self.listeTourUnite[0].finTourUnite()
                self.listeTourUnite.remove(self.listeTourUnite[0])

            elif self.listeTourUnite[0].attaque(PixelX, PixelY):
                plateau[oldCoord] = ['rien', videString]
                self.uniteMorte()
                self.texteAAfficher.append(self.listeTourUnite[0].name + deplaceString)
                self.texteAAfficher.append(TempsAffichageTexte)
                self.listeTourUnite[0].finTourUnite()
                self.listeTourUnite.remove(self.listeTourUnite[0])

            else:
                self.texteAAfficher.append(self.listeTourUnite[0].name + impossibleDeplaceString)
                self.texteAAfficher.append(TempsAffichageTexte)

        elif self.surBouclier(PixelX, PixelY):
            self.clicSurDefense()
            self.listeTourUnite[0].finTourUnite()

        elif self.surSablier(PixelX, PixelY):
            self.clicsurSablier()
            self.listeTourUnite[0].finTourUnite()

        if len(self.listeTourUnite) == 0:
            initieTour(self.joueur1, self.joueur2, self.listeTourUnite)
        self.listeTourUnite[0].deplacementPossibleDebutTour(self, self.joueur1, self.joueur2, self.listeTourUnite[0])

    ###========================================================================================================###
    def clicDroit(self):
        PixelX = pygame.mouse.get_pos()[0]
        PixelY = pygame.mouse.get_pos()[1]
        print(self.DansEcran(PixelX,PixelY))

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
    def unitePresente(self, XCase, YCase, uniteJouant, listeAttaque, listeUnitePouvantEtreAttaque):
        for unite in self.joueur1.armee + self.joueur2.armee:
            if unite.getCoord() == (XCase, YCase):
                if uniteJouant == unite:
                    return False
                elif uniteJouant.appartenance == unite.appartenance:
                    return True
                elif uniteJouant.appartenance != unite.appartenance:
                    listeUnitePouvantEtreAttaque.append(unite)
                    listeAttaque.append(unite.hautCase)
                    listeAttaque.append(unite.basCase)
                    listeAttaque.append(unite.gaucheCase)
                    listeAttaque.append(unite.droiteCase)
                    return True
                return True
        return False

    ###========================================================================================================###
    def uniteMorte(self):
        for unite in self.joueur1.armee+ self.joueur2.armee:
            if unite.vieCourante <= 0:
                self.suppressionUnite(unite)
                return True
        return False


    ###========================================================================================================###
    def suppressionUnite(self, uniteASuppr):
        """Todo : Trouver toutes les références de l'unite"""
        if uniteASuppr in self.joueur1.armee:
            self.joueur1.armee.remove(uniteASuppr)
        else:
            self.joueur2.armee.remove(uniteASuppr)
        if uniteASuppr in self.listeTourUnite:
            self.listeTourUnite.remove(uniteASuppr)
        for creature in self.joueur2.armee+self.joueur1.armee:
            creature.delReference(uniteASuppr)
