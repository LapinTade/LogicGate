#-*- coding: utf-8 -*- 
from PyQt4 import QtCore, QtGui 
from PyQt4.QtCore import pyqtSignal,pyqtSlot
import fonction
import math

import sys, random

#@TODO Faire des fichiers séparé par classe :p
#   Ajouter les not entrée et sortie
#   Rectifier les lignes entrees et sorties
#   ...

def debug_trace():
  '''Set a tracepoint in the Python debugger that works with Qt'''
  from PyQt4.QtCore import pyqtRemoveInputHook
  from pdb import set_trace
  pyqtRemoveInputHook()
  set_trace()


class Out(QtGui.QGraphicsObject,QtGui.QGraphicsItem):
    def __init__(self, name, x, y, value=False, plan=None, lastGate=None, parent=None):
        super(Out, self).__init__(parent)
        self.name = name
        self.x = x
        self.y = y
        self.value = value

        self.lastGate = lastGate

        self.plan = plan

    def boundingRect(self):
        return QtCore.QRectF(-10,-10,40,12)

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def setValue(self):
        self.value = self.lastGate.getValue()

    def mousePressEvent(self,event):
        self.plan.setGValues()
        self.plan.update()
        print 'X:%s, Y:%s === name: %s | Valeur: %s' % (self.pos().x(), self.pos().y(),self.name, self.value)

    def paint(self, painter, option, parent=None):
        if self.value:
            painter.setPen(QtGui.QColor("green"))
        else:
            painter.setPen(QtGui.QColor("red"))
        painter.drawText(self.x,self.y,self.name)
        painter.drawRect(self.boundingRect())



class Entry(QtGui.QGraphicsObject,QtGui.QGraphicsItem):
    #signal = QtCore.pyqtSignal()

    def __init__(self, name, x, y, value=False, plan=None,parent=None):
        super(Entry, self).__init__(parent)
        self.name = name
        self.x = x
        self.y = y
        self.value = value

        self.plan = plan

        #self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)

    def __str__(self):
        return str(self.name)

    """def setPos(self, x, y):
                    self.x = x
                    self.y = y
                    super(Entry, self).setPos(x,y)"""


    def boundingRect(self):
        return QtCore.QRectF(-10,-10,20,12)

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def setValue(self, value):
        self.value = value

    def mousePressEvent(self,event):
        self.value = not self.value
        self.plan.setGValues()
        self.plan.update()
        print 'X:%s, Y:%s === name: %s | Valeur: %s' % (self.pos().x(), self.pos().y(),self.name, self.value)

    def paint(self, painter, option, parent=None):
        if self.value:
            painter.setPen(QtGui.QColor("green"))
        else:
            painter.setPen(QtGui.QColor("red"))
        painter.drawText(self.x,self.y,self.name)
        painter.drawRect(self.boundingRect())

        """if(self.isSelected()):
            print 'X:%s, Y:%s === name: %s | Valeur: %s' % (self.pos().x(), self.pos().y(),self.name, self.value)
            self.value = not self.value
            print "#", self.plan
            self.plan.setGValues()
            #self.plan.update()
            self.setSelected(False)
            #self.plan.getView().update()
            #self.signal.connect(self.plan.setGValues)
            #self.signal.emit()"""
            


