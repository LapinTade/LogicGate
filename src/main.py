#-*- coding: utf-8 -*- 
import Gate
import pygame
from pygame.locals import *
import var

porte = Gate.ANDGate(True, True)
lol = Gate.ANDGate(True, True)
print porte & lol
print porte

pygame.init()

fenetre = pygame.display.set_mode((800,600))
fenetre.fill((255,255,255))

# Boucle pour affichage constant de la fenetre
continuer = 1

# Charge l'image de la porte en mémoire
imgGate = pygame.image.load(porte.imgGate).convert_alpha()
# Resizing en 100x50
imgGate = pygame.transform.smoothscale(imgGate, (100,50))
fenetre.blit(imgGate, (0,0))
# Rafraîchissement de l'écran
pygame.display.flip()

while continuer:
	continuer = (int(input()))