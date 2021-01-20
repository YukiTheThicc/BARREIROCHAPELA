import

import var


class DialogEliminarCliente(QtWidgets.QDialog):
    def __init__(self):
        super(DialogEliminarCliente, self).__init__()
        var.dlgEliminarCliente = Ui_ven_confirmacion()
        var.dlgEliminarCliente.setupUi(self)
        self.pregunta = var.dlgEliminarCliente.lbl_pregunta
        var.dlgEliminarCliente.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            clients.Clientes.bajaCliente)
        var.dlgEliminarCliente.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.No).clicked.connect(self.close)


class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        var.dlgCalendar = ui_ven_calendar()
        var.dlgCalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgCalendar.calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        var.dlgCalendar.calendar.clicked.connect(clients.Clientes.cargarFecha)