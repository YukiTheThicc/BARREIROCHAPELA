from PyQt5 import QtSql

import var
import events
from venConfirmacion import *


class DialogEliminarProducto(QtWidgets.QDialog):
    def __init__(self):
        super(DialogEliminarProducto, self).__init__()
        Productos.dlgEliminarProducto = Ui_ven_confirmacion()
        Productos.dlgEliminarProducto.setupUi(self)
        self.pregunta = Productos.dlgEliminarProducto.lbl_pregunta
        Productos.dlgEliminarProducto.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(Productos.baja_producto)
        Productos.dlgEliminarProducto.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.No).clicked.connect(self.close)


class Productos:

    dlgEliminarProducto = None

    @classmethod
    def crear_modulo(cls):
        cls.dlgEliminarProducto = DialogEliminarProducto()

        var.ui.btn_pro_salir.clicked.connect(events.Eventos.salir)
        var.ui.btn_pro_guardar.clicked.connect(Productos.alta_producto)
        var.ui.tbl_pro_tabla.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tbl_pro_tabla.clicked.connect(Productos.sel_producto)
        var.ui.btn_pro_eliminar.clicked.connect(Productos.eliminar_producto)
        var.ui.btn_pro_limpiar.clicked.connect(Productos.limpiar_campos)
        var.ui.btn_pro_modificar.clicked.connect(events.Eventos.modificar_producto)
        var.ui.btn_pro_recargar.clicked.connect(Productos.recargar)

        cls.db_actualizar_tabla_pro()

    @classmethod
    def alta_producto(cls):
        nombre = var.ui.edit_pro_nombre.text()
        precio = var.ui.dspin_pro_precio.value()
        stock = var.ui.spin_pro_stock.value()
        if not nombre == '':
            to_insert = [nombre, precio, stock]
            cls.db_alta_producto(to_insert)
        else:
            events.Eventos.aviso("Necesita un nombre")

    @staticmethod
    def sel_producto():
        try:
            tupla_elegida = var.ui.tbl_pro_tabla.selectedItems()
            campos_producto = {"nombre": var.ui.edit_pro_nombre, "precio": var.ui.dspin_pro_precio,
                               "codigo": var.ui.lbl_pro_muestra_codigo, "stock": var.ui.spin_pro_stock}
            campos_producto["codigo"].setText(tupla_elegida[0].text())
            campos_producto["nombre"].setText(tupla_elegida[1].text())
            campos_producto["precio"].setValue(float(tupla_elegida[2].text()))
            campos_producto["stock"].setValue(int(tupla_elegida[3].text()))
        except Exception as error:
            print('Error en sel_producto: %s ' % str(error))

    @staticmethod
    def limpiar_campos():
        '''
        limpia los datos del formulario cliente
        :return: none
        '''
        try:
            var.ui.edit_pro_nombre.setText('')
            var.ui.lbl_pro_muestra_codigo.setText('')
            var.ui.dspin_pro_precio.setValue(0.01)
            var.ui.edit_pro_stock.setValue(0)
        except Exception as error:
            print('Error en limpiar_producto: %s ' % str(error))

    @classmethod
    def eliminar_producto(cls):
        """
        Funcion para llamar al dialogo de confirmacion y recoger el resultado
        :return:
        """
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            if codigo != '':
                cls.dlgEliminarProducto.show()
                cls.dlgEliminarProducto.pregunta.setText("Esta seguro/a que quiere borrar\n"
                                                         "este producto?")
            else:
                events.Eventos.aviso("Seleccione un producto")
        except Exception as error:
            print('Error: %s' % str(error))

    @classmethod
    def baja_producto(cls):
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            cls.db_baja_producto(codigo)
            cls.db_actualizar_tabla_pro()
            Productos.limpiar_campos()
        except Exception as error:
            print('Error en baja_producto: %s ' % str(error))

    @classmethod
    def modif_producto(cls):
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            newdata = [var.ui.edit_pro_nombre.text(), var.ui.dspin_pro_precio.value(), var.ui.spin_pro_stock.value()]
            cls.db_modif_producto(codigo, newdata)
            cls.db_actualizar_tabla_pro()
        except Exception as error:
            print('Error en modif_producto productos: %s ' % str(error))

    @classmethod
    def recargar(cls):
        try:
            Productos.limpiar_campos()
            cls.db_actualizar_tabla_pro()
            print('Recargando...')
        except Exception as error:
            print('Error en recargar_producto: %s ' % str(error))

    @classmethod
    def buscar(cls):
        try:
            nombre = var.ui.lbl_pro_nombre.text()
            if nombre != '':
                cls.db_buscar_producto(nombre)
            else:
                print('Se ha intentado buscar por un nombre vacio')
        except Exception as error:
            print('Error en buscar_producto: %s ' % str(error))

    @staticmethod
    def db_actualizar_tabla_pro():
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

    @classmethod
    def db_alta_producto(cls, producto: [str, float, int]):
        query = QtSql.QSqlQuery()
        query.prepare('insert into articulos (nombre, precio_unidad, stock)'
                      'VALUES (:nombre, :precio_unidad, :stock)')
        query.bindValue(':nombre', str(producto[0]))
        query.bindValue(':precio_unidad', round(producto[1], 2))
        query.bindValue(':stock', producto[2])
        if query.exec_():
            print("Inserción de Producto Correcta")
            cls.db_actualizar_tabla_pro()
            var.ui.lbl_status.setText('El producto ' + str(producto[0]) + ' ha sido dado de alta')
        else:
            print("Error: ", query.lastError().text())

    @staticmethod
    def db_baja_producto(codigo):
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
    def db_modif_producto(codigo, nuevos_datos):
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
    def db_buscar_producto(nombre):
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