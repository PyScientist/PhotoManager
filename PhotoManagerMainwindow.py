# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python36\Scripts\PhotoManager\ui\PhotoManagerMainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_upper = QtWidgets.QHBoxLayout()
        self.horizontalLayout_upper.setObjectName("horizontalLayout_upper")
        self.toolButton_choose_dir = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_choose_dir.setObjectName("toolButton_choose_dir")
        self.horizontalLayout_upper.addWidget(self.toolButton_choose_dir)
        self.lineEdit_for_dir_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_for_dir_name.setObjectName("lineEdit_for_dir_name")
        self.horizontalLayout_upper.addWidget(self.lineEdit_for_dir_name)
        self.verticalLayout.addLayout(self.horizontalLayout_upper)
        self.horizontalLayout_middle = QtWidgets.QHBoxLayout()
        self.horizontalLayout_middle.setObjectName("horizontalLayout_middle")
        self.listWidget_for_files = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_for_files.setObjectName("listWidget_for_files")
        self.horizontalLayout_middle.addWidget(self.listWidget_for_files)
        self.textEdit_for_report = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_for_report.setObjectName("textEdit_for_report")
        self.horizontalLayout_middle.addWidget(self.textEdit_for_report)
        self.verticalLayout.addLayout(self.horizontalLayout_middle)
        self.horizontalLayout_lower = QtWidgets.QHBoxLayout()
        self.horizontalLayout_lower.setObjectName("horizontalLayout_lower")
        self.toolButton_create_files_set_object = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_create_files_set_object.setObjectName("toolButton_create_files_set_object")
        self.horizontalLayout_lower.addWidget(self.toolButton_create_files_set_object)
        self.toolButton_plot_files_set_object = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_plot_files_set_object.setObjectName("toolButton_plot_files_set_object")
        self.horizontalLayout_lower.addWidget(self.toolButton_plot_files_set_object)
        self.spinBox_of_file_object = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_of_file_object.setMaximumSize(QtCore.QSize(30, 16777215))
        self.spinBox_of_file_object.setObjectName("spinBox_of_file_object")
        self.horizontalLayout_lower.addWidget(self.spinBox_of_file_object)
        self.toolButton_find_figures = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_find_figures.setObjectName("toolButton_find_figures")
        self.horizontalLayout_lower.addWidget(self.toolButton_find_figures)
        self.verticalLayout.addLayout(self.horizontalLayout_lower)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton_choose_dir.setText(_translate("MainWindow", "choose folder"))
        self.toolButton_create_files_set_object.setText(_translate("MainWindow", "Create files set object"))
        self.toolButton_plot_files_set_object.setText(_translate("MainWindow", "plot files set object"))
        self.toolButton_find_figures.setText(_translate("MainWindow", "find figures"))

