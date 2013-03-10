#-*- coding: utf-8 -*- 
from PyQt4 import QtCore, QtGui, QtOpenGL
import fonction
import math

import sys, random

#@TODO Faire des fichiers séparé par classe :p
#   Ajouter class entree (avec valeur bool)
#   Ajouter le 'linkage' des portes avec les entree ou entres elles
#   Ajouter le résultat de chaque porte
#   Ajouter les not entrée et sortie
#   ...

def debug_trace():
  '''Set a tracepoint in the Python debugger that works with Qt'''
  from PyQt4.QtCore import pyqtRemoveInputHook
  from pdb import set_trace
  pyqtRemoveInputHook()
  set_trace()


class Entry(QtGui.QGraphicsItem):
    def __init__(self, name, x, y, value,parent=None):
        super(Entry, self).__init__(parent)
        self.name = name
        self.x = x
        self.y = y
        self.value = value

        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)

    def __str__(self):
        return str(self.name)

    """def setPos(self, x, y):
                    self.x = x
                    self.y = y
                    super(Entry, self).setPos(x,y)"""

    def boundingRect(self):
        return QtCore.QRectF(0,0,10,10)

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def setValue(self, value):
        self.value = value

    def paint(self, painter, option, parent=None):
        painter.setPen(QtGui.QColor("black"))
        painter.drawText(self.x,self.y,self.name)

        if(self.isSelected()):
            print 'X:%s, Y:%s === name: %s' % (self.pos().x(), self.pos().y(),self.name)

class Gate(QtGui.QGraphicsItem):
    def __init__(self, x, y, size=20, scale=1, parent=None):
        super(Gate, self).__init__(parent)
        self.size = size
        self.scale = scale

        self.setPos(x,y)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)

        self.entreeA = None
        self.entreeB = None

    #def __str__(self):
        #return "entreeA: " + self.entreeA + ", entreeB: " + self.entreeB


    def boundingRect(self):
        return QtCore.QRectF(0,0,self.size*2,self.size+(self.size/2))

    def paint(self, painter, option, parent=None):
        painter.setPen(QtGui.QColor("black"))
# painter.drawEllipse(QtCore.QRectF(self.size+(self.size/2),(self.size/4),(self.size/2),(self.size/2)))
        if(self.isSelected()):
            print "\nid(self): %s" % (id(self))
            print "X:%s, Y:%s === entreeA: %s, entreeB: %s" % (self.pos().x(), self.pos().y(), type(self.entreeA), type(self.entreeB))
            print "Add entreeA: %s, Add entreeB: %s" % (id(self.entreeA), id(self.entreeB))

    def setEntries(self, entreeA, entreeB):
        self.entreeA, self.entreeB = entreeA, entreeB

    def getEntries(self):
        return (self.entreeA,self.entreeB)


class AndGate(Gate):
    def __init__(self,*args,**kwargs):
        super(AndGate, self).__init__(*args,**kwargs)

    def __str__(self):
        return "AndGate: " + super(AndGate, self).__str__()
    
    def paint(self, painter, option, parent=None):
        super(AndGate, self).paint(painter,option)
        painter.drawLine(0,self.size,self.size,self.size)
        painter.drawLine(0,0,self.size,0)
        painter.drawLine(0,0,0,self.size)
        
        painter.drawText(self.size/2,(self.size/2)+(self.size/8),"&")
        painter.drawArc(QtCore.QRectF(self.size/2,0,self.size,self.size),90*16,-180*16)


class OrGate(Gate):
    def __init__(self,*args,**kwargs):
        super(OrGate, self).__init__(*args,**kwargs)

    def __str__(self):
        return "OrGate: " + super(OrGate, self).__str__()
 
    def paint(self, painter, option, parent=None):
        super(OrGate, self).paint(painter,option)
        painter.drawLine(0,self.size,self.size,self.size)
        painter.drawLine(0,0,self.size,0)

        painter.drawArc(QtCore.QRectF(-self.size/2,0,self.size,self.size),90*16,-180*16)
        painter.drawArc(QtCore.QRectF(0,0,self.size*2,self.size*2),90*16,-60*16)
        painter.drawArc(QtCore.QRectF(0,-self.size,self.size*2,self.size*2),-90*16,60*16)


