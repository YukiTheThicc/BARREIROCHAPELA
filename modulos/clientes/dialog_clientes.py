from datetime import datetime
from PyQt5 import QtWidgets, QtCore

import var
from modulos.clientes import clients
from ventanas.venCalendar import ui_ven_calendar
from ventanas.venConfirmacion import Ui_ven_confirmacion


class DialogEliminar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogEliminar, self).__init__()
        clients.Clientes.dlgEliminarCliente = Ui_ven_confirmacion()
        clients.Clientes.dlgEliminarCliente.setupUi(self)
        self.pregunta = clients.Clientes.dlgEliminarCliente.lbl_pregunta
        clients.Clientes.dlgEliminarCliente.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            clients.Clientes.bajaCliente)
        clients.Clientes.dlgEliminarCliente.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.No).clicked.connect(self.close)


class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        clients.Clientes.dlgCalendar = ui_ven_calendar()
        clients.Clientes.dlgCalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        clients.Clientes.dlgCalendar.calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        clients.Clientes.dlgCalendar.calendar.clicked.connect(clients.Clientes.cargarFecha)
