from PyQt5 import QtSql
from PyQt5 import QtWidgets

import var


class Ventas:

    cmb_articulos = None

    @classmethod
    def crear_modulo(cls):
        pass

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
            subtotal = 0.00
            var.venta = []
            codfac = var.ui.lblNumFac.text()
            var.venta.append(int(codfac))
            articulo = cls.cmb_articulos.currentText()
            dato = cls.db_recoger_codigo_precio(articulo)
            var.venta.append(int(dato[0]))
            var.venta.append(articulo)
            row = var.ui.tabVenta.currentRow()
            cantidad = var.ui.tabVenta.item(row, 2).text()
            cantidad = cantidad.replace(',', '.')
            var.venta.append(int(cantidad))
            precio = dato[1].replace(',', '.')
            var.venta.append(round(float(precio),2))
            subtotal = round(float(cantidad)*float(dato[1]), 2)
            var.venta.append(subtotal)
            var.venta.append(row)
            #sleep(1)
            if codfac != '' and articulo != '' and cantidad != '':
                conexion.Conexion.altaVenta()
                var.subfac = round(float(subtotal) + float(var.subfac),2)
                var.ui.lblSubtotal.setText(str(var.subfac))
                var.iva = round(float(var.subfac) * 0.21, 2)
                var.ui.lblIva.setText(str(var.iva))
                var.fac = round(float(var.iva) + float(var.subfac), 2)
                var.ui.lblTotal.setText(str(var.fac))
                Ventas.mostrarVentasfac()
            else:
               var.ui.lblstatus.setText('Faltan Datos de la Factura')

        except Exception as error:
            print('Error en procesar_venta: %s ' % str(error))

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
