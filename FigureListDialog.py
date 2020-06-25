# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python36\Scripts\PhotoManager\ui\FigureListDialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Visualise_figure_list_form(object):
    def setupUi(self, Visualise_figure_list_form):
        Visualise_figure_list_form.setObjectName("Visualise_figure_list_form")
        Visualise_figure_list_form.setWindowModality(QtCore.Qt.WindowModal)
        Visualise_figure_list_form.resize(500, 458)
        self.verticalLayout = QtWidgets.QVBoxLayout(Visualise_figure_list_form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_first = QtWidgets.QHBoxLayout()
        self.horizontalLayout_first.setObjectName("horizontalLayout_first")
        self.list_widget_figures = QtWidgets.QListWidget(Visualise_figure_list_form)
        self.list_widget_figures.setObjectName("list_widget_figures")
        self.horizontalLayout_first.addWidget(self.list_widget_figures)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_for_figure_show = QtWidgets.QLabel(Visualise_figure_list_form)
        self.label_for_figure_show.setObjectName("label_for_figure_show")
        self.verticalLayout_2.addWidget(self.label_for_figure_show)
        self.Statistics_Field = QtWidgets.QTextEdit(Visualise_figure_list_form)
        self.Statistics_Field.setObjectName("Statistics_Field")
        self.verticalLayout_2.addWidget(self.Statistics_Field)
        self.horizontalLayout_first.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_first)
        self.horizontalLayout_second = QtWidgets.QHBoxLayout()
        self.horizontalLayout_second.setObjectName("horizontalLayout_second")
        self.show_dupicate_figures_button = QtWidgets.QToolButton(Visualise_figure_list_form)
        self.show_dupicate_figures_button.setObjectName("show_dupicate_figures_button")
        self.horizontalLayout_second.addWidget(self.show_dupicate_figures_button)
        self.print_report_button = QtWidgets.QToolButton(Visualise_figure_list_form)
        self.print_report_button.setObjectName("print_report_button")
        self.horizontalLayout_second.addWidget(self.print_report_button)
        self.buttonBox = QtWidgets.QDialogButtonBox(Visualise_figure_list_form)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_second.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_second)

        self.retranslateUi(Visualise_figure_list_form)
        QtCore.QMetaObject.connectSlotsByName(Visualise_figure_list_form)

    def retranslateUi(self, Visualise_figure_list_form):
        _translate = QtCore.QCoreApplication.translate
        Visualise_figure_list_form.setWindowTitle(_translate("Visualise_figure_list_form", "Visualise figure list"))
        self.label_for_figure_show.setText(_translate("Visualise_figure_list_form", "Your figure will be here"))
        self.show_dupicate_figures_button.setText(_translate("Visualise_figure_list_form", "show duplicates"))
        self.print_report_button.setText(_translate("Visualise_figure_list_form", "print_report"))

