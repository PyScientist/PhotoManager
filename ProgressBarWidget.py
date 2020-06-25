# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python36\Scripts\PhotoManager\ui\ProgressBarWidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressWidget(object):
    def setupUi(self, ProgressWidget):
        ProgressWidget.setObjectName("ProgressWidget")
        ProgressWidget.resize(400, 75)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProgressWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progressBar = QtWidgets.QProgressBar(ProgressWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(ProgressWidget)
        QtCore.QMetaObject.connectSlotsByName(ProgressWidget)

    def retranslateUi(self, ProgressWidget):
        _translate = QtCore.QCoreApplication.translate
        ProgressWidget.setWindowTitle(_translate("ProgressWidget", "Form"))

