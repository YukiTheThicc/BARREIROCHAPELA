from datetime import datetime

from venCalendar import *
from venConfirmacion import *

import conexion
import events
import var


class DialogEliminarCliente(QtWidgets.QDialog):
    def __init__(self):
        super(DialogEliminarCliente, self).__init__()
        var.dlgEliminarCliente = Ui_ven_confirmacion()
        var.dlgEliminarCliente.setupUi(self)
        self.pregunta = var.dlgEliminarCliente.lbl_pregunta
        var.dlgEliminarCliente.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(Clientes.baja_cliente)
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
        var.dlgCalendar.calendar.clicked.connect(Clientes.cargar_fecha)

class Clientes():

    @staticmethod
    def crear_modulo():
        var.dlgCalendar = DialogCalendar()
        var.dlgEliminarCliente = DialogEliminarCliente()

        # Conexion de los elementos que crean el dialogo para salir del programa
        var.ui.btn_salir.clicked.connect(events.Eventos.salir)
        # Conecta el edit de DNI con la funcion que valida si es correcto o no
        var.ui.edit_dni.editingFinished.connect(lambda: Clientes.show_validar_dni())
        # Conecta clicar el calendar con la funcion que abre la venCalendar
        var.ui.btn_calendar.clicked.connect(Clientes.abrir_calendar)
        # Conecta clicar el boton de guardar con la funcion que guarda el cliente en la
        # base de datos y lo carga en la tabla de la Interfaz
        var.ui.btn_guardar.clicked.connect(Clientes.alta_cliente)
        # Conecta clicar el boton de limpiar con la funcion que limpia los campos de la
        # Interfaz
        var.ui.btn_limpiar.clicked.connect(Clientes.limpiar_cliente)
        # Conecta clicar el boton de eliminar con la funcion que elimina un cliente de la
        # base de datos
        var.ui.btn_eliminar.clicked.connect(events.Eventos.eliminar)
        # Conecta clicar el boton de modificar con la funcion que modifica el cliente con
        # el DNI en el editBox del DNI
        var.ui.btn_modificar.clicked.connect(Clientes.modif_cliente)
        # Conecta la apertura de la combo con la funcion que lee lo que seleccione el usuario
        var.ui.cmb_prov.activated[str].connect(Clientes.sel_pov)
        # Conecta clicar un cliente de la lista de clientes con la funcion que carga sus
        # datos en los campos de la Interfaz
        var.ui.tbl_listcli.clicked.connect(Clientes.cargar_cliente)
        # Conecta que el evento clicar en la tabla conecte con una funcion que seleciona la
        # tupla entera
        var.ui.tbl_listcli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        # Carga la comboBox de provincias en blanco
        events.Eventos.cargar_prov()
        # Conecta clicar en el boton de racargar con la funcion que recarga todos los clientes en la tabla
        var.ui.btn_recargar.clicked.connect(Clientes.recargar)
        # Conecta clicar en el boton de buscar con la funcion que busca un cliente segun su dni
        var.ui.btn_buscar.clicked.connect(Clientes.buscar)
        var.ui.statusbar.addPermanentWidget(var.ui.lbl_status, 1)
        var.ui.lbl_status.setText('Buenos Días')
        # Ponemos valor 18 por defecto en la spinBox de edad
        var.ui.sbox_edad.setValue(18)
        # Ponemos el valor minimo de la spinBox
        var.ui.sbox_edad.setMinimum(18)
        # Ponemos el valor maximo de la spinBox
        var.ui.sbox_edad.setMaximum(120)

        # Arrays con los botones chk y rbt
        var.rbtSex = (var.ui.rbt_fem, var.ui.rbt_mas)
        var.chkPago = (var.ui.chk_efect, var.ui.chk_tarje, var.ui.chk_trans)
        for i in var.rbtSex:
            i.toggled.connect(Clientes.sel_sexo)
        for i in var.chkPago:
            i.stateChanged.connect(Clientes.sel_pago)

    @staticmethod
    def validar_dni(dni):
        '''
        Codigo que valida el dni
        :return:
        '''
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
        '''
        Muestra indicacion sobre el resultado de la validacion del dni
        '''
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

    @staticmethod
    def sel_sexo():
        try:
            if var.ui.rbt_fem.isChecked():
                var.sex = 'Mujer'
            if var.ui.rbt_mas.isChecked():
                var.sex = 'Hombre'
        except Exception as error:
            print('Error en sel_sexo: %s' % str(error))

    @staticmethod
    def sel_pago():
        try:
            var.pay = []
            for i, data in enumerate(var.ui.grp_chk_pago.buttons()):
                # Coge el grupo de chk_box
                if data.isChecked() and i == 0:
                    var.pay.append('Efectivo')
                if data.isChecked() and i == 1:
                    var.pay.append('Tarjeta')
                if data.isChecked() and i == 2:
                    var.pay.append('Transferencia')
            return var.pay
        except Exception as error:
            print('Error en sel_pago: %s' % str(error))

    @staticmethod
    def sel_pov(prov):
        try:
            global vpro
            vpro = prov
        except Exception as error:
            print('Error en sel_pov: %s' % str(error))

    '''
    Abrir la ventana calendario
    '''

    @staticmethod
    def abrir_calendar():
        try:
            var.dlgCalendar.show()
        except Exception as error:
            print('Error en abrir_calendar: %s ' % str(error))

    '''
    Este módulo se ejecuta cuando clickeamos en un día del calendar, es decir, clicked.connect de calendar
    '''

    @staticmethod
    def cargar_fecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.edit_fechaalta.setText(str(data))
            var.dlgCalendar.hide()
        except Exception as error:
            print('Error en cargar_fecha: %s ' % str(error))

    @staticmethod
    def alta_cliente():
        '''
        Cargara los datos de los clientes en la tabla
        :return:
        '''
        try:
            dni = var.ui.edit_dni.text()
            if Clientes.validar_dni(dni):
                new_client_data = []  # contiene todos los datos
                edit_text_fields = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre,
                          var.ui.edit_fechaalta, var.ui.edit_dir]
                for i in edit_text_fields:
                    new_client_data.append(i.text())  # cargamos los valores que hay en los campos
                new_client_data.append(vpro)
                new_client_data.append(var.sex)
                new_client_data.append(Clientes.sel_pago())
                new_client_data.append(var.ui.sbox_edad.value())
                if len(new_client_data) == 9:
                    conexion.Conexion.alta_cliente(new_client_data)
                else:
                    print('El numero de datos a insertar no cuadra')

            else:
                events.Eventos.aviso("El dni no es valido")
        except Exception as error:
            print('Error en alta_cliente: %s ' % str(error))

    @staticmethod
    def limpiar_cliente():
        '''
        limpia los datos del formulario cliente
        :return: none
        '''
        try:
            client = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre,
                      var.ui.edit_fechaalta, var.ui.edit_dir]
            for i in range(len(client)):
                client[i].setText('')
            var.ui.grp_chk_pago.setExclusive(False)  # necesario para los radiobutton
            for dato in var.rbtSex:
                dato.setChecked(False)
            for data in var.chkPago:
                data.setChecked(False)
            var.ui.cmb_prov.setCurrentIndex(0)
            var.ui.lbl_validar.setText('')
            var.ui.lbl_codigo.setText('')
            var.ui.sbox_edad.setValue(18)
        except Exception as error:
            print('Error en limpiarCliente: %s ' % str(error))

    @staticmethod
    def cargar_cliente():
        '''
        Carga los datos de un elemento en la tabla en los campos de datos
        :return: none
        '''
        try:
            tupla_elegida = var.ui.tbl_listcli.selectedItems()
            campos_cliente = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre]
            var.dni = campos_cliente[0].text()
            if tupla_elegida:
                tupla_elegida = [dato.text() for dato in tupla_elegida]
            i = 0
            for i, dato in enumerate(campos_cliente):
                dato.setText(tupla_elegida[i])
            conexion.Conexion.cargar_cliente()
        except Exception as error:
            print('Error en cargar_cliente: %s ' % str(error))

    @staticmethod
    def baja_cliente():
        '''
        módulos para dar de baja un cliente
        :return:
        '''
        try:
            dni = var.ui.edit_dni.text()
            conexion.Conexion.baja_cliente(dni)
            conexion.Conexion.mostrar_clientes()
            Clientes.limpiar_cliente()
        except Exception as error:
            print('Error en baja_cliente: %s ' % str(error))

    @staticmethod
    def modif_cliente():
        """
        módulos para dar de modificar datos de un cliente
        :return:
        """
        try:
            newdata = []
            client = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre,
                      var.ui.edit_fechaalta, var.ui.edit_dir]
            for i in client:
                newdata.append(i.text())  # cargamos los valores que hay en los editline
            newdata.append(var.ui.cmb_prov.currentText())
            newdata.append(var.sex)
            var.pay = Clientes.sel_pago()
            newdata.append(var.pay)
            newdata.append(var.ui.sbox_edad.value())
            cod = var.ui.lbl_codigo.text()
            conexion.Conexion.modif_cliente(cod, newdata)
            conexion.Conexion.mostrar_clientes()
        except Exception as error:
            print('Error en modif_cliente: %s ' % str(error))

    @staticmethod
    def recargar():
        try:
            Clientes.limpiar_cliente()
            conexion.Conexion.mostrar_clientes()
            print('Recargando...')
        except Exception as error:
            print('Error en recargar: %s ' % str(error))

    @staticmethod
    def buscar():
        try:
            dni = var.ui.edit_dni.text()
            if Clientes.validar_dni(dni):
                conexion.Conexion.buscar_cliente(dni)
            else:
                print('Se ha intentado buscar un DNI no valido')
        except Exception as error:
            print('Error en buscar: %s ' % str(error))


