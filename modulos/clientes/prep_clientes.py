from PyQt5 import QtWidgets

import events
import var

from modulos.clientes import clients
from modulos.clientes.dialog_clientes import DialogCalendar, DialogEliminarCliente


class Clientes():
    def crear_modulo(self):
        var.dlgCalendar = DialogCalendar()
        var.dlgEliminarCliente = DialogEliminarCliente()

        self.crear_conexiones()


    @staticmethod
    def crear_conexiones():
        var.ui.actionSalir.triggered.connect(events.Eventos.salir)
        # Conexion de los elementos que crean el dialogo para salir del programa
        var.ui.btn_salir.clicked.connect(events.Eventos.salir)
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
        # Ponemos valor 18 por defecto en la spinBox de edad
        var.ui.sbox_edad.setValue(18)
        # Ponemos el valor minimo de la spinBox
        var.ui.sbox_edad.setMinimum(18)
        # Ponemos el valor maximo de la spinBox
        var.ui.sbox_edad.setMaximum(120)

        for i in var.rbtSex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkPago:
            i.stateChanged.connect(clients.Clientes.selPago)
