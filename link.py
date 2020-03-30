# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'link.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(434, 186)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_display = QtWidgets.QLabel(Dialog)
        self.label_display.setObjectName("label_display")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_display)
        self.line_display = QtWidgets.QLineEdit(Dialog)
        self.line_display.setCursorPosition(0)
        self.line_display.setObjectName("line_display")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.line_display)
        self.label_open = QtWidgets.QLabel(Dialog)
        self.label_open.setObjectName("label_open")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_open)
        self.combo_open_in = QtWidgets.QComboBox(Dialog)
        self.combo_open_in.setObjectName("combo_open_in")
        self.combo_open_in.addItem("")
        self.combo_open_in.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.combo_open_in)
        self.label_search = QtWidgets.QLabel(Dialog)
        self.label_search.setObjectName("label_search")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_search)
        self.combo_search_type = QtWidgets.QComboBox(Dialog)
        self.combo_search_type.setObjectName("combo_search_type")
        self.combo_search_type.addItem("")
        self.combo_search_type.addItem("")
        self.combo_search_type.addItem("")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.combo_search_type)
        self.line_search = QtWidgets.QLineEdit(Dialog)
        self.line_search.setObjectName("line_search")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.line_search)
        self.button_current = QtWidgets.QPushButton(Dialog)
        self.button_current.setObjectName("button_current")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.button_current)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        self.combo_open_in.setCurrentIndex(-1)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.line_display, self.combo_open_in)
        Dialog.setTabOrder(self.combo_open_in, self.combo_search_type)
        Dialog.setTabOrder(self.combo_search_type, self.line_search)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add Field"))
        self.label_display.setText(_translate("Dialog", "Field content"))
        self.line_display.setText(_translate("Dialog", "Default"))
        self.label_open.setText(_translate("Dialog", "Open in"))
        self.combo_open_in.setItemText(0, _translate("Dialog", "Browser"))
        self.combo_open_in.setItemText(1, _translate("Dialog", "Previewer"))
        self.label_search.setText(_translate("Dialog", "Search"))
        self.combo_search_type.setItemText(0, _translate("Dialog", "Note ID"))
        self.combo_search_type.setItemText(1, _translate("Dialog", "Card ID"))
        self.combo_search_type.setItemText(2, _translate("Dialog", "Search query"))
        self.line_search.setText(_translate("Dialog", "ID or Query"))
        self.button_current.setText(_translate("Dialog", "Current"))


