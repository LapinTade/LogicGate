LogicGate
=========

Projet Tut' 2013 L3 Info

Pygame:
> easy_install pygame

Path:
> easy_install path.py


apt-get install qt4-designer qt4-doc python-qt4 python-qt4-doc pyqt4-dev-tools

Exemple de résultat retourner pour ma fonction composition pour l'expression : 
((a or not r) and (a or b)) and (a or not r) or not(x and y)

Résultat :
porte = 
[['a', 'or', 'not r'], ['porte[0]', 'and', 'porte[2]'], 
['a', 'or', 'b'], ['porte[2]', 'and', 'porte[4]'], 
['a', 'or', 'not r'], ['porte[4]', 'or', 'porte[6]'], 
['x', 'and', 'y']]

Des remarques ?