class Gate(QtGui.QGraphicsItem):
    def __init__(self, x, y, value=False,size=20, scale=1, parent=None):
        super(Gate, self).__init__(parent)
        self.size = size
        self.scale = scale

        self.value = value

        self.setPos(x,y)

        #self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)

        self.entreeA = None
        self.entreeB = None

        self.entreeAX = 0
        self.entreeAY = 0

        self.entreeBX = 0
        self.entreeBY = self.size

        self.sortieX = self.size+(self.size/2)
        self.sortieY = self.size/2

        self.entryIsNot = [False,False]
        self.gateNot = False


    #def __str__(self):
        #return "entreeA: " + self.entreeA + ", entreeB: " + self.entreeB


    def getValue(self):
        if self.value is None:
            if self.entreeA is None or self.entreeB is None:
                return None
            else:
                if isinstance(self.entreeA, Gate):
                    self.entreeA.getValue()
                if isinstance(self.entreeB, Gate):
                    self.entreeB.getValue()

                self.setValue()
                if self.gateNot:
                    return not self.value
                else:
                    return self.value
        else:
            if self.gateNot:
                return not self.value
            else:
                return self.value

    def boundingRect(self):
        return QtCore.QRectF(0,0,self.size*2,self.size+(self.size/2))

    def setEntryIsNot(self,index):
        self.entryIsNot[index] = True

    def setGateNot(self):
        self.gateNot = True

    def getGateNot(self):
        return self.gateNot

    def getEntryIsNot(self):
        return self.entryIsNot

    def mousePressEvent(self, event):
        self.setValue()

    def getCoordEntreeA(self):
        return self.scenePos() + QtCore.QPointF(self.entreeAX,self.entreeAY)

    def getCoordEntreeB(self):
        return self.scenePos() + QtCore.QPointF(self.entreeBX,self.entreeBY)

    def getCoordSortie(self):
        return self.scenePos() + QtCore.QPointF(self.sortieX,self.sortieY)

    def paint(self, painter, option, parent=None):
        """painter.setPen(QtGui.QColor("black"))
        painter.drawPoint(QtCore.QPointF(self.entreeAX,self.entreeAY))
        painter.drawPoint(QtCore.QPointF(self.entreeBX,self.entreeBY))
        painter.drawPoint(QtCore.QPointF(self.sortieX,self.sortieY))"""

        if self.value:
            painter.setPen(QtGui.QColor("green"))
        else:
            painter.setPen(QtGui.QColor("red"))


# painter.drawEllipse(QtCore.QRectF(self.size+(self.size/2),(self.size/4),(self.size/2),(self.size/2)))
        """if(self.isSelected()):
            print "\nid(self): %s" % (id(self))
            print "X:%s, Y:%s === entreeA: %s, entreeB: %s" % (self.pos().x(), self.pos().y(), type(self.entreeA), type(self.entreeB))
            print "entreeA: %s, Add entreeB: %s" % (id(self.entreeA), id(self.entreeB))
            print self.value
            self.setValue()
            print "Updated"""

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


    def setValue(self):
        #Cas erreur
        if self.entreeA is None or self.entreeB is None:
            pass
        else:
            retA = self.entreeA.getValue()
            retB = self.entreeB.getValue()
            if self.entryIsNot[0]:
                retA = not retA
            if self.entryIsNot[1]:
                retB = not retB

            self.value = retA and retB


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

    def setValue(self):
        #Cas erreur
        if self.entreeA is None or self.entreeB is None:
            pass
        else:
            retA = self.entreeA.getValue()
            retB = self.entreeB.getValue()
            if self.entryIsNot[0]:
                retA = not retA
            if self.entryIsNot[1]:
                retB = not retB

            self.value = retA or retB

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
        painter.setPen(QtGui.QColor("white"))
        painter.drawLine(0,self.size/2,self.size,self.size/2)
        painter.setPen(QtGui.QColor("black"))
        #painter.drawText(0,(self.size/2)+(self.size/5),"1")
        painter.drawLine(0,0,0,self.size)
        painter.drawLine(0,0,self.size,self.size/2)
        painter.drawLine(0,self.size,self.size,self.size/2)


class Connexion(QtGui.QGraphicsLineItem):
    def __init__(self,x1,y1,x2,y2,parent=None):
        super(Connexion, self).__init__(parent)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.midX = (x1 + x2) / 2
        self.midY = (y1 + y2) / 2


    def paint(self, painter, option, parent=None):
        """
        (x1,y1)___(self.midX,y1)
                        |
                        |
                        |
                  (self.midX,y2) ____ (x2,y2)
        """
        painter.setPen(QtGui.QColor("black"))
        painter.drawLine(self.x1,self.y1,self.midX,self.y1)
        painter.drawLine(self.midX,self.y1,self.midX,self.y2)
        painter.drawLine(self.midX,self.y2,self.x2,self.y2)



