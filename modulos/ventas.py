from PyQt5 import QtSql
from PyQt5 import QtWidgets

import var


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
        '''
        Modulo que prepara tabla Ventas, carga un combo en la tabla
        y carga dicho combo con los datos del producto
        :return:
        '''
        try:
            cls.cmb_articulos = QtWidgets.QComboBox()
            cls.cargar_cmb_articulos()
            var.ui.tabVenta.setRowCount(i + 1)
            var.ui.tabVenta.setItem(i, 0, QtWidgets.QTableWidgetItem())
            var.ui.tabVenta.setCellWidget(i, 1, cls.cmb_articulos)
            var.ui.tabVenta.setItem(i, 2, QtWidgets.QTableWidgetItem())
            var.ui.tabVenta.setItem(i, 3, QtWidgets.QTableWidgetItem())
            var.ui.tabVenta.setItem(i, 4, QtWidgets.QTableWidgetItem())
        except Exception as error:
            print('Error Preparar tabla de ventas: %s ' % str(error))

    @classmethod
    def procesar_venta(cls):
        try:
            new_venta = []
            articulo = cls.cmb_articulos.currentText()
            dato = cls.db_recoger_codigo_precio(articulo)
            codfac = var.ui.lblNumFac.text()

            row = var.ui.tabVenta.currentRow()
            cantidad = var.ui.tabVenta.item(row, 2).text()
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
                cls.db_insertar_venta(new_venta)
                subtotal = round(float(subtotal), 2)
                var.ui.lblSubtotal.setText(str(subtotal))
                iva = round(float(subtotal) * 0.21, 2)
                var.ui.lblIva.setText(str(iva))
                total = round(float(iva) + float(subtotal), 2)
                var.ui.lblTotal.setText(str(total))
                Ventas.mostrar_ventas()
            else:
                var.ui.lblstatus.setText('Faltan Datos de la Factura')

        except Exception as error:
            print('Error en procesar_venta: %s ' % str(error))

    @classmethod
    def mostrar_ventas(cls):
        try:
            cls.cmb_articulos = QtWidgets.QComboBox()
            cls.cargar_cmb_articulos()
            cod_fac = var.ui.lblNumFac.text()
            cls.db_ventas_factura(cod_fac)

        except Exception as error:
            print('Error en mostrar_ventas: %s' % str(error))

    @classmethod
    def anular_venta(cls):
        try:
            fila = var.ui.tabVenta.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codventa = int(fila[0])
            cls.db_anular_venta(codventa)
            Ventas.mostrar_ventas()

        except Exception as error:
            print('Error proceso anular venta de una factura: %s' % str(error))

    @classmethod
    def db_insertar_venta(cls, venta):
        query = QtSql.QSqlQuery()
        query.prepare('insert into ventas (codfacventa, codarticventa, cantidad, precio) VALUES (:codfacventa, '
                      ':codarticventa, :cantidad, :precio )')
        query.bindValue(':codfacventa', int(venta[0]))
        query.bindValue(':codarticventa', int(venta[1]))
        query.bindValue(':cantidad', int(venta[3]))
        query.bindValue(':precio', float(venta[4]))
        row = var.ui.tabVenta.currentRow()
        if query.exec_():
            var.ui.lblstatus.setText('Venta Realizada')
            var.ui.tabVenta.setItem(row, 1, QtWidgets.QTableWidgetItem(str(venta[2])))
            var.ui.tabVenta.setItem(row, 2, QtWidgets.QTableWidgetItem(str(venta[3])))
            var.ui.tabVenta.setItem(row, 3, QtWidgets.QTableWidgetItem(str(venta[4])))
            var.ui.tabVenta.setItem(row, 4, QtWidgets.QTableWidgetItem(str(venta[5])))
            row = row + 1
            var.ui.tabVenta.insertRow(row)
            var.ui.tabVenta.setCellWidget(row, 1, cls.cmb_articulos)
            var.ui.tabVenta.scrollToBottom()
            cls.cargar_cmb_articulos()
        else:
            print("Error alta venta: ", query.lastError().text())

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
        query.bindValue(':codfac', articulo)
        if query.exec_():
            while query.next():
                datos = [str(query.value(0)), str(query.value(1))]
        return datos

    @staticmethod
    def db_anular_venta(cod_venta):
        query = QtSql.QSqlQuery()
        query.prepare('delete from ventas where cod_venta = :cod_venta')
        query.bindValue(':cod_venta', cod_venta)
        if query.exec_():
            var.ui.lblstatus.setText('Venta Anulada')
        else:
            print("Error baja venta: ", query.lastError().text())

    @classmethod
    def db_ventas_factura(cls, codfac):
        try:
            var.ui.tabVenta.clearContents()
            var.subfac = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad from ventas where codfacventa = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                index = 0
                subtotal = 0.00
                while query.next():
                    codventa = query.value(0)
                    codarticventa = query.value(1)
                    cantidad = query.value(2)
                    var.ui.tabVenta.setRowCount(index + 1)
                    var.ui.tabVenta.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                    query1.prepare('select producto, precio from productos where codigo = :codarticventa')
                    query1.bindValue(':codarticventa', int(codarticventa))
                    if query1.exec_():
                        while query1.next():
                            articulo = query1.value(0)
                            precio = query1.value(1)
                            var.ui.tabVenta.setItem(index, 1, QtWidgets.QTableWidgetItem(str(articulo)))
                            var.ui.tabVenta.setItem(index, 2, QtWidgets.QTableWidgetItem(str(cantidad)))
                            subtotal = round(float(cantidad) * float(precio), 2)
                            var.ui.tabVenta.setItem(index, 3, QtWidgets.QTableWidgetItem(str(precio)))
                            var.ui.tabVenta.setItem(index, 4, QtWidgets.QTableWidgetItem(str(subtotal)))
                        index += 1
                        subtotal = round(float(subtotal) + float(subtotal), 2)
                cls.setup_tabla_ventas(index)
                if int(index) > 0:
                    cls.setup_tabla_ventas(index)
                else:
                    print(index)
                    var.ui.tabVenta.setRowCount(0)
                    cls.setup_tabla_ventas(0)
                var.ui.lblSubtotal.setText(str(subtotal))
                iva = round(float(subtotal) * 0.21, 2)
                var.ui.lblIva.setText(str(iva))
                total = round(float(iva) + float(subtotal), 2)
                var.ui.lblTotal.setText(str(total))
        except Exception as error:
            print('Error Listado de la tabla de ventas: %s ' % str(error))
