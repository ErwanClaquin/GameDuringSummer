from Joueur import *

def initPartie(couleur1,couleur2):
    joueur1 = joueur(couleur1,"papou", True)
    joueur2 = joueur(couleur2,"erwan", False)
    return joueur1, joueur2


def init1UniteJoueur(joueur):
    joueur.addUnite(orcString, 0, 0, joueur)
    joueur.addUnite(soldatString, 0, 5, joueur)
    joueur.addUnite(orcString, 0, 9, joueur)


def init2UniteJoueur(joueur):
    joueur.addUnite(soldatString,19, 0, joueur)
    joueur.addUnite(orcString, 19, 5, joueur)
    joueur.addUnite(soldatString, 19, 9, joueur)


def initieTour(joueur1, joueur2, liste):
    listeTemporaire = []
    for element in joueur1.armee + joueur2.armee:
        listeTemporaire.append(element)

    while len(listeTemporaire) != 0:
        positionMax = 0
        position = 0
        initiativeMax = listeTemporaire[0].initiativeCourante

        for element in listeTemporaire:
            if element.initiativeCourante > initiativeMax:
                initiativeMax = element.initiativeCourante
                positionMax =position
            position += 1

        liste.append(listeTemporaire[positionMax])
        listeTemporaire.remove(listeTemporaire[positionMax])

    return liste

