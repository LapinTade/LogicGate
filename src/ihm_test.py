import pygame
from pygame.locals import *

# ajout du chemin general du projet => import de la lib
import sys; sys.path.insert(0, "..")

from pgu import gui

app = gui.Desktop()
app.connect(gui.QUIT, app.quit, None)

c = gui.Table(width=800,height=600)

def cb():
	print 'lol'
btn = gui.Button('LOL?')
btn.connect(gui.CLICK, cb)

c.add(btn,0,0)

app.run(c)