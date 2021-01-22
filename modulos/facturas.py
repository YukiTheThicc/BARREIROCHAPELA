from datetime import datetime

from venCalendar import *
import var

class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        var.dlgCalendar = ui_ven_calendar()
        var.dlgCalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgCalendar.calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        var.dlgCalendar.calendar.clicked.connect(Facturas.cargar_fecha)

class Facturas:
    @staticmethod
    def crear_modulo():


    @staticmethod
    def alta_fac():
        dni = var.ui.edit_fac_dni.text()
        nombre = var.ui.edit_fac_nombre.text()
        fecha = var.ui.

    @staticmethod
    def limpiar_fac():