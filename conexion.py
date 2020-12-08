from PyQt5 import QtSql
import var
from venPrincipal import *


class Conexion():

    @staticmethod
    def db_connect(filename):
        '''
        Conexion con la base de datos tipo sqlite.
        :param filename:
        :return:
        '''
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filename)
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos',
                                           'No se puede establecer conexion.\n'
                                           'Haz Click para Cancelar.', QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexión Establecida')
        return True

    @staticmethod
    def altaCli(cliente):
        '''
        Metodo que crea una instruccion de sql que inserta una tupla en la base de datos
        segun los datos regogidos en el array que se le pasa como argumento.
        :param cliente:
        :return:
        '''
        query = QtSql.QSqlQuery()
        query.prepare('insert into clientes (dni, apellidos, nombre, fechalta, direccion, provincia, sexo, '
                      'formaspago, edad) '
                      'VALUES (:dni, :apellidos, :nombre, :fechalta, :direccion, :provincia, :sexo, :formaspago, :edad)')
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
            Conexion.mostrarClientes()
            var.ui.lbl_status.setText('Cliente con dni ' + str(cliente[0]) + ' dado de alta')
        else:
            print("Error: ", query.lastError().text())

    @staticmethod
    def cargarCliente():
        '''
        Este metodo carga un cliente desde la base de datos a traves de una query que usa
        el dni que este escrito en el editBox de DNI de la ventana principal.
        :return:
        '''
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
                for data in var.chkPago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkPago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkPago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkPago[2].setChecked(True)
                var.ui.sbox_edad.setValue(query.value(9))

    @staticmethod
    def mostrarClientes():
        '''
        Metodo que carga el DNI, nombre y apellidos en la tabla de la ventana principal.
        :return:
        '''
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
    def bajaCli(dni):
        ''''
        Metodo para eliminar cliente. Se llama desde fichero clientes.py
        :return None
        '''
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            print('Baja cliente')
            var.ui.lbl_status.setText('Cliente con dni ' + dni + ' dado de baja')
        else:
            print("Error mostrar clientes: ", query.lastError().text())

    @staticmethod
    def modifCli(codigo, newdata):
        ''''
           modulo para modificar cliente. se llama desde fichero clientes.py
           :return None
           '''
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
    def buscarCliente(dni):
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