class XOrGate(Gate):
    def __init__(self,*args,**kwargs):
        super(XOrGate, self).__init__(*args,**kwargs)

    def __str__(self):
        return "XOrGate: " + super(XOrGate, self).__str__()
 
    def paint(self, painter, option, parent=None):
        super(XOrGate, self).paint(painter,option)
        painter.drawLine(0,self.size,self.size,self.size)
        painter.drawLine(0,0,self.size,0)

        painter.drawArc(QtCore.QRectF(-self.size/2-1,0,self.size,self.size),90*16,-180*16)
        painter.drawArc(QtCore.QRectF(-self.size/2+2,0,self.size,self.size),90*16,-180*16)
        painter.drawArc(QtCore.QRectF(0,0,self.size*2,self.size*2),90*16,-60*16)
        painter.drawArc(QtCore.QRectF(0,-self.size,self.size*2,self.size*2),-90*16,60*16)


class NotGate(Gate):
    def __init__(self,*args,**kwargs):
        super(NotGate, self).__init__(*args,**kwargs)

    def __str__(self):
        return "NotGate: ", super(NotGate, self).__str__()
 
    def paint(self, painter, option, parent=None):
        super(NotGate, self).paint(painter,option)
        painter.drawText(0,(self.size/2)+(self.size/5),"1")
        painter.drawLine(0,0,0,self.size)
        painter.drawLine(0,0,self.size,self.size/2)
        painter.drawLine(0,self.size,self.size,self.size/2)


class Connexion(QtGui.QGraphicsLineItem):
    def __init__(self,x1,y1,x2,y2):
         print "HELOO"



