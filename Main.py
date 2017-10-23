from Data import *
from unite import *
from Soldat import *
from Orc import *
from InitialisationPartie import *
from EcranCombat import *
import time

pygame.init()
joueur1,joueur2 = initPartie("bleue","rouge")

init1UniteJoueur(joueur1)
init2UniteJoueur(joueur2)
listeTourUnite = []
initieTour(joueur1, joueur2, listeTourUnite)
pygame.mouse.set_visible(True)

#todo on rentre en combat
ecranDeCombat = EcranCombat(joueur1, joueur2,listeTourUnite)
ecranDeCombat.start()
combatEnCours = True

while combatEnCours:
    for event in pygame.event.get():
        """On fait la liste de tous les évenements qui peuvent se produirent"""
        if event.type == QUIT:
            """Si l'utilisateur clic sur al croix en haut à droite, le programme se ferme"""
            combatEnCours = False

        if event.type == MOUSEBUTTONUP and event.button == LEFT_BUTTON:
            ecranDeCombat.clicGauche()

        elif event.type == MOUSEBUTTONUP and event.button == RIGHT_BUTTON:
            ecranDeCombat.clicDroit()
    time.sleep(TempsRafraichissementActionSouris)

    if len(joueur1.armee) == 0:
        print(joueur2.name, "gagne")
        combatEnCours = False
    elif len(joueur2.armee) == 0:
        print(joueur1.name, "gagne")
        combatEnCours = False

ecranDeCombat.finDeCombat()
ecranDeCombat.join(5)
pygame.quit()
sys.exit()