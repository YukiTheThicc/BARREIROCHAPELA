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
        Productos.dlgEliminarProducto.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            Productos.baja_producto)
        Productos.dlgEliminarProducto.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.No).clicked.connect(self.close)


class Productos:
    dlgEliminarProducto = None

    @classmethod
    def crear_modulo(cls):
        cls.dlgEliminarProducto = DialogEliminarProducto()

        var.ui.btn_pro_salir.clicked.connect(events.salir)
        var.ui.btn_pro_guardar.clicked.connect(cls.alta_producto)
        var.ui.tbl_pro_tabla.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tbl_pro_tabla.clicked.connect(cls.sel_producto)
        var.ui.btn_pro_eliminar.clicked.connect(cls.eliminar_producto)
        var.ui.btn_pro_limpiar.clicked.connect(cls.limpiar_campos)
        var.ui.btn_pro_modificar.clicked.connect(cls.modificar_producto)
        var.ui.btn_pro_recargar.clicked.connect(cls.recargar)

        cls.db_actualizar_tabla_pro()

    @classmethod
    def alta_producto(cls):
        """

        Recoge los datos de un productod e la interfaz.

        :return: None

        """
        nombre = var.ui.edit_pro_nombre.text()
        precio = var.ui.dspin_pro_precio.value()
        stock = var.ui.spin_pro_stock.value()
        if not nombre == '':
            to_insert = [nombre, precio, stock]
            cls.db_alta_producto(to_insert)
        else:
            events.aviso("Necesita un nombre")

    @staticmethod
    def sel_producto():
        """

        Pone los datos del producto seleccionado en la tabla en los campos de la interfaz de productos.

        :return: None

        """
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
        """

        Limpia los campos de la interfaz de productos.

        :return: None

        """
        try:
            var.ui.edit_pro_nombre.setText('')
            var.ui.lbl_pro_muestra_codigo.setText('')
            var.ui.dspin_pro_precio.setValue(0.01)
            var.ui.spin_pro_stock.setValue(0)
        except Exception as error:
            print('Error en limpiar_campos: %s ' % str(error))

    @classmethod
    def eliminar_producto(cls):
        """
        Funcion para llamar al dialogo de confirmacion para eliminar a un producto.

        :return: None

        """
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            if codigo != '':
                cls.dlgEliminarProducto.show()
                cls.dlgEliminarProducto.pregunta.setText("Esta seguro/a que quiere borrar\n"
                                                         "este producto?")
            else:
                events.aviso("Seleccione un producto")
        except Exception as error:
            print('Error en eliminar_producto: %s' % str(error))

    @classmethod
    def baja_producto(cls):
        """

        Recoge el código del producto y lo elimina de la base de datos, actualiza la tabla de productos y limpia los
        campos de la interfaz.

        :return: None

        """
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            cls.db_baja_producto(codigo)
            cls.db_actualizar_tabla_pro()
            Productos.limpiar_campos()
        except Exception as error:
            print('Error en baja_producto: %s ' % str(error))

    @classmethod
    def modificar_producto(cls):
        """

        Recoge los nuevos datos de un producto ya existente y llama a la función que los actualiza en la base de datos.

        :return: None

        """
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            newdata = [var.ui.edit_pro_nombre.text(), var.ui.dspin_pro_precio.value(), var.ui.spin_pro_stock.value()]
            cls.db_modif_producto(codigo, newdata)
            cls.db_actualizar_tabla_pro()
        except Exception as error:
            print('Error en modificar_producto: %s ' % str(error))

    @classmethod
    def recargar(cls):
        """

        Recarga la tabla de productos y limpia los campos de la interfaz.

        :return: None

        """
        try:
            Productos.limpiar_campos()
            cls.db_actualizar_tabla_pro()
        except Exception as error:
            print('Error en recargar: %s ' % str(error))

    @staticmethod
    def db_actualizar_tabla_pro():
        """

        Actualiza la tabla de productos leyendo los datos guardados en la base de datos.

        :return: None

        """
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
            print("Error en db_actualizar_tabla_pro: ", query.lastError().text())

    @classmethod
    def db_alta_producto(cls, producto: [str, float, int]):
        """

        Inserta en la base de datos un producto con los datos pasados como parámetros.

        :param producto: lista, datos del producto
        :return: None

        """
        query = QtSql.QSqlQuery()
        query.prepare('insert into articulos (nombre, precio_unidad, stock)'
                      'VALUES (:nombre, :precio_unidad, :stock)')
        query.bindValue(':nombre', str(producto[0]))
        query.bindValue(':precio_unidad', round(producto[1], 2))
        query.bindValue(':stock', producto[2])
        if query.exec_():
            cls.db_actualizar_tabla_pro()
            var.ui.lbl_status.setText('El producto ' + str(producto[0]) + ' ha sido dado de alta')
        else:
            print("Error en db_alta_producto: ", query.lastError().text())

    @staticmethod
    def db_baja_producto(codigo):
        """

        Da de baja en la base de datos el producto con el codigo pasado como parámetro.

        :param codigo: int, codigo del producto
        :return: None

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from articulos where codigo = :codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            var.ui.lbl_status.setText('Producto de codigo ' + codigo + ' dado de baja')
        else:
            print("Error en db_baja_producto: ", query.lastError().text())

    @staticmethod
    def db_modif_producto(codigo, nuevos_datos):
        """

        Modifica los datos del producto con el código pasado por parámetro con los nuevos datos pasados por parámetro
        dentro de la base de datos.

        :param codigo: int, codigo del producto
        :param nuevos_datos: lista, datos del producto
        :return: None

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
            var.ui.lbl_status.setText('El producto  ' + str(nuevos_datos[0]) + ' ha sido modificado')
        else:
            print("Error en db_modif_producto: ", query.lastError().text())

    @staticmethod
    def importar_producto(datos: [str, float, int]):
        """

        Importa un producto con los datos del producto pasados como parámetro. Si ya existe en la base actualiza el
        precio y le suma el stock, y si no existe lo inserta con todos los datos.

        :param datos:
        :return:
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select * from articulos where nombre = :nombre')
            query.bindValue(':nombre', datos[0])
            if query.exec_() and query.size() == 4:
                while query.next():
                    query_up = QtSql.QSqlQuery()
                    codigo = int(query_up.value(0))
                    nuevo_precio = datos[1]
                    nuevo_stock = query_up.value(3) + datos[2]
                    query_up.prepare('update articulos set nombre=:nombre, precio_unidad=:precio, stock=:stock '
                                     'where codigo=:codigo')
                    query_up.bindValue(':codigo', codigo)
                    query_up.bindValue(':nombre', datos[0])
                    query_up.bindValue(':precio', round(nuevo_precio, 2))
                    query_up.bindValue(':stock', nuevo_stock)
                    if query_up.exec_():
                        pass
                    else:
                        print('Error en actualizar importar_producto')
            else:
                query_add = QtSql.QSqlQuery()
                query_add.prepare('insert into articulos (nombre, precio_unidad, stock)'
                                  'VALUES (:nombre, :precio_unidad, :stock)')
                query_add.bindValue(':nombre', datos[0])
                query_add.bindValue(':precio_unidad', round(datos[1], 2))
                query_add.bindValue(':stock', datos[2])
                if query_add.exec_():
                    pass
                else:
                    print('Error en insertar importar_producto')
        except Exception as error:
            print('Error en importar_producto: %s' % str(error))
