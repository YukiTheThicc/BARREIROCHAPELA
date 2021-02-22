from PyQt5 import QtSql
from PyQt5 import QtWidgets

import var
import modulos.productos as p


class Cmb_articulos(QtWidgets.QComboBox):
    def __init__(self):
        super(Cmb_articulos, self).__init__()
        Ventas.cmb_articulos = QtWidgets.QComboBox()


class Ventas:
    cmb_articulos = None
    sub_total = None
    iva = None
    total = None

    @classmethod
    def crear_modulo(cls):
        """



        :return:

        """
        cls.cmb_articulos = Cmb_articulos()
        cls.cargar_cmb_articulos()

        var.ui.tbl_ventas_lista.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.btn_venta_add.clicked.connect(cls.procesar_venta)
        var.ui.btn_venta_del.clicked.connect(cls.anular_venta)

    @classmethod
    def cargar_cmb_articulos(cls):
        """



        :return:
        :rtype:

        """
        cls.cmb_articulos.clear()
        query = QtSql.QSqlQuery()
        cls.cmb_articulos.addItem('')
        query.prepare('select codigo, nombre from articulos order by nombre')
        if query.exec_():
            while query.next():
                cls.cmb_articulos.addItem(str(query.value(1)))

    @classmethod
    def setup_tabla_ventas(cls, i: int):
        """



        :param i:
        :return:

        """
        try:
            cls.cmb_articulos = QtWidgets.QComboBox()
            cls.cargar_cmb_articulos()
            var.ui.tbl_ventas_lista.setRowCount(i + 1)
            var.ui.tbl_ventas_lista.setItem(i, 0, QtWidgets.QTableWidgetItem())
            var.ui.tbl_ventas_lista.setCellWidget(i, 1, cls.cmb_articulos)
            var.ui.tbl_ventas_lista.setItem(i, 2, QtWidgets.QTableWidgetItem())
            var.ui.tbl_ventas_lista.setItem(i, 3, QtWidgets.QTableWidgetItem())
            var.ui.tbl_ventas_lista.setItem(i, 4, QtWidgets.QTableWidgetItem())
        except Exception as error:
            print('Error en setup_tabla_ventas: %s ' % str(error))

    @classmethod
    def procesar_venta(cls):
        try:
            new_venta = []
            articulo = cls.cmb_articulos.currentText()
            dato = cls.db_recoger_codigo_precio(articulo)
            codfac = var.ui.lbl_fac_numero.text()

            row = var.ui.tbl_ventas_lista.currentRow()
            cantidad = var.ui.tbl_ventas_lista.item(row, 2).text()
            cantidad = cantidad.replace(',', '.')
            precio = dato[1].replace(',', '.')
            subtotal = round(float(cantidad) * float(dato[1]), 2)

            new_venta.append(int(codfac))
            new_venta.append(int(dato[0]))
            new_venta.append(articulo)
            new_venta.append(int(cantidad))
            new_venta.append(round(float(precio), 2))
            new_venta.append(subtotal)
            new_venta.append(row)

            if codfac != '' and articulo != '' and cantidad != '':
                query = QtSql.QSqlQuery()
                query.prepare('select stock from articulos where nombre = :articulo')
                query.bindValue(':articulo', articulo)
                if query.exec_():
                    stock = 0
                    while query.next():
                        stock = query.value(0)
                    if stock >= int(cantidad):
                        cls.db_insertar_venta(new_venta, stock)
                        subtotal = round(float(subtotal), 2)
                        var.ui.lbl_fac_subtotal.setText(str(subtotal))
                        iva = round(float(subtotal) * 0.21, 2)
                        var.ui.lbl_fac_iva.setText(str(iva))
                        total = round(float(iva) + float(subtotal), 2)
                        var.ui.lbl_fac_total.setText(str(total))
                        Ventas.mostrar_ventas()
                    else:
                        var.ui.lbl_status.setText('No hay suficiente stock')
                else:
                    print("Error en procesar_venta: ", query.lastError().text())
            else:
                var.ui.lbl_status.setText('Faltan Datos de la Factura')
        except Exception as error:
            print('Error en procesar_venta: %s ' % str(error))

    @classmethod
    def mostrar_ventas(cls):
        try:
            cls.cmb_articulos = QtWidgets.QComboBox()
            cls.cargar_cmb_articulos()
            cod_fac = var.ui.lbl_fac_numero.text()
            cls.db_ventas_factura(cod_fac)

        except Exception as error:
            print('Error en mostrar_ventas: %s' % str(error))

    @classmethod
    def anular_venta(cls):
        try:
            fila = var.ui.tbl_ventas_lista.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codventa = int(fila[0])
            cls.db_anular_venta(codventa)
            Ventas.mostrar_ventas()

        except Exception as error:
            print('Error en anular_venta: %s' % str(error))

    @classmethod
    def db_insertar_venta(cls, venta, stock):
        query = QtSql.QSqlQuery()
        query.prepare('insert into ventas (cod_factura_venta, cod_articulo_venta, cantidad, coste) VALUES ('
                      ':codfacventa, ' ':codarticventa, :cantidad, :precio )')
        query.bindValue(':codfacventa', int(venta[0]))
        query.bindValue(':codarticventa', int(venta[1]))
        query.bindValue(':cantidad', int(venta[3]))
        query.bindValue(':precio', float(venta[4]))
        row = var.ui.tbl_ventas_lista.currentRow()
        if query.exec_():
            new_stock = stock - int(venta[3])
            query_update_stock = QtSql.QSqlQuery()
            query_update_stock.prepare('update articulos set stock=:new_stock where codigo=:codigo')
            query_update_stock.bindValue(':new_stock', new_stock)
            query_update_stock.bindValue(':codigo', int(venta[1]))
            if query_update_stock.exec_():
                var.ui.tbl_ventas_lista.setItem(row, 1, QtWidgets.QTableWidgetItem(str(venta[2])))
                var.ui.tbl_ventas_lista.setItem(row, 2, QtWidgets.QTableWidgetItem(str(venta[3])))
                var.ui.tbl_ventas_lista.setItem(row, 3, QtWidgets.QTableWidgetItem(str(venta[4])))
                var.ui.tbl_ventas_lista.setItem(row, 4, QtWidgets.QTableWidgetItem(str(venta[5])))
                row = row + 1
                var.ui.tbl_ventas_lista.insertRow(row)
                var.ui.tbl_ventas_lista.setCellWidget(row, 1, cls.cmb_articulos)
                var.ui.tbl_ventas_lista.scrollToBottom()
                cls.cargar_cmb_articulos()
                p.Productos.db_actualizar_tabla_pro()
                var.ui.lbl_status.setText('Venta Realizada')
            else:
                print("Error en db_insertar_venta: ", query.lastError().text())
        else:
            print("Error en db_insertar_venta: ", query.lastError().text())

    @staticmethod
    def db_recoger_codigo_precio(articulo: str):
        """



        :param articulo:
        :type articulo:
        :return:
        :rtype:

        """
        datos = []
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, precio_unidad from articulos where nombre = :articulo')
        query.bindValue(':articulo', articulo)
        if query.exec_():
            while query.next():
                datos = [str(query.value(0)), str(query.value(1))]
        else:
            print("Error en db_recoger_codigo_precio: ", query.lastError().text())
        return datos

    @staticmethod
    def db_anular_venta(cod_venta):
        query = QtSql.QSqlQuery()
        query.prepare('delete from ventas where cod_venta = :cod_venta')
        query.bindValue(':cod_venta', cod_venta)
        if query.exec_():
            var.ui.lbl_status.setText('Venta Anulada')
        else:
            print("Error en db_anular_venta: ", query.lastError().text())

    @classmethod
    def db_ventas_factura(cls, codfac):
        try:
            var.ui.tbl_ventas_lista.clearContents()
            var.subfac = 0.00
            query_ventas = QtSql.QSqlQuery()
            query_articulos = QtSql.QSqlQuery()
            query_ventas.prepare('select cod_venta, cod_articulo_venta, cantidad from ventas where cod_factura_venta '
                                 '= :codfac')
            query_ventas.bindValue(':codfac', int(codfac))
            if query_ventas.exec_():
                index = 0
                subtotal = 0.00
                while query_ventas.next():
                    cod_venta = query_ventas.value(0)
                    cod_articulo_venta = query_ventas.value(1)
                    cantidad = query_ventas.value(2)
                    var.ui.tbl_ventas_lista.setRowCount(index + 1)
                    var.ui.tbl_ventas_lista.setItem(index, 0, QtWidgets.QTableWidgetItem(str(cod_venta)))
                    query_articulos.prepare('select nombre, precio_unidad from articulos where codigo = '
                                            ':cod_articulo_venta')
                    query_articulos.bindValue(':cod_articulo_venta', int(cod_articulo_venta))
                    if query_articulos.exec_():
                        coste_venta = 0
                        while query_articulos.next():
                            articulo = query_articulos.value(0)
                            precio = query_articulos.value(1)
                            var.ui.tbl_ventas_lista.setItem(index, 1, QtWidgets.QTableWidgetItem(str(articulo)))
                            var.ui.tbl_ventas_lista.setItem(index, 2, QtWidgets.QTableWidgetItem(str(cantidad)))
                            coste_venta = round(float(cantidad) * float(precio), 2)
                            var.ui.tbl_ventas_lista.setItem(index, 3, QtWidgets.QTableWidgetItem(str(precio)))
                            var.ui.tbl_ventas_lista.setItem(index, 4, QtWidgets.QTableWidgetItem(str(coste_venta)))
                        index += 1
                        subtotal = round(float(subtotal) + float(coste_venta), 2)
                if int(index) > 0:
                    cls.setup_tabla_ventas(index)
                else:
                    var.ui.tbl_ventas_lista.setRowCount(0)
                    cls.setup_tabla_ventas(0)
                var.ui.lbl_fac_subtotal.setText(str(subtotal))
                iva = round(float(subtotal) * 0.21, 2)
                var.ui.lbl_fac_iva.setText(str(iva))
                total = round(float(iva) + float(subtotal), 2)
                var.ui.lbl_fac_total.setText(str(total))
        except Exception as error:
            print('Error en db_ventas_factura: %s ' % str(error))
