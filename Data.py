import pygame
from pygame.locals import *
import sys


orcString= "orc"
soldatString = "soldat"
videString = "vide"
defenseString = " augmente sa défense !"
attendString = " attend"
deplaceString = " se déplace"
impossibleDeplaceString = " ne peux pas se déplacer ici !"

augmentationDefense = 3

plateau = {(x, y): ['rien', videString] for x in range(20) for y in range(10)}


TailleCases = 40
TempsRafraichissementEcranCombat = 0
TempsRafraichissementActionSouris = 0
TempsAEnlever = 0.006
TempsAffichageTexte = 3
LEFT_BUTTON = 1
RIGHT_BUTTON = 3
