from datetime import datetime
from PyQt5 import QtSql

from venCalendar import *
import var
import modulos.ventas as v


class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        Facturas.dlg_calendar = ui_ven_calendar()
        Facturas.dlg_calendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        Facturas.dlg_calendar.calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        Facturas.dlg_calendar.calendar.clicked.connect(Facturas.cargar_fecha)


class Facturas:

    dlg_calendar = None

    @classmethod
    def crear_modulo(cls):
        """

        Modulo que crea las conexiones a eventos y ventanas de dialogo necesarias para el funcionamiento del

        :return:
        :rtype:

        """
        cls.dlg_calendar = DialogCalendar()

        var.ui.btn_fac_calendar.clicked.connect(cls.abrir_calendar)
        var.ui.btn_fac_facturar.clicked.connect(cls.alta_factura)
        var.ui.btn_fac_anular.clicked.connect(cls.borrar_factura)
        var.ui.btn_fac_buscar.clicked.connect(cls.db_mostrar_facturas_por_cliente)
        var.ui.btn_fac_recargar.clicked.connect(cls.db_mostrar_facturas)
        var.ui.tbl_fac_listfact.clicked.connect(cls.cargar_factura)
        var.ui.tbl_fac_listfact.clicked.connect(v.Ventas.mostrar_ventas)
        var.ui.tbl_fac_listfact.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        cls.db_mostrar_facturas()

    @classmethod
    def abrir_calendar(cls):
        """



        :return:
        :rtype:

        """
        try:
            cls.dlg_calendar.show()
        except Exception as error:
            print('Error en abrir_calendar: %s ' % str(error))

    @classmethod
    def cargar_fecha(cls, q_date):
        """



        :param q_date:
        :type q_date:
        :return:
        :rtype:

        """
        try:
            data = ('{0}/{1}/{2}'.format(q_date.day(), q_date.month(), q_date.year()))
            var.ui.edit_fac_calendar.setText(str(data))
            cls.dlg_calendar.hide()
        except Exception as error:
            print('Error en cargar_fecha: %s ' % str(error))

    @classmethod
    def alta_factura(cls):
        """



        :return:
        :rtype:

        """
        dni = var.ui.edit_fac_dni.text()
        nombre = var.ui.edit_fac_nombre.text()
        fecha = var.ui.edit_fac_calendar.text()
        if dni != '' and fecha != '':
            cls.db_alta_factura(dni, fecha, nombre)
        v.Ventas.setup_tabla_ventas(0)

    @classmethod
    def cargar_factura(cls):
        """



        :return:
        :rtype:

        """
        try:
            fila = var.ui.tbl_fac_listfact.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
                var.ui.lbl_fac_numero.setText(str(fila[0]))
                var.ui.edit_fac_calendar.setText(str(fila[1]))
                cls.db_cargar_fac(str(fila[0]))
        except Exception as error:
            print('Error en cargar_factura: %s ' % str(error))

    @classmethod
    def borrar_factura(cls):
        """



        :return:

        """
        try:
            codigo = var.ui.lbl_fac_numero.text()
            cls.db_borrar_factura(codigo)
            v.Ventas.setup_tabla_ventas(0)
        except Exception as error:
            print('Error en borrar_factura: %s ' % str(error))

    @staticmethod
    def limpiar_factura():
        """



        :return:
        :rtype:

        """
        var.ui.edit_fac_dni.setText("")
        var.ui.edit_fac_nombre.setText("")
        var.ui.edit_fac_calendar.setText("")
        var.ui.lbl_fac_numero.setText("")

    @classmethod
    def db_alta_factura(cls, dni, fecha, nombre):
        """



        :param dni:
        :type dni:
        :param fecha:
        :type fecha:
        :param nombre:
        :type nombre:
        :return:
        :rtype:

        """
        query = QtSql.QSqlQuery()
        query.prepare('insert into facturas (dni, fecha, apellidos) VALUES (:dni, :fecha, :apellidos )')
        query.bindValue(':dni', str(dni))
        query.bindValue(':fecha', str(fecha))
        query.bindValue(':apellidos', str(nombre))
        if query.exec_():
            var.ui.lbl_status.setText('Factura Creada')
            cls.db_mostrar_facturas()
        else:
            print("Error en db_alta_factura: ", query.lastError().text())

    @classmethod
    def db_mostrar_facturas(cls):
        """



        :return:
        :rtype:

        """
        i = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, fecha from facturas order by codfac desc')
        if query.exec_():
            while query.next():
                var.ui.tbl_fac_listfact.setRowCount(i + 1)
                var.ui.tbl_fac_listfact.setItem(i, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                var.ui.tbl_fac_listfact.setItem(i, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                i += 1
            cls.limpiar_factura()
            var.ui.tbl_fac_listfact.selectRow(0)
            var.ui.tbl_fac_listfact.setFocus()
        else:
            print("Error db_mostrar_facturas: ", query.lastError().text())
        if i == 0:
            var.ui.tbl_fac_listfact.clearContents()

    @staticmethod
    def db_mostrar_facturas_por_cliente():
        """



        :return:
        :rtype:

        """
        dni = var.ui.edit_fac_dni.text()
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, fecha from facturas where dni = :dni order by codfac desc')
        query.bindValue(':dni', str(dni))
        i = 0
        if query.exec_():
            while query.next():
                codfac = query.value(0)
                fecha = query.value(1)
                var.ui.tbl_fac_listfact.setRowCount(i + 1)
                var.ui.tbl_fac_listfact.setItem(i, 0, QtWidgets.QTableWidgetItem(str(codfac)))
                var.ui.tbl_fac_listfact.setItem(i, 1, QtWidgets.QTableWidgetItem(str(fecha)))
                i += 1
            if i == 0:
                var.ui.tbl_fac_listfact.setRowCount(0)
                var.ui.lbl_status.setText('Cliente sin Facturas')
        else:
            print("Error en db_mostrar_facturas_por_cliente: ", query.lastError().text())

    @staticmethod
    def db_cargar_fac(cod):
        """



        :param cod:
        :type cod:
        :return:
        :rtype:

        """
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos from facturas where codfac = :codfac')
        query.bindValue(':codfac', int(cod))
        if query.exec_():
            while query.next():
                var.ui.edit_fac_dni.setText(str(query.value(0)))
                var.ui.edit_fac_nombre.setText(str(query.value(1)))
        else:
            print("Error en db_cargar_fac: ", query.lastError().text())

    @classmethod
    def db_borrar_factura(cls, codigo):
        """



        :param codigo:
        :return:

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from facturas where codfac = :codigo')
        query.bindValue(':codigo', int(codigo))
        if query.exec_():
            var.ui.lbl_status.setText('Factura Borrada')
            cls.db_mostrar_facturas()
        else:
            print("Error en db_borrar_factura: ", query.lastError().text())
        query.prepare('delete from ventas where cod_factura_venta = :codigo')
        query.bindValue(':codigo', int(codigo))
        if query.exec_():
            var.ui.lbl_status.setText('Factura Anulada')
        else:
            print("Error en db_borrar_factura: ", query.lastError().text())
        var.ui.lbl_fac_subtotal.setText('0.00')
        var.ui.lbl_fac_iva.setText('0.00')
        var.ui.lbl_fac_total.setText('0.00')
