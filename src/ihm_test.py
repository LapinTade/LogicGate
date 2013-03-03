#-*- coding: utf-8 -*- 
from PyQt4 import QtCore, QtGui, QtOpenGL

import sys, random

#@TODO Faire des fichiers séparé par classe :p

#TEST
class Gate(QtGui.QGraphicsItem):
    def __init__(self, x, y, size=20, scale=1, parent=None):
        super(Gate, self).__init__(parent)
        self.x = x
        self.y = y
        self.size = size
        self.scale = scale

        self.setPos(self.x,self.y)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return QtCore.QRectF(0,0,self.size*2,self.size+(self.size/2))

    def paint(self, painter, option, parent=None):
        painter.setPen(QtGui.QColor("black"))
# painter.drawEllipse(QtCore.QRectF(self.size+(self.size/2),(self.size/4),(self.size/2),(self.size/2)))

class AndGate(Gate):
    def __init__(self,*args,**kwargs):
        super(AndGate, self).__init__(*args,**kwargs)
    
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

    def paint(self, painter, option, parent=None):
        super(OrGate, self).paint(painter,option)



class NotGate(Gate):
    def __init__(self,*args,**kwargs):
        super(NotGate, self).__init__(*args,**kwargs)

    def paint(self, painter, option, parent=None):
        super(NotGate, self).paint(painter,option)
        painter.drawText(self.size/2,(self.size/2)+(self.size/8),"1")
        painter.drawLine(0,0,0,self.size)
        painter.drawLine(0,0,self.size,self.size/2)
        painter.drawLine(0,self.size,self.size,self.size/2)


class Plan(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(Plan, self).__init__(parent)
        self.setStyleSheet("background-color:white;")
        self.setAutoFillBackground(True)

        self.setRenderHint(QtGui.QPainter.Antialiasing)

        self.scene = QtGui.QGraphicsScene()

        self.setScene(self.scene)
        self.scene.setSceneRect(0,0,780,500)

        self.gate = NotGate(50,50)
        self.scene.addItem(self.gate)

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

        """self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(780, 501, 20, 20))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(757, 501, 20, 20))
        self.pushButton_3.setObjectName("pushButton_3")

        self.horizontalScrollBar = QtGui.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(0, 500, 755, 20))
        self.horizontalScrollBar.setMinimum(-99)
        self.horizontalScrollBar.setSliderPosition(0)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")

        self.verticalScrollBar = QtGui.QScrollBar(self.centralwidget)
        self.verticalScrollBar.setGeometry(QtCore.QRect(780, 0, 20, 500))
        self.verticalScrollBar.setMinimum(-99)
        self.verticalScrollBar.setProperty("value", 0)
        self.verticalScrollBar.setSliderPosition(0)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")"""

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
        QtCore.QMetaObject.connectSlotsByName(LogicGate)

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