class Circuit(object):
    def __init__(self, inputGates, inputEntries):
        self.circuit = inputGates
        self.lstGates = {}
        self.lstEntries = inputEntries

        """self.gates = { "or" : OrGate(0,0),
                        "and" : AndGate(0,0),
                        "xor" : XOrGate(0,0),
                        "not" : NotGate(0,0)}.get(valeur,None)()"""
        x = 0
        for porte in self.circuit:
            #print porte
            porteOne = porte[1]
            if porteOne == "or":
                gate = OrGate(0,0)
                #gate.setEntries(porte[0],porte[2]) 
            elif porteOne == "and":
                gate = AndGate(0,0)
                #gate.setEntries(porte[0],porte[2])
            self.lstGates[x] = gate
            x += 1
            #elif porteOne == "etc..."


        for x in range(0,len(self.circuit)):
            #print "TYPE1:",type(self.entryCreator(porte[0]))
            #print "TYPE1:",type(self.entryCreator(porte[2]))
            self.lstGates[x].setEntries(self.entryCreator(self.circuit[x][0]),self.entryCreator(self.circuit[x][2]))

    def posGates(self):
        notPosedGate = []
                        
        for k in range(0,len(self.lstGates)):
            notPosedGate.append(True)

        x = 50
        shift = 60

        for k in range(0,len(self.lstGates)): 
            for gate in self.lstGates:
                if notPosedGate[gate]:
                    #debug_trace()
                    #print "\n>k:",k," => ",id(self.lstGates[gate])
                    entreeA, entreeB = self.lstGates[gate].getEntries()
                    #print id(entreeA),id(entreeB),"<"
                    if isinstance(entreeA, Entry) and isinstance(entreeB, Entry):
                        self.lstGates[gate].setX(x)
                        notPosedGate[gate] = False

                    #Cas A est une porte et B non
                    if isinstance(entreeA, Gate) and isinstance(entreeB, Entry):
                        self.lstGates[gate].setX(entreeA.pos().x()+shift)
                        notPosedGate[gate] = False

                    #Cas B est une porte et A non
                    if isinstance(entreeB, Gate) and isinstance(entreeA, Entry):
                        self.lstGates[gate].setX(entreeB.pos().x()+shift)
                        notPosedGate[gate] = False

                    #Cas ou A et B sont des portes
                    if isinstance(entreeA, Gate) and isinstance(entreeB, Gate):
                        #print "ICI"
                        for w in range(0,len(self.lstGates)):
                            #debug_trace()
                            b = self.lstGates[w]
                            if b is entreeA:
                                posedA = notPosedGate[w]
                            if b is entreeB:
                                posedB = notPosedGate[w]
                        #print posedA,posedB
                        if (not posedA and not posedB):
                            #print "ON PEUT POSER LA double GATE"
                            notPosedGate[gate] = False
                            #print "\nA",self.lstGates[gate].pos()
                            if entreeA.pos().x() > entreeB.pos().x():
                                self.lstGates[gate].setX(entreeA.pos().x()+shift)
                            else:
                                self.lstGates[gate].setX(entreeB.pos().x()+shift)
                            print "B",self.lstGates[gate].pos()
                            notPosedGate[gate] = False

                    #Cas d'erreur
                    if entreeA is None or entreeB is None:
                        self.lstGates[gate].setPos(0,0)
                        notPosedGate[gate] = False
                        break

                    #print "C",self.lstGates[gate].pos()
                    self.lstGates[gate].setY(math.fabs(entreeA.pos().y() + entreeB.pos().y())/2)
                    #print "D",self.lstGates[gate].pos(),"\n"


    def drawConnection(self,scene):
        for gate in self.lstGates:
            gateX = int(self.lstGates[gate].pos().x())
            gateY = int(self.lstGates[gate].pos().y())

            entryA, entryB = self.lstGates[gate].getEntries()
            entryAX = int(entryA.pos().x())
            entryAY = int(entryA.pos().y())
            entryBX = int(entryB.pos().x())
            entryBY = int(entryB.pos().y())

            scene.addItem(QtGui.QGraphicsLineItem(gateX,gateY,entryAX,entryAY))
            scene.addItem(QtGui.QGraphicsLineItem(gateX,gateY,entryBX,entryBY))

            #print "\nEntryA: %s EntryB: %s" % (entryA.pos(),entryB.pos())
            #print "A( %s, %s); B( %s, %s)" % (entryAX,entryAY, entryBX,entryBY)
        
    def showGates(self):
        for porte in self.circuit:
            print porte[1]

    def showEntries(self):
        print self.lstEntries

    def getGates(self):
        return self.lstGates

    def showGates(self):
        print self.lstGates

    def entryCreator(self, entry):
        if "not" in entry:
            return
        try:
            entry = int(entry)
            return self.lstGates[entry]
        except:
            return self.lstEntries[entry]


