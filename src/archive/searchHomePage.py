# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchHomePage.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1122, 928)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.SearchComplete = QtGui.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(26)
        self.SearchComplete.setFont(font)
        self.SearchComplete.setFlat(False)
        self.SearchComplete.setObjectName(_fromUtf8("SearchComplete"))
        self.gridLayout.addWidget(self.SearchComplete, 1, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.TopoMap = QtGui.QLabel(self.centralwidget)
        self.TopoMap.setText(_fromUtf8(""))
        self.TopoMap.setPixmap(QtGui.QPixmap(_fromUtf8("topoMap.jpg")))
        self.TopoMap.setObjectName(_fromUtf8("TopoMap"))
        self.gridLayout.addWidget(self.TopoMap, 0, 0, 1, 1)
        self.ToggleLayers = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ToggleLayers.sizePolicy().hasHeightForWidth())
        self.ToggleLayers.setSizePolicy(sizePolicy)
        self.ToggleLayers.setMinimumSize(QtCore.QSize(100, 70))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ToggleLayers.setFont(font)
        self.ToggleLayers.setObjectName(_fromUtf8("ToggleLayers"))
        self.gridLayout.addWidget(self.ToggleLayers, 0, 1, 1, 1, QtCore.Qt.AlignTop)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1122, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Crow\'s Nest", None))
        self.SearchComplete.setText(_translate("MainWindow", "Search Complete", None))
        self.ToggleLayers.setText(_translate("MainWindow", "Toggle Layers", None))

