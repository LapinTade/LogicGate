from PyQt4 import QtCore, QtGui, QtOpenGL

import sys, random

#@TODO Faire des fichiers séparé par classe :p

class Gate(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        print "test"
        # On va essayer de faire des item personnalisé, on pourra les drag and drop etc...


class Plan(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(Plan, self).__init__(parent)
        self.setStyleSheet("background-color:white;")
        self.setAutoFillBackground(True)

        self.setRenderHint(QtGui.QPainter.Antialiasing)

        self.scene = QtGui.QGraphicsScene()

        self.drawAndGate(50,50)

        self.setScene(self.scene)
        self.scene.setSceneRect(0,0,780,500)
        self.show()


    def drawAndGate(self,x,y,scale=1,h=20,w=20):
        h_size = h * scale
        dh_size = (h_size/2)
        w_size = w * scale
        dw_size = (w_size/2)
        startAngle = 90 * 16
        endAngle = -180 * 16

        self.drawLine(x,y,x+h_size,y)
        self.drawLine(x,y,x,y+w_size)
        self.drawLine(x+h_size,y+w_size,x,y+w_size)
        self.drawArc(x+dh_size,y,h_size,w_size,startAngle,endAngle)
        self.drawText(x,y-3,"&")

    def drawLine(self,x1,y1,x2,y2):
        line=QtGui.QGraphicsLineItem(x1,y1,x2,y2)
        self.scene.addItem(line)

    def drawArc(self,x,y,height,width,startAngle,endAngle):
        arc=QtGui.QGraphicsEllipseItem(x,y,height,width)
        arc.setStartAngle(startAngle)
        arc.setSpanAngle(endAngle)
        self.scene.addItem(arc)

    def drawText(self,x,y,string):
        txt = QtGui.QGraphicsTextItem(string)
        txt.setPos(x,y)
        self.scene.addItem(txt)


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