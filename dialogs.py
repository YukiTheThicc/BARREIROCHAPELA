from datetime import datetime
from PyQt5 import QtPrintSupport

from ventanas.venAviso import *
from ventanas.venCalendar import *
from ventanas.venPrincipal import *
from ventanas.venConfirmacion import *
from ventanas.venAcercaDe import *
import var
import events


class DialogAviso(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAviso, self).__init__()
        var.dlgAviso = Ui_ven_aviso()
        var.dlgAviso.setupUi(self)
        var.dlgAviso.btn_ok.clicked.connect(self.close)
        var.lbl_mensaje = var.dlgAviso.lbl_mensaje
        var.lbl_mensaje.setText("Mensaje por defecto")


class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.dlgSalir = Ui_ven_confirmacion()
        var.dlgSalir.setupUi(self)
        var.lbl_pregunta = var.dlgSalir.lbl_pregunta
        var.dlgSalir.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.salir)
        var.lbl_pregunta.setText("")


class DialogBuscador(QtWidgets.QFileDialog):
    def __init__(self):
        super(DialogBuscador, self).__init__()
        self.setWindowTitle('Abrir Archivo')
        self.setModal(True)


class DialogImpresora(QtPrintSupport.QPrintDialog):
    def __init__(self):
        super(DialogImpresora, self).__init__()


class DialogAbout(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAbout, self).__init__()
        var.dlgAviso = Ui_ven_acercade()
        var.dlgAviso.setupUi(self)
        var.dlgAviso.btn_ok.clicked.connect(self.close)