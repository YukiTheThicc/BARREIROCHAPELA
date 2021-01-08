from PyQt5 import QtPrintSupport

import clients
from productos import prep_productos as p
import conexion
import events
import sys
import var
from datetime import datetime

from venAviso import *
from venCalendar import *
from venPrincipal import *
from venConfirmacion import *
from venAcercaDe import *


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


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.dlgAbout = DialogAbout()
        var.dlgAviso = DialogAviso()
        var.dlgSalir = DialogSalir()
        var.dlgCalendar = DialogCalendar()
        var.dlgEliminarCliente = DialogEliminarCliente()
        var.dlgBuscador = DialogBuscador()
        var.dlgImprimir = DialogImpresora()
        var.dni_valido = False

        # Arrays con los botones chk y rbt
        var.rbtSex = (var.ui.rbt_fem, var.ui.rbt_mas)
        var.chkPago = (var.ui.chk_efect, var.ui.chk_tarje, var.ui.chk_trans)

        '''
        Conexion de eventos con los elementos de la Interfaz
        '''
        # Conexion de los elementos que crean el dialogo para salir del programa
        var.ui.btn_salir.clicked.connect(events.Eventos.salir)
        var.ui.actionSalir.triggered.connect(events.Eventos.salir)
        # Conecta el edit de DNI con la funcion que valida si es correcto o no
        var.ui.edit_dni.editingFinished.connect(lambda: clients.Clientes.resValidarDni())
        # Conecta clicar el calendar con la funcion que abre la venCalendar
        var.ui.btn_calendar.clicked.connect(clients.Clientes.abrirCalendar)
        # Conecta clicar el boton de guardar con la funcion que guarda el cliente en la
        # base de datos y lo carga en la tabla de la Interfaz
        var.ui.btn_guardar.clicked.connect(clients.Clientes.altaCliente)
        # Conecta clicar el boton de limpiar con la funcion que limpia los campos de la
        # Interfaz
        var.ui.btn_limpiar.clicked.connect(clients.Clientes.limpiarCli)
        # Conecta clicar el boton de eliminar con la funcion que elimina un cliente de la
        # base de datos
        var.ui.btn_eliminar.clicked.connect(events.Eventos.eliminar)
        # Conecta clicar el boton de modificar con la funcion que modifica el cliente con
        # el DNI en el editBox del DNI
        var.ui.btn_modificar.clicked.connect(clients.Clientes.modifCliente)
        # Conecta la apertura de la combo con la funcion que lee lo que seleccione el usuario
        var.ui.cmb_prov.activated[str].connect(clients.Clientes.selProv)
        # Conecta clicar un cliente de la lista de clientes con la funcion que carga sus
        # datos en los campos de la Interfaz
        var.ui.tbl_listcli.clicked.connect(clients.Clientes.cargarCli)
        # Conecta que el evento clicar en la tabla conecte con una funcion que seleciona la
        # tupla entera
        var.ui.tbl_listcli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        # Carga la comboBox de provincias en blanco
        events.Eventos.cargar_prov()
        # Conecta clicar en el boton de racargar con la funcion que recarga todos los clientes en la tabla
        var.ui.btn_recargar.clicked.connect(clients.Clientes.recargar)
        # Conecta clicar en el boton de buscar con la funcion que busca un cliente segun su dni
        var.ui.btn_buscar.clicked.connect(clients.Clientes.buscar)
        var.ui.statusbar.addPermanentWidget(var.ui.lbl_status, 1)
        var.ui.lbl_status.setText('Buenos Días')
        # Ponemos valor 18 por defecto en la spinBox de edad
        var.ui.sbox_edad.setValue(18)
        # Ponemos el valor minimo de la spinBox
        var.ui.sbox_edad.setMinimum(18)
        # Ponemos el valor maximo de la spinBox
        var.ui.sbox_edad.setMaximum(120)

        var.ui.actionsalir.triggered.connect(events.Eventos.salir)
        var.ui.actionBuscador.triggered.connect(events.Eventos.abrir_buscador)
        var.ui.actionImpresora.triggered.connect(events.Eventos.abrir_impresora)

        # ---------------------------PARA EXAMEN-------------------------
        p.PrepProductos.crear_conexiones()

        var.ui.action_about.triggered.connect(events.Eventos.about)
        # ---------------------------FIN DE PARA EXAMEN-------------------------
        for i in var.rbtSex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkPago:
            i.stateChanged.connect(clients.Clientes.selPago)

        # Conexion con la base de datos
        conexion.Conexion.db_connect(var.filebd)
        # Muestra en la tabla los clientes guardados en la base de datos
        conexion.Conexion.mostrar_clientes()
        conexion.Conexion.actualizar_tabla_pro()

    def closeEvent(self, event):
        if event:
            events.Eventos.salir(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
