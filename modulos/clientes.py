from datetime import datetime

from PyQt5 import QtSql

from venCalendar import *
from venConfirmacion import *

import events
import var


class DialogEliminarCliente(QtWidgets.QDialog):
    """

    Clase de la ventana de diálogo que saltará al intentar eliminar un cliente

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


class Clientes:
    """

    Módulo de clientes: se implementan aquí todas las funciones necesarias para un módulo de clientes funcional.

    :var Clientes.dlgCalendar: Guarda la ventana de diálogo del calendario que se abre al pulsar el botón de fecha.


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

        Metodo que prepara y crea el modulo de clientes

        :return: None
        :rtype: None

        Se crean las ventanas de diálogo propias del módulo de clientes y las variables de clase de los radiobuttons y
        los checkboxes. Luego procede a crear todas las conexiones para los eventos de los widgets de la ventana
        principal con los métodos apropiados.
        clase


        """
        Clientes.dlgCalendar = DialogCalendar()
        Clientes.dlgEliminarCliente = DialogEliminarCliente()

        var.ui.btn_salir.clicked.connect(events.Eventos.salir)
        var.ui.edit_dni.editingFinished.connect(lambda: Clientes.show_validar_dni())
        var.ui.btn_calendar.clicked.connect(Clientes.abrir_calendar)
        var.ui.btn_guardar.clicked.connect(Clientes.alta_cliente)
        var.ui.btn_limpiar.clicked.connect(Clientes.limpiar_cliente)
        var.ui.btn_eliminar.clicked.connect(events.Eventos.eliminar)
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
        '''
        Carga las provincias al iniciar el programa
        :return:
        '''
        try:
            prov = ['', 'Pontevedra', 'A Coruña', 'Lugo', 'Ourense']
            for i in prov:
                var.ui.cmb_prov.addItem(i)
        except Exception as error:
            print('Error %s' % str(error))

    @staticmethod
    def validar_dni(dni):

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
        except:
            print('Error modulo validar DNI')
            return None

    @staticmethod
    def show_validar_dni():

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
        except:
            print('Error modulo valido DNI')
            return None

    @classmethod
    def sel_sexo(cls):
        try:
            if var.ui.rbt_fem.isChecked():
                cls.sex = 'Mujer'
            if var.ui.rbt_mas.isChecked():
                cls.sex = 'Hombre'
        except Exception as error:
            print('Error en sel_sexo: %s' % str(error))

    @classmethod
    def sel_pago(cls):
        try:
            cls.pay = []
            for i, data in enumerate(var.ui.grp_chk_pago.buttons()):
                if data.isChecked() and i == 0:
                    cls.pay.append('Efectivo')
                if data.isChecked() and i == 1:
                    cls.pay.append('Tarjeta')
                if data.isChecked() and i == 2:
                    cls.pay.append('Transferencia')
            return cls.pay
        except Exception as error:
            print('Error en sel_pago: %s' % str(error))

    @staticmethod
    def abrir_calendar():
        try:
            Clientes.dlgCalendar.show()
        except Exception as error:
            print('Error en abrir_calendar: %s ' % str(error))

    @staticmethod
    def cargar_fecha(q_date):
        try:
            data = ('{0}/{1}/{2}'.format(q_date.day(), q_date.month(), q_date.year()))
            var.ui.edit_fechaalta.setText(str(data))
            Clientes.dlgCalendar.hide()
        except Exception as error:
            print('Error en cargar_fecha: %s ' % str(error))

    @classmethod
    def alta_cliente(cls):
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
                events.Eventos.aviso("El dni no es valido")
        except Exception as error:
            print('Error en db_alta_cliente: %s ' % str(error))

    @classmethod
    def limpiar_cliente(cls):

        try:
            client = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre,
                      var.ui.edit_fechaalta, var.ui.edit_dir]
            for i in range(len(client)):
                client[i].setText('')
            var.ui.grp_chk_pago.setExclusive(False)  # necesario para los radiobutton
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
            print('Error en db_cargar_cliente: %s ' % str(error))

    @staticmethod
    def baja_cliente():

        try:
            dni = var.ui.edit_dni.text()
            Clientes.db_baja_cliente(dni)
            Clientes.db_mostrar_clientes()
            Clientes.limpiar_cliente()
        except Exception as error:
            print('Error en db_baja_cliente: %s ' % str(error))

    @classmethod
    def modif_cliente(cls):

        try:
            newdata = []
            client = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre,
                      var.ui.edit_fechaalta, var.ui.edit_dir]
            for i in client:
                newdata.append(i.text())  # cargamos los valores que hay en los editline
            newdata.append(var.ui.cmb_prov.currentText())
            newdata.append(cls.sex)
            var.pay = Clientes.sel_pago()
            newdata.append(cls.pay)
            newdata.append(var.ui.sbox_edad.value())
            cod = var.ui.lbl_codigo.text()
            Clientes.db_modif_cliente(cod, newdata)
            Clientes.db_mostrar_clientes()
        except Exception as error:
            print('Error en db_modif_cliente: %s ' % str(error))

    @staticmethod
    def recargar():
        try:
            Clientes.limpiar_cliente()
            Clientes.db_mostrar_clientes()
            print('Recargando...')
        except Exception as error:
            print('Error en recargar: %s ' % str(error))

    @staticmethod
    def buscar():
        try:
            dni = var.ui.edit_dni.text()
            if Clientes.validar_dni(dni):
                Clientes.db_buscar_cliente(dni)
            else:
                print('Se ha intentado buscar un DNI no valido')
        except Exception as error:
            print('Error en buscar: %s ' % str(error))

    @staticmethod
    def db_alta_cliente(cliente):

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
            print("Inserción Correcta")
            Clientes.db_mostrar_clientes()
            var.ui.lbl_status.setText('Cliente con dni ' + str(cliente[0]) + ' dado de alta')
        else:
            print("Error: ", query.lastError().text())

    @staticmethod
    def db_cargar_cliente():

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

        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos, nombre from clientes')
        if query.exec_():
            while query.next():
                dni = query.value(0)
                apellidos = query.value(1)
                nombre = query.value(2)
                var.ui.tbl_listcli.setRowCount(index + 1)  # crea la fila y a continuación mete los datos
                var.ui.tbl_listcli.setItem(index, 0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tbl_listcli.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tbl_listcli.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                index += 1
        else:
            print("Error mostrar clientes: ", query.lastError().text())

    @staticmethod
    def db_baja_cliente(dni):

        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            print('Baja cliente')
            var.ui.lbl_status.setText('Cliente con dni ' + dni + ' dado de baja')
        else:
            print("Error mostrar clientes: ", query.lastError().text())

    @staticmethod
    def db_modif_cliente(codigo, newdata):

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
            print('Cliente modificado')
            var.ui.lbl_status.setText('Cliente con dni ' + str(newdata[0]) + ' modificado')
        else:
            print("Error modificar cliente: ", query.lastError().text())

    @staticmethod
    def db_buscar_cliente(dni):
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
