# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'venAviso.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import var


class Ui_ven_aviso(object):
    def setupUi(self, ven_aviso):
        ven_aviso.setObjectName("ven_aviso")
        ven_aviso.resize(341, 98)
        ven_aviso.setModal(True)
        self.btn_ok = QtWidgets.QPushButton(ven_aviso)
        self.btn_ok.setGeometry(QtCore.QRect(170, 60, 75, 23))
        self.btn_ok.setObjectName("btn_ok")
        var.lbl_mensaje = QtWidgets.QLabel(ven_aviso)
        var.lbl_mensaje.setGeometry(QtCore.QRect(130, 30, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        var.lbl_mensaje.setFont(font)
        var.lbl_mensaje.setAlignment(QtCore.Qt.AlignCenter)
        var.lbl_mensaje.setObjectName("lbl_mensaje")
        self.lbl_icono = QtWidgets.QLabel(ven_aviso)
        self.lbl_icono.setGeometry(QtCore.QRect(40, 20, 61, 61))
        self.lbl_icono.setMinimumSize(QtCore.QSize(51, 0))
        self.lbl_icono.setText("")
        self.lbl_icono.setPixmap(QtGui.QPixmap(":/avisosalir/img/iconoaviso.png"))
        self.lbl_icono.setScaledContents(True)
        self.lbl_icono.setObjectName("lbl_icono")

        self.retranslateUi(ven_aviso)
        QtCore.QMetaObject.connectSlotsByName(ven_aviso)

    def retranslateUi(self, ven_aviso):
        _translate = QtCore.QCoreApplication.translate
        ven_aviso.setWindowTitle(_translate("ven_aviso", "Aviso"))
        self.btn_ok.setText(_translate("ven_aviso", "OK"))
        var.lbl_mensaje.setText(_translate("ven_aviso", "Aviso por defecto"))

import avisosalir_rc