class Circuit(object):
    def __init__(self, inputGates, inputEntries, plan):
        self.circuit = inputGates
        self.lstGates = {}
        self.lstEntries = {}

        """self.gates = { "or" : OrGate(0,0),
                        "and" : AndGate(0,0),
                        "xor" : XOrGate(0,0),
                        "not" : NotGate(0,0)}.get(valeur,None)()"""
        x = 0

        #Creation des gates
        print self.circuit
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

        #creation des entries
        for entry in inputEntries:
            self.lstEntries[entry] = Entry(entry, 0, 0, False, plan)


        # Linkage des entrees
        for x in range(0,len(self.circuit)):
            #print "TYPE1:",type(self.entryCreator(porte[0]))
            #print "TYPE1:",type(self.entryCreator(porte[2]))
            gate = self.lstGates[x]
            gate.setEntries(self.entryCreator(self.circuit[x][0],gate,0),self.entryCreator(self.circuit[x][2],gate,1))

        self.lastGate = self.lstGates[len(self.lstGates)-1]
        self.out = Out("Exit",0,0,False, plan, self.lastGate)

    def posGates(self,scene):
        notPosedGate = []
                        
        for k in range(0,len(self.lstGates)):
            notPosedGate.append(True)

        x = 50
        shift = 60
        entryShift = 15

        print "PLACING"

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
                        x += entryShift

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
        

        yMin,yMax = 2000,0
        for index in self.lstEntries:
            entry = self.lstEntries[index]
            entryY = entry.pos().y()
            if entryY > yMax:
                yMax = entryY
            if entryY < yMin:
                yMin = entryY
        
        self.out.setX(self.lastGate.pos().x()+shift)
        self.out.setY(math.fabs(yMax + yMin)/2)

        scene.addItem(self.out)

    def drawConnections(self,scene):
        for gate in self.lstGates:
            # Porte concernée
            gateX = int(self.lstGates[gate].pos().x())
            gateY = int(self.lstGates[gate].pos().y())

            gatePointA = self.lstGates[gate].getCoordEntreeA()
            gatePointB = self.lstGates[gate].getCoordEntreeB()

            gateAX,gateAY = gatePointA.x(),gatePointA.y()
            gateBX,gateBY = gatePointB.x(),gatePointB.y()

            # Autres portes/entree
            entryA, entryB = self.lstGates[gate].getEntries()
            entryAX = int(entryA.pos().x()+15)
            entryAY = int(entryA.pos().y())
            entryBX = int(entryB.pos().x()+15)
            entryBY = int(entryB.pos().y())

            #Cas si ce sont des portes, on redefinit les coord
            if isinstance(entryA, Gate):
                entryPointA = entryA.getCoordSortie()
                entryAX, entryAY = entryPointA.x(),entryPointA.y()

            if isinstance(entryB, Gate):
                entryPointB = entryB.getCoordSortie() 
                entryBX, entryBY = entryPointB.x(),entryPointB.y()

            #On inverse les entryA et entryB si B est au dessous de A
            if entryAY > entryBY:
                tmpX = entryAX
                tmpY = entryAY
                entryAX = entryBX
                entryAY = entryBY
                entryBX = tmpX
                entryBY = tmpY


            #scene.addItem(QtGui.QGraphicsLineItem(gateX,gateY,entryAX,entryAY))
            #scene.addItem(QtGui.QGraphicsLineItem(gateX,gateY,entryBX,entryBY))
            #con1 = Connexion(gateX,gateY,entryAX,entryAY)
            #con2 = Connexion(gateX,gateY,entryBX,entryBY)
            self.drawConnexion(scene,gateAX,gateAY,entryAX,entryAY)
            self.drawConnexion(scene,gateBX,gateBY,entryBX,entryBY)
            #scene.addItem(con1)
            #scene.addItem(con2)
            #print "\nEntryA: %s EntryB: %s" % (entryA.pos(),entryB.pos())
            #print "A( %s, %s); B( %s, %s)" % (entryAX,entryAY, entryBX,entryBY)
            if self.lstGates[gate].getEntryIsNot()[0]:
                notG = NotGate(gateAX-15,gateAY-5,False,10)
                scene.addItem(notG)
            if self.lstGates[gate].getEntryIsNot()[1]:
                notG = NotGate(gateBX-15,gateBY-5,False,10)
                scene.addItem(notG)
            if self.lstGates[gate].getGateNot():
                #@TODO
                #   Bouger ce putain de cercle ;)
                #   Definir quand une porte est gateNot
                scene.addItem(QtGui.QGraphicsEllipseItem(QtGui.QRectF(gateAX,gateAY,5,5)))


        xLast, yLast = self.lastGate.getCoordSortie().x(),self.lastGate.getCoordSortie().y()
        self.drawConnexion(scene,self.out.pos().x(),self.out.pos().y(), xLast, yLast)

    def drawConnexion(self,scene,x1,y1,x2,y2):
        midX = (x1 + x2) / 2
        """
        (x1,y1)___(self.midX,y1)
                        |
                        |
                        |
                  (self.midX,y2) ____ (x2,y2)
        """
        scene.addItem(QtGui.QGraphicsLineItem(x1,y1,midX,y1))
        scene.addItem(QtGui.QGraphicsLineItem(midX,y1,midX,y2))
        scene.addItem(QtGui.QGraphicsLineItem(midX,y2,x2,y2))

    def desc(self):
        print "\nGates Values:"
        gates = self.lstGates
        for gate in gates:
            print gates[gate].getValue()

        print "\nEntries Value:"
        entries = self.lstEntries
        for entry in entries:
            print entries[entry].getValue()


    def showGates(self):
        for porte in self.circuit:
            print porte[1]

    def showEntries(self):
        print self.lstEntries

    def getGates(self):
        return self.lstGates

    def getEntries(self):
        return self.lstEntries

    def showGates(self):
        print self.lstGates

    def getOut(self):
        return self.out

    def entryCreator(self, entry, gate, index):
        if "not" in entry:
            print "\nNOT ENTRY", entry,"gate", gate,"index" ,index,"\n"
            gate.setEntryIsNot(index)
            return self.lstEntries[entry[4:]]
        try:
            entry = int(entry)
            return self.lstGates[entry]
        except:
            return self.lstEntries[entry]


