import pygame
from pygame.locals import *

# ajout du chemin general du projet => import de la lib
import sys; sys.path.insert(0, "..")

from pgu import gui

app = gui.App()

e = gui.Button("Kikoo")

app.connect(gui.QUIT, app.quit)

app.run(e) 