from datetime import datetime

from PyQt5 import QtSql

from venCalendar import *
from venConfirmacion import *

import events
import var


class DialogEliminarCliente(QtWidgets.QDialog):
    """

    Clase de la ventana de diálogo que saltará al intentar eliminar un cliente.

    """

    def __init__(self):
        super(DialogEliminarCliente, self).__init__()
        Clientes.dlgEliminarCliente = Ui_ven_confirmacion()
        Clientes.dlgEliminarCliente.setupUi(self)
        self.pregunta = Clientes.dlgEliminarCliente.lbl_pregunta
        Clientes.dlgEliminarCliente.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            Clientes.baja_cliente)
        Clientes.dlgEliminarCliente.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.No).clicked.connect(self.close)


class DialogCalendar(QtWidgets.QDialog):
    """

    Clase que define la ventana de diálogo del calendario que se abrirá al pulsar el botón del calendario.

    """

    def __init__(self):
        super(DialogCalendar, self).__init__()
        Clientes.dlgCalendar = ui_ven_calendar()
        Clientes.dlgCalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        Clientes.dlgCalendar.calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        Clientes.dlgCalendar.calendar.clicked.connect(Clientes.cargar_fecha)


def eliminar():
    """

    Funcion para llamar al dialogo de confirmacion para eliminar a un cliente.

    :return:

    """
    try:
        Clientes.dlgEliminarCliente.show()
        Clientes.dlgEliminarCliente.pregunta.setText("Esta seguro/a que quiere borrar?")
    except Exception as error:
        print('Error en eliminar: %s' % str(error))


class Clientes:
    """

    Módulo de clientes: se implementan aquí todas las funciones necesarias para un módulo de clientes funcional.

    """
    dlgCalendar = None
    dlgEliminarCliente = None
    chkPago = None
    rbtSex = None
    sex = None
    vpro = None
    pay = []
    pay2 = []

    @classmethod
    def crear_modulo(cls):
        """

        Metodo que prepara y crea el modulo de clientes.

        :return: None

        Se crean las ventanas de diálogo propias del módulo de clientes y las variables de clase de los radiobuttons y
        los checkboxes. Luego procede a crear todas las conexiones para los eventos de los widgets de la ventana
        principal con los métodos apropiados.
        clase


        """
        Clientes.dlgCalendar = DialogCalendar()
        Clientes.dlgEliminarCliente = DialogEliminarCliente()

        var.ui.btn_salir.clicked.connect(events.salir)
        var.ui.edit_dni.editingFinished.connect(lambda: Clientes.show_validar_dni())
        var.ui.btn_calendar.clicked.connect(Clientes.abrir_calendar)
        var.ui.btn_guardar.clicked.connect(Clientes.alta_cliente)
        var.ui.btn_limpiar.clicked.connect(Clientes.limpiar_cliente)
        var.ui.btn_eliminar.clicked.connect(eliminar)
        var.ui.btn_modificar.clicked.connect(Clientes.modif_cliente)
        var.ui.tbl_listcli.clicked.connect(Clientes.cargar_cliente)
        var.ui.tbl_listcli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.btn_recargar.clicked.connect(Clientes.recargar)
        var.ui.btn_buscar.clicked.connect(Clientes.buscar)

        cls.cargar_prov()
        var.ui.sbox_edad.setValue(18)
        var.ui.sbox_edad.setMinimum(18)
        var.ui.sbox_edad.setMaximum(120)

        cls.rbtSex = (var.ui.rbt_fem, var.ui.rbt_mas)
        cls.chkPago = (var.ui.chk_efect, var.ui.chk_tarje, var.ui.chk_trans)
        for i in cls.rbtSex:
            i.toggled.connect(Clientes.sel_sexo)
        for i in cls.chkPago:
            i.stateChanged.connect(Clientes.sel_pago)

        cls.db_mostrar_clientes()

    @staticmethod
    def cargar_prov():
        """

        Carga la combobox de provincias con los valores requeridos

        :return: None

        """
        try:
            prov = ['', 'Pontevedra', 'A Coruña', 'Lugo', 'Ourense']
            for i in prov:
                var.ui.cmb_prov.addItem(i)
        except Exception as error:
            print('Error en cargar_prov: %s' % str(error))

    @staticmethod
    def validar_dni(dni):
        """

        Valida un DNI que se le pasa por parámetro.

        :param dni: str
        :return: bool, True si válido, False si no válido

        Comprueba que la logitud es correcta, que el últimop carácter es una letra y que esta se corresponde con la
        letra que le debería tocar a esa secuencia de números.

        """
        try:
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'
            dig_ext = 'XYZ'
            reemp_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = '0123456789'
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.remplace(dni[0], reemp_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control
        except Exception as error:
            print('Error en validar_dni: ', str(error))
            return None

    @staticmethod
    def show_validar_dni():
        """

        Muestra de forma visual los resultados de la validación de DNI.

        :return: bool, True si válido, False si no válido o None si se lanza excepción

        Muestra una V verde o una X roja al lado de la etiqueta de DNI además de poner el texto en la edit box en mayús-
        culas.

        """
        try:
            dni = var.ui.edit_dni.text()
            if Clientes.validar_dni(dni):
                var.ui.lbl_validar.setStyleSheet('QLabel {color: green;}')
                var.ui.lbl_validar.setText('V')
                var.ui.edit_dni.setText(dni.upper())
                return True
            else:
                var.ui.lbl_validar.setStyleSheet('QLabel {color: red;}')
                var.ui.lbl_validar.setText('X')
                var.ui.edit_dni.setText(dni.upper())
                return False
        except Exception as error:
            print('Error en show_validar_dni: ', str(error))
            return None

    @classmethod
    def sel_sexo(cls):
        """

        Pone la variable de clase 'sex' a hombre o mujer según el radioButton que esté checkeado.

        :return: None

        """
        try:
            if var.ui.rbt_fem.isChecked():
                cls.sex = 'Mujer'
            if var.ui.rbt_mas.isChecked():
                cls.sex = 'Hombre'
        except Exception as error:
            print('Error en sel_sexo: %s' % str(error))

    @classmethod
    def sel_pago(cls):
        """

        Añade a la variable de clase de métodos de pago los que estén checkeados en el momento de su ejecucción.

        :return: None

        """
        try:
            cls.pay = []
            for i, data in enumerate(var.ui.grp_chk_pago.buttons()):
                if data.isChecked() and i == 0:
                    cls.pay.append('Efectivo')
                if data.isChecked() and i == 1:
                    cls.pay.append('Tarjeta')
                if data.isChecked() and i == 2:
                    cls.pay.append('Transferencia')
        except Exception as error:
            print('Error en sel_pago: %s' % str(error))

    @staticmethod
    def abrir_calendar():
        """

        Abre la ventana de diálogo del calendario

        :return: None

        """
        try:
            Clientes.dlgCalendar.show()
        except Exception as error:
            print('Error en abrir_calendar: %s ' % str(error))

    @staticmethod
    def cargar_fecha(q_date):
        """

        Transforma la fecha de QT pasada por parámetro a un str y lo pone en la editbox de la fecha.

        :param q_date:
        :return: None

        """
        try:
            data = ('{0}/{1}/{2}'.format(q_date.day(), q_date.month(), q_date.year()))
            var.ui.edit_fechaalta.setText(str(data))
            Clientes.dlgCalendar.hide()
        except Exception as error:
            print('Error en cargar_fecha: %s ' % str(error))

    @classmethod
    def alta_cliente(cls):
        """

        Valida si el DNI es valido y si lo es, añade a una lista de datos los datos para un nuevo cliente y llama a la
        función que inserta el cliente en la base de datos.

        :return: None

        """
        try:
            dni = var.ui.edit_dni.text()
            if Clientes.validar_dni(dni):
                new_client_data = []  # contiene todos los datos
                edit_text_fields = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre,
                                    var.ui.edit_fechaalta, var.ui.edit_dir]
                for i in edit_text_fields:
                    new_client_data.append(i.text())  # cargamos los valores que hay en los campos
                new_client_data.append(cls.vpro)
                new_client_data.append(cls.sex)
                new_client_data.append(Clientes.sel_pago())
                new_client_data.append(var.ui.sbox_edad.value())
                if len(new_client_data) == 9:
                    Clientes.db_alta_cliente(new_client_data)
                else:
                    print('El numero de datos a insertar no cuadra')
            else:
                events.aviso("El dni no es valido")
        except Exception as error:
            print('Error en alta_cliente: %s ' % str(error))

    @classmethod
    def limpiar_cliente(cls):
        """

        Limpia los campos de la ui de clientes.

        :return: None

        """
        try:
            client = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre,
                      var.ui.edit_fechaalta, var.ui.edit_dir]
            for i in range(len(client)):
                client[i].setText('')
            var.ui.grp_chk_pago.setExclusive(False)
            for dato in cls.rbtSex:
                dato.setChecked(False)
            for data in cls.chkPago:
                data.setChecked(False)
            var.ui.cmb_prov.setCurrentIndex(0)
            var.ui.lbl_validar.setText('')
            var.ui.lbl_codigo.setText('')
            var.ui.sbox_edad.setValue(18)
        except Exception as error:
            print('Error en limpiarCliente: %s ' % str(error))

    @staticmethod
    def cargar_cliente():
        """

        Selecciona los datos de la tabla de clientes y los pone en los campos de datos de la interfaz. LLama a la
        función de db_cargar_cliente para recoger el resto de los datos del cliente.

        :return: None

        """
        try:
            tupla_elegida = var.ui.tbl_listcli.selectedItems()
            campos_cliente = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre]
            if tupla_elegida:
                tupla_elegida = [dato.text() for dato in tupla_elegida]
            for i, dato in enumerate(campos_cliente):
                dato.setText(tupla_elegida[i])
                if i == 0:
                    var.ui.edit_fac_dni.setText(tupla_elegida[0])
                if i == 1:
                    var.ui.edit_fac_nombre.setText(tupla_elegida[1])
            Clientes.db_cargar_cliente()
        except Exception as error:
            print('Error en cargar_cliente: %s ' % str(error))

    @staticmethod
    def baja_cliente():
        """

        Recoge el DNI del editbox de clientes y elimina el cliente con ese DNI.

        :return: None

        """
        try:
            dni = var.ui.edit_dni.text()
            Clientes.db_baja_cliente(dni)
            Clientes.db_mostrar_clientes()
            Clientes.limpiar_cliente()
        except Exception as error:
            print('Error en baja_cliente: %s ' % str(error))

    @classmethod
    def modif_cliente(cls):
        """

        Modifica los datos de un cliente ya existente.

        :return: None

        Recoge de los campos de la interfaz de cliente, los recoge en una lista y los envía a la función que los
        actualiza en la base de datos.

        """
        try:
            newdata = []
            client = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre,
                      var.ui.edit_fechaalta, var.ui.edit_dir]
            for i in client:
                newdata.append(i.text())
            newdata.append(var.ui.cmb_prov.currentText())
            newdata.append(cls.sex)
            Clientes.sel_pago()
            newdata.append(cls.pay)
            newdata.append(var.ui.sbox_edad.value())
            cod = var.ui.lbl_codigo.text()
            Clientes.db_modif_cliente(cod, newdata)
            Clientes.db_mostrar_clientes()
        except Exception as error:
            print('Error en modif_cliente: %s ' % str(error))

    @staticmethod
    def recargar():
        """

        Recarga lista de clientes.

        :return: None

        """
        try:
            Clientes.limpiar_cliente()
            Clientes.db_mostrar_clientes()
            print('Recargando...')
        except Exception as error:
            print('Error en recargar: %s ' % str(error))

    @staticmethod
    def buscar():
        """

        Busca un cliente según su DNI llamando a la función que lo busca en la base de datos.

        :return: None

        """
        try:
            dni = var.ui.edit_dni.text()
            if Clientes.validar_dni(dni):
                Clientes.db_buscar_cliente(dni)
            else:
                var.ui.lbl_status.setText('Se ha intentado buscar un DNI no valido')
        except Exception as error:
            print('Error en buscar: %s ' % str(error))

    @staticmethod
    def db_alta_cliente(cliente):
        """

        Inserta en la base de datos un cliente con la lista de datos que se le pasan como parámetros.

        :param cliente: lista de datos del cliente
        :return: None

        """
        query = QtSql.QSqlQuery()
        query.prepare('insert into clientes (dni, apellidos, nombre, fechalta, direccion, provincia, sexo, '
                      'formaspago, edad) '
                      'VALUES (:dni, :apellidos, :nombre, :fechalta, :direccion, :provincia, :sexo, :formaspago, '
                      ':edad)')
        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':fechalta', str(cliente[3]))
        query.bindValue(':direccion', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        query.bindValue(':formaspago', str(cliente[7]))
        query.bindValue(':edad', str(cliente[8]))
        if query.exec_():
            Clientes.db_mostrar_clientes()
            var.ui.lbl_status.setText('Cliente con dni ' + str(cliente[0]) + ' dado de alta')
        else:
            print("Error en db_alta_cliente: ", query.lastError().text())

    @staticmethod
    def db_cargar_cliente():
        """

        Carga de la base de datos los campos restantes que no se muestran en la tabla de clientes y los pone en la
        interfaz de clientes.

        :return: None

        """
        dni = var.ui.edit_dni.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lbl_codigo.setText(str(query.value(0)))
                var.ui.edit_fechaalta.setText(query.value(4))
                var.ui.edit_dir.setText(query.value(5))
                var.ui.cmb_prov.setCurrentText(str(query.value(6)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbt_fem.setChecked(True)
                    var.ui.rbt_mas.setChecked(False)
                else:
                    var.ui.rbt_mas.setChecked(True)
                    var.ui.rbt_fem.setChecked(False)
                for data in Clientes.chkPago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    Clientes.chkPago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    Clientes.chkPago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    Clientes.chkPago[2].setChecked(True)
                var.ui.sbox_edad.setValue(query.value(9))

    @staticmethod
    def db_mostrar_clientes():
        """

        Imprime en la tabla de clientes el DNI, nombre y apellidos de todos los clientes en la base de datos.

        :return: None

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos, nombre from clientes')
        if query.exec_():
            while query.next():
                dni = query.value(0)
                apellidos = query.value(1)
                nombre = query.value(2)
                var.ui.tbl_listcli.setRowCount(index + 1)
                var.ui.tbl_listcli.setItem(index, 0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tbl_listcli.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tbl_listcli.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                index += 1
        else:
            print("Error en db_mostrar_clientes: ", query.lastError().text())

    @staticmethod
    def db_baja_cliente(dni):
        """

        Elimina una tupla de cliente en la base de datos segíun su DNI.

        :param dni: str, el dni
        :return: None

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            var.ui.lbl_status.setText('Cliente con dni ' + dni + ' dado de baja')
        else:
            print("Error en db_baja_cliente: ", query.lastError().text())

    @staticmethod
    def db_modif_cliente(codigo, newdata):
        """

        Según el código que se le pasa por parámetro, actualiza el cliente con los nuevos datos que se le pasan como
        parámetro.

        :param codigo: int, código del cliente.
        :param newdata: lista, datos del cliente.
        :return: None

        """
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare('update clientes set dni=:dni, apellidos=:apellidos, nombre=:nombre, fechalta=:fechalta, '
                      'direccion=:direccion, provincia=:provincia, sexo=:sexo, formaspago=:formaspago, edad=:edad '
                      'where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':dni', str(newdata[0]))
        query.bindValue(':apellidos', str(newdata[1]))
        query.bindValue(':nombre', str(newdata[2]))
        query.bindValue(':fechalta', str(newdata[3]))
        query.bindValue(':direccion', str(newdata[4]))
        query.bindValue(':provincia', str(newdata[5]))
        query.bindValue(':sexo', str(newdata[6]))
        query.bindValue(':formaspago', str(newdata[7]))
        query.bindValue(':edad', str(newdata[8]))
        if query.exec_():
            var.ui.lbl_status.setText('Cliente con dni ' + str(newdata[0]) + ' modificado')
        else:
            print("Error en db_modif_cliente: ", query.lastError().text())

    @staticmethod
    def db_buscar_cliente(dni):
        """

        Busca el cliente con el DNI y lo pone solo en la tabla de clientes.

        :param dni: str, dni
        :return: None

        """
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.tbl_listcli.setRowCount(1)
                var.ui.tbl_listcli.setItem(0, 0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tbl_listcli.setItem(0, 1, QtWidgets.QTableWidgetItem(query.value(2)))
                var.ui.tbl_listcli.setItem(0, 2, QtWidgets.QTableWidgetItem(query.value(3)))
        else:
            print("Error buscando cliente: ", query.lastError().text())
