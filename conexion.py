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
    def alta_cliente(cliente):
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
            Conexion.mostrar_clientes()
            var.ui.lbl_status.setText('Cliente con dni ' + str(cliente[0]) + ' dado de alta')
        else:
            print("Error: ", query.lastError().text())

    @staticmethod
    def cargar_cliente():
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
    def mostrar_clientes():
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
    def baja_cliente(dni):
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
    def modif_cliente(codigo, newdata):
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
    def buscar_cliente(dni):
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

    # ======================================CONEXIONES PARA LA TABLA DE PRODUCTOS=======================================

    @staticmethod
    def actualizar_tabla_pro():
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, nombre, precio_unidad, stock from articulos')
        if query.exec_():
            while query.next():
                codigo = query.value(0)
                nombre = query.value(1)
                precio = query.value(2)
                stock = query.value(3)
                var.ui.tbl_pro_tabla.setRowCount(index + 1)  # crea la fila y a continuación mete los datos
                var.ui.tbl_pro_tabla.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                var.ui.tbl_pro_tabla.setItem(index, 1, QtWidgets.QTableWidgetItem(nombre))
                var.ui.tbl_pro_tabla.setItem(index, 2, QtWidgets.QTableWidgetItem(str(precio)))
                var.ui.tbl_pro_tabla.setItem(index, 3, QtWidgets.QTableWidgetItem(str(stock)))
                index += 1
        else:
            print("Error al actualizar la tabla de productos: ", query.lastError().text())

    @staticmethod
    def alta_producto(producto: [str, float, int]):
        query = QtSql.QSqlQuery()
        query.prepare('insert into articulos (nombre, precio_unidad, stock)'
                      'VALUES (:nombre, :precio_unidad, :stock)')
        query.bindValue(':nombre', str(producto[0]))
        query.bindValue(':precio_unidad', round(producto[1], 2))
        query.bindValue(':stock', producto[2])
        if query.exec_():
            print("Inserción de Producto Correcta")
            Conexion.actualizar_tabla_pro()
            var.ui.lbl_status.setText('El producto ' + str(producto[0]) + ' ha sido dado de alta')
        else:
            print("Error: ", query.lastError().text())

    @staticmethod
    def baja_producto(codigo):
        query = QtSql.QSqlQuery()
        query.prepare('delete from articulos where codigo = :codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            var.ui.lbl_status.setText('Producto de codigo ' + codigo + ' dado de baja')
        else:
            print("Error dando de baja a un prodcuto: ", query.lastError().text())

    @staticmethod
    def modif_producto(codigo, nuevos_datos):
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare('update articulos set nombre=:nombre, precio_unidad=:precio, stock=:stock '
                      'where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':nombre', nuevos_datos[0])
        query.bindValue(':precio', round(nuevos_datos[1], 2))
        query.bindValue(':stock', nuevos_datos[2])
        if query.exec_():
            print('Producto modificado')
            var.ui.lbl_status.setText('El producto  ' + str(nuevos_datos[0]) + ' ha sido modificado')
        else:
            print("Error modificar producto conexion: ", query.lastError().text())

    @staticmethod
    def buscar_producto(nombre):
        query = QtSql.QSqlQuery()
        query.prepare('select * from articulos where nombre = :nombre')
        query.bindValue(':nombre', nombre)
        if query.exec_():
            while query.next():
                var.ui.tbl_listcli.setRowCount(1)
                var.ui.tbl_listcli.setItem(0, 0, QtWidgets.QTableWidgetItem(query.value(0)))
                var.ui.tbl_listcli.setItem(0, 1, QtWidgets.QTableWidgetItem(nombre))
                var.ui.tbl_listcli.setItem(0, 2, QtWidgets.QTableWidgetItem(query.value(2)))
        else:
            print("Error buscando cliente: ", query.lastError().text())

    # ======================================CONEXIONES PARA LA TABLA DE FACTURAS========================================
    @staticmethod
    def alta_fac(dni, fecha, apel):
        query = QtSql.QSqlQuery()
        query.prepare('insert into facturas (dni, fecha, apellidos) VALUES (:dni, :fecha, :apellidos )')
        query.bindValue(':dni', str(dni))
        query.bindValue(':fecha', str(fecha))
        query.bindValue(':apellidos', str(apel))
        if query.exec_():
            var.ui.lblstatus.setText('Factura Creada')
        else:
            print("Error alta factura: ", query.lastError().text())
        query1 = QtSql.QSqlQuery()
        query1.prepare('select max(codfac) from facturas')
        if query1.exec_():
            while query1.next():
                var.ui.lblNumFac.setText(str(query1.value(0)))