class Plan(QtGui.QGraphicsView):
    def __init__(self, view, parent=None,):
        super(Plan, self).__init__(parent)
        self.setStyleSheet("background-color:white;")
        self.setAutoFillBackground(True)
        self.setViewportUpdateMode(QtGui.QGraphicsView.SmartViewportUpdate)

        self.setRenderHint(QtGui.QPainter.Antialiasing)

        self.scene = QtGui.QGraphicsScene()

        self.setScene(self.scene)
        self.scene.setSceneRect(0,0,780,500)

        self.circuit = None
        self.view = view

    def analyseExpr(self,txt, nat):
        self.scene.clear()
        entriesObjects = {}
        txt = str(txt)
        if txt != "":
            expr = txt
        else:
            #expr = "a and b or ((a and b) or (c and d))"
            #expr = "(a and b) or (b and c)"
            #expr = "(a and b) or (c and (a and b))"
            expr = "(((a or b) and c) and a)"
            #expr = "(((a and b) and v) or c)"
            #expr = '((a or r) and (a or b)) and (a or x) or not(x and y)'
        print expr
        exprBool = fonction.decompose(expr)
        entries = fonction.donneEntree(exprBool)

        print fonction.composition(exprBool)

        self.circuit = Circuit(fonction.composition(exprBool), entries, self)
        ggates = self.circuit.getGates()


        if nat == "circuit":

            ### On set les positions des gates et entries
            #   Futur migration dans le cricuit.
            x = 0
            for y in range(0,len(ggates)):
                gate = ggates[y]
                gate.setPos(50+x,656)
                self.scene.addItem(gate)
                x += 60

            x = 0
            for y in range(0,len(self.circuit.lstEntries)):
                #txt = QtGui.QGraphicsTextItem(entry)
                #txt.setPos(10,30+x)
                #self.scene.addItem(txt)
                entry = self.circuit.lstEntries[entries[y]]
                entry.setPos(10,30+x)
                self.scene.addItem(entry)
                x += 500 / len(self.circuit.lstEntries)

            #self.circuit.showGates()
            self.circuit.posGates(self.scene)
            self.circuit.drawConnections(self.scene)
            #self.scale(2,2)

            self.circuit.desc()
            self.setGValues()
        else:
            print "hello"
            self.scene.addItem(QtGui.QGraphicsLineItem(0,0,0,40))
            
            x=0
            for y in range(0,len(self.circuit.lstEntries)):
                entry = self.circuit.lstEntries[entries[y]]
                entry.setPos(30+x,10)
                self.scene.addItem(entry)
                x += 500 / len(self.circuit.lstEntries)
                self.scene.addItem(QtGui.QGraphicsLineItem(x,0,x,40))

            self.scene.addItem(QtGui.QGraphicsLineItem(0,40,x,40))

            txt = QtGui.QGraphicsTextItem("Entries")
            txt.setPos(0,40)
            self.scene.addItem(txt)

            txt = QtGui.QGraphicsTextItem("And Gates")
            txt.setPos(20,80)
            self.scene.addItem(txt)

            txt = QtGui.QGraphicsTextItem("Or Gates")
            txt.setPos(500,80)
            self.scene.addItem(txt)

            self.scene.addItem(QtGui.QGraphicsLineItem(0,70,0,300))
            self.scene.addItem(QtGui.QGraphicsLineItem(400,70,400,300))

            x,y=10,0
            x2,y2=10,0
            for k in range(0,len(ggates)):
                gate = ggates[k]
                if isinstance(gate, AndGate):
                    gate.setPos(0+x,110 + y)
                if isinstance(gate, OrGate):
                    gate.setPos(410+x2,110 + y2)

                self.scene.addItem(gate)
                x += 40
                if x > 200:
                    x = 0
                    y += 20
                x2 += 40
                if x2 > 200:
                    x2 = 0
                    y2 += 20

            out = self.circuit.getOut()
            out.setPos(50,400)
            self.scene.addItem(out)

            self.scene.addItem(QtGui.QGraphicsRectItem(0,350,150,100))

            txt = QtGui.QGraphicsTextItem("Entries")
            txt.setPos(0,350)
            self.scene.addItem(txt)


    @pyqtSlot()
    def setGValues(self):
        gates = self.circuit.getGates()
        for gate in gates:
            gates[gate].setValue()
            
        for gate in gates:
            gates[gate].setValue()
        self.circuit.desc()

        out = self.circuit.getOut()
        out.setValue()

    def getView(self):
        return self.view