class Plan(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(Plan, self).__init__(parent)
        self.setStyleSheet("background-color:white;")
        self.setAutoFillBackground(True)

        self.setRenderHint(QtGui.QPainter.Antialiasing)

        self.scene = QtGui.QGraphicsScene()

        self.setScene(self.scene)
        self.scene.setSceneRect(0,0,780,500)


    def analyseExpr(self,txt):
        self.scene.clear()
        entriesObjects = {}
        if txt != "":
            expr = txt
        else:
            #expr = "a and b or ((a and b) or (c and d))"
            expr = "(a and b) or (b and c)"
            #expr = '((a or r) and (a or b)) and (a or x) or not(x and y)'
        print expr
        exprBool = fonction.decompose(expr)
        entries = fonction.donneEntree(exprBool)


        for entry in entries:
            entriesObjects[entry] = Entry(entry, 0, 0, False)

        circuit = Circuit(fonction.composition(exprBool), entriesObjects)
        ggates = circuit.getGates()

        ### On set les positions des gates et entries
        #   Futur migration dans le cricuit.
        x = 0
        for y in range(0,len(ggates)):
            self.gate = ggates[y]
            self.gate.setPos(50+x,656)
            self.scene.addItem(self.gate)
            x += 60

        x = 0
        for y in range(0,len(circuit.lstEntries)):
            #txt = QtGui.QGraphicsTextItem(entry)
            #txt.setPos(10,30+x)
            #self.scene.addItem(txt)
            entry = circuit.lstEntries[entries[y]]
            entry.setPos(10,30+x)
            self.scene.addItem(entry)
            x += 50

        #circuit.showGates()
        circuit.posGates()
        circuit.drawConnection(self.scene)
        #self.scale(2,2)
        self.show()


class Ui_MainWindow(object):
    def setupUi(self, LogicGate):
        LogicGate.setObjectName("LogicGate")
        LogicGate.setMinimumSize(QtCore.QSize(800, 600))
        LogicGate.setMaximumSize(QtCore.QSize(800, 600))

        self.centralwidget = QtGui.QWidget(LogicGate)
        self.centralwidget.setObjectName("centralwidget")

        self.infoLabel = QtGui.QLabel(self.centralwidget)
        self.infoLabel.setGeometry(QtCore.QRect(505, 522, 290, 30))
        self.infoLabel.setObjectName("infoLabel")

        self.analyse = QtGui.QPushButton(self.centralwidget)
        self.analyse.setGeometry(QtCore.QRect(400, 522, 100, 30))
        self.analyse.setObjectName("analyse")

        self.exprBool = QtGui.QLineEdit(self.centralwidget)
        self.exprBool.setGeometry(QtCore.QRect(0, 522, 400, 30))
        self.exprBool.setObjectName("exprBool")

        self.plan = Plan(self.centralwidget)
        self.plan.setFixedSize(800,520)        
        #self.plan.setGeometry(QtCore.QRect(0, 0, 780, 500))
        self.plan.setObjectName("plan")

        LogicGate.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(LogicGate)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName("menu")

        self.menuAnalysis = QtGui.QMenu(self.menubar)
        self.menuAnalysis.setObjectName("menuAnalysis")

        LogicGate.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(LogicGate)
        self.statusbar.setObjectName("statusbar")
        LogicGate.setStatusBar(self.statusbar)

        self.actionOpen = QtGui.QAction(LogicGate)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtGui.QAction(LogicGate)
        self.actionClose.setObjectName("actionClose")
        self.actionAbout = QtGui.QAction(LogicGate)
        self.actionAbout.setObjectName("actionAbout")
        self.actionGraphics = QtGui.QAction(LogicGate)
        self.actionGraphics.setObjectName("actionGraphics")
        self.actionTable = QtGui.QAction(LogicGate)
        self.actionTable.setObjectName("actionTable")

        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)

        self.menu.addAction(self.actionAbout)
        self.menuAnalysis.addAction(self.actionGraphics)
        self.menuAnalysis.addAction(self.actionTable)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(LogicGate)
        QtCore.QObject.connect(self.analyse, QtCore.SIGNAL("clicked()"), self.aExpr)
        QtCore.QMetaObject.connectSlotsByName(LogicGate)

    def aExpr(self):
        self.plan.analyseExpr(self.exprBool.text())

    def retranslateUi(self, LogicGate):
        LogicGate.setWindowTitle(QtGui.QApplication.translate("LogicGate", "LogicGate", None, QtGui.QApplication.UnicodeUTF8))
        self.infoLabel.setText(QtGui.QApplication.translate("LogicGate", "Current expression: None", None, QtGui.QApplication.UnicodeUTF8))
        self.analyse.setText(QtGui.QApplication.translate("LogicGate", "Analyse !", None, QtGui.QApplication.UnicodeUTF8))
        #self.pushButton_2.setText(QtGui.QApplication.translate("LogicGate", "+", None, QtGui.QApplication.UnicodeUTF8))
        #self.pushButton_3.setText(QtGui.QApplication.translate("LogicGate", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("LogicGate", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("LogicGate", "?", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAnalysis.setTitle(QtGui.QApplication.translate("LogicGate", "Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("LogicGate", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("LogicGate", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("LogicGate", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGraphics.setText(QtGui.QApplication.translate("LogicGate", "Graphics", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTable.setText(QtGui.QApplication.translate("LogicGate", "Table", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
