from PyQt5 import QtWidgets

import events
import var, conexion


class Clientes():

    @staticmethod
    def validarDni(dni):
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
    def resValidarDni():
        '''
        Muestra indicacion sobre el resultado de la validacion del dni
        '''
        try:
            dni = var.ui.edit_dni.text()
            if Clientes.validarDni(dni):
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
    def selSexo():
        try:
            if var.ui.rbt_fem.isChecked():
                var.sex = 'Mujer'
            if var.ui.rbt_mas.isChecked():
                var.sex = 'Hombre'
        except Exception as error:
            print('Error: %s' % str(error))

    @staticmethod
    def selPago():
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
            print(var.pay)
            return var.pay
        except Exception as error:
            print('Error: %s' % str(error))

    @staticmethod
    def selProv(prov):
        try:
            global vpro
            vpro = prov
        except Exception as error:
            print('Error: %s' % str(error))

    '''
    Abrir la ventana calendario
    '''

    @staticmethod
    def abrirCalendar():
        try:
            var.dlgCalendar.show()
        except Exception as error:
            print('Error: %s ' % str(error))

    '''
    Este módulo se ejecuta cuando clickeamos en un día del calendar, es decir, clicked.connect de calendar
    '''

    @staticmethod
    def cargarFecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.edit_fechaalta.setText(str(data))
            var.dlgCalendar.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    @staticmethod
    def altaCliente():
        '''
        Cargara los datos de los clientes en la tabla
        :return:
        '''
        try:
            dni = var.ui.edit_dni.text()
            if Clientes.validarDni(dni):
                newcli = []  # contiene todos los datos
                clitab = []  # será lo que carguemos en la tablas
                client = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre,
                          var.ui.edit_fechaalta, var.ui.edit_dir]
                k = 0
                for i in client:
                    newcli.append(i.text())  # cargamos los valores que hay en los editline
                    if k < 3:
                        clitab.append(i.text())
                        k += 1
                newcli.append(vpro)
                newcli.append(var.sex)
                var.pay2 = Clientes.selPago()
                newcli.append(var.pay2)
                if client:
                    # comprobarmos que no esté vacío lo principal
                    # aquí empieza como trabajar con la TableWidget
                    row = 0
                    column = 0
                    var.ui.tbl_listcli.insertRow(row)
                    for registro in clitab:
                        cell = QtWidgets.QTableWidgetItem(registro)
                        var.ui.tbl_listcli.setItem(row, column, cell)
                        column += 1
                    conexion.Conexion.altaCli(newcli)
                else:
                    print('Faltan Datos')
            else:
                events.Eventos.aviso("El dni no es valido")
        except Exception as error:
            print('Error cargar clientes en Clients: %s ' % str(error))

    @staticmethod
    def limpiarCli():
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
            print('Error limpiar widgets: %s ' % str(error))

    @staticmethod
    def cargarCli():
        '''
        carga en widgets formulario cliente los datos
        elegidos en la tabla
        :return: none
        '''
        try:
            fila = var.ui.tbl_listcli.selectedItems()
            client = [var.ui.edit_dni, var.ui.edit_apel, var.ui.edit_nombre]
            if fila:
                fila = [dato.text() for dato in fila]
            i = 0
            for i, dato in enumerate(client):
                dato.setText(fila[i])
            conexion.Conexion.cargarCliente()
        except Exception as error:
            print('Error cargar clientes: %s ' % str(error))

    @staticmethod
    def bajaCliente():
        '''
        módulos para dar de baja un cliente
        :return:
        '''
        try:
            dni = var.ui.edit_dni.text()
            events.Eventos.confirmar("Esta seguro/a que quiere borrar?")
            if var.confirmacion:
                conexion.Conexion.bajaCli(dni)
                conexion.Conexion.mostrarClientes()
                Clientes.limpiarCli()
        except Exception as error:
            print('Error eliminando clientes: %s ' % str(error))

    @staticmethod
    def modifCliente():
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
            var.pay = Clientes.selPago()
            print(var.pay)
            newdata.append(var.pay)
            newdata.append(var.ui.sbox_edad.value())
            cod = var.ui.lbl_codigo.text()
            conexion.Conexion.modifCli(cod, newdata)
            conexion.Conexion.mostrarClientes()

        except Exception as error:
            print('Error modificar clientes: %s ' % str(error))

    @staticmethod
    def recargar():
        try:
            Clientes.limpiarCli()
            conexion.Conexion.mostrarClientes()
            print('Recargando...')
        except Exception as error:
            print('Error recargargando clientes: %s ' % str(error))

    @staticmethod
    def buscar():
        try:
            dni = var.ui.edit_dni.text()
            if Clientes.validarDni(dni):
                conexion.Conexion.buscarCliente(dni)
            else:
                print('Se ha intentado buscar un DNI no valido')
        except Exception as error:
            print('Error buscando clientes: %s ' % str(error))