class Ui_MainWindow(object):
    def setupUi(self, LogicGate):
        self.nat = "circuit"

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

        self.plan = Plan(LogicGate, self.centralwidget)
        self.plan.setFixedSize(800,520)        
        #self.plan.setGeometry(QtCore.QRect(0, 0, 780, 500))
        self.plan.setObjectName("plan")
        print "###",self.plan

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
        self.actionClose.triggered.connect(QtGui.qApp.quit)
        QtCore.QObject.connect(self.actionGraphics, QtCore.SIGNAL("triggered()"), lambda n="circuit": self.setNat(n))
        QtCore.QObject.connect(self.actionTable, QtCore.SIGNAL("triggered()"), lambda n="table": self.setNat(n))
        QtCore.QObject.connect(self.analyse, QtCore.SIGNAL("clicked()"), self.aExpr)
        QtCore.QMetaObject.connectSlotsByName(LogicGate)

    def setNat(self, nat):
        self.nat = nat

    def aExpr(self):
        self.plan.analyseExpr(self.exprBool.text(),self.nat)

    def retranslateUi(self, LogicGate):
        LogicGate.setWindowTitle(QtGui.QApplication.translate("LogicGate", "LogicGate", None, QtGui.QApplication.UnicodeUTF8))
        self.infoLabel.setText(QtGui.QApplication.translate("LogicGate", "Current expression: None", None, QtGui.QApplication.UnicodeUTF8))
        self.analyse.setText(QtGui.QApplication.translate("LogicGate", "Analyse !", None, QtGui.QApplication.UnicodeUTF8))
        #self.pushButton_2.setText(QtGui.QApplication.translate("LogicGate", "+", None, QtGui.QApplication.UnicodeUTF8))
        #self.pushButton_3.setText(QtGui.QApplication.translate("LogicGate", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("LogicGate", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("LogicGate", "?", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAnalysis.setTitle(QtGui.QApplication.translate("LogicGate", "Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("LogicGate", "Open (not implanted yet)", None, QtGui.QApplication.UnicodeUTF8))
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
