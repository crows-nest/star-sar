# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectLayers.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

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
        MainWindow.resize(1095, 681)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("topoMap.jpg")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ChooseLayersText = QtGui.QLabel(self.centralwidget)
        self.ChooseLayersText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.ChooseLayersText.setObjectName(_fromUtf8("ChooseLayersText"))
        self.verticalLayout.addWidget(self.ChooseLayersText, 0, QtCore.Qt.AlignTop)
        self.TopoCheckBox = QtGui.QCheckBox(self.centralwidget)
        self.TopoCheckBox.setIconSize(QtCore.QSize(30, 30))
        self.TopoCheckBox.setChecked(True)
        self.TopoCheckBox.setAutoRepeat(False)
        self.TopoCheckBox.setObjectName(_fromUtf8("TopoCheckBox"))
        self.verticalLayout.addWidget(self.TopoCheckBox, 0, QtCore.Qt.AlignTop)
        self.ProbCheckBox = QtGui.QCheckBox(self.centralwidget)
        self.ProbCheckBox.setIconSize(QtCore.QSize(30, 30))
        self.ProbCheckBox.setObjectName(_fromUtf8("ProbCheckBox"))
        self.verticalLayout.addWidget(self.ProbCheckBox, 0, QtCore.Qt.AlignTop)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1095, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Crow\'s Nest", None))
        self.ChooseLayersText.setText(_translate("MainWindow", "Select your layers:", None))
        self.TopoCheckBox.setText(_translate("MainWindow", "Topographical Map", None))
        self.ProbCheckBox.setText(_translate("MainWindow", "Probability Distribution", None))

if __name__ == "__main__":
    app = QApplication([])

    test = Ui_MainWindow()
    window = QtWidget()
    test.setupUi(window)
    window.show()
    app.exec_()



