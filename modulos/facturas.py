from datetime import datetime
from PyQt5 import QtSql

from venCalendar import *
import var


class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        Facturas.dlgCalendar = ui_ven_calendar()
        Facturas.dlgCalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        Facturas.dlgCalendar.calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        Facturas.dlgCalendar.calendar.clicked.connect(Facturas.cargar_fecha)


class Facturas:

    dlgCalendar = None

    @staticmethod
    def abrir_calendar():
        try:
            Facturas.dlgCalendar.show()
        except Exception as error:
            print('Error en abrir_calendar: %s ' % str(error))

    @staticmethod
    def crear_modulo():
        Facturas.dlgCalendar = DialogCalendar()
        # Conxion del boton de calendario
        var.ui.btn_fac_calendar.clicked.connect(Facturas.abrir_calendar)

    @staticmethod
    def cargar_fecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.edit_fac_calendar.setText(str(data))
            var.dlgCalendar.hide()
        except Exception as error:
            print('Error en cargar_fecha: %s ' % str(error))

    @staticmethod
    def alta_fac():
        dni = var.ui.edit_fac_dni.text()
        nombre = var.ui.edit_fac_nombre.text()
        fecha = var.ui.edit_fac_calendar.text()

    @staticmethod
    def limpiar_fac():
        dni = var.ui.edit_fac_dni.setText("")
        nombre = var.ui.edit_fac_nombre.setText("")
        fecha = var.ui.edit_fac_calendar.setText("")
