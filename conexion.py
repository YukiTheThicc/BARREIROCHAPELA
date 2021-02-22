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
        """

        :param codigo:
        :type codigo:
        :return:
        :rtype:
        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from articulos where codigo = :codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            var.ui.lbl_status.setText('Producto de codigo ' + codigo + ' dado de baja')
        else:
            print("Error dando de baja a un prodcuto: ", query.lastError().text())

    @staticmethod
    def modif_producto(codigo, nuevos_datos):
        """

        :param codigo:
        :param nuevos_datos:
        :return:
        """
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
        """

        :param nombre:
        :return:
        """
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
