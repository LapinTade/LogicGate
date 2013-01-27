import var
import pygame
from pygame.locals import *
"""
@author: MARIN Jordy, ROZE Nicolas
"""
class Gate(object):
	""" Classe Gate qui represante une porte logique

	Deux entree A et B, et une sortie S
	"""
	def __init__(self, entranceA, entranceB):
		"""	Constructeur, prend en param 2 bool"""
		self.entranceA = entranceA
		self.entranceB = entranceB

	def __str__(self):
		return "Entre A: %s, entranceB: %s" % (self.entranceA, self.entranceB)

class ANDGate(Gate):
	""" Classe de la porte AND"""
	def __init__(self, entranceA, entranceB):
		Gate.__init__(self, entranceA, entranceB)
		self.sortieS = entranceA & entranceB

		self.imgGate = var.img_ANDGate

	def __str__(self):
		self.sortieS = self.entranceA & self.entranceB
		return "Entre A: %s, entranceB: %s \nSortieS: %s" % (self.entranceA, self.entranceB, self.sortieS)

	def __and__(self, other):
		return (self.entranceA & self.entranceB) & (other.entranceA & other.entranceB)