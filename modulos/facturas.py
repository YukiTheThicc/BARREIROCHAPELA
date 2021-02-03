from datetime import datetime
from PyQt5 import QtSql

from venCalendar import *
import var


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
    cmb_articulos = None

    @classmethod
    def crear_modulo(cls):
        """



        :return:
        :rtype:



        """
        cls.dlg_calendar = DialogCalendar()

        var.ui.btn_fac_calendar.clicked.connect(Facturas.abrir_calendar)

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
    def cargar_cmb_articulos(cls):
        """



        :return:
        :rtype:



        """
        cls.cmb_articulos.clear()
        query = QtSql.QSqlQuery()
        cls.cmb_articulos.addItem('')
        query.prepare('select codigo, producto from productos order by producto')
        if query.exec_():
            while query.next():
                cls.cmb_articulos.addItem(str(query.value(1)))

    @classmethod
    def cargar_fecha(cls, qDate):
        """



        :param qDate:
        :type qDate:
        :return:
        :rtype:



        """
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.edit_fac_calendar.setText(str(data))
            cls.dlg_calendar.hide()
        except Exception as error:
            print('Error en cargar_fecha: %s ' % str(error))

    @classmethod
    def alta_fac(cls):
        """



        :return:
        :rtype:



        """
        dni = var.ui.edit_fac_dni.text()
        nombre = var.ui.edit_fac_nombre.text()
        fecha = var.ui.edit_fac_calendar.text()
        if dni != '' and fecha != '':
            cls.db_alta_factura(dni, fecha, nombre)

    @classmethod
    def cargar_factura(cls):
        """



        :return:
        :rtype:



        """
        try:
            fila = var.ui.tbl_fac_listfact.selectedItems()


    @staticmethod
    def limpiar_fac():
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
            var.ui.lblstatus.setText('Factura Creada')
            cls.db_mostrar_facturas()
        else:
            print("Error en db_alta_factura: ", query.lastError().text())

    @staticmethod
    def db_mostrar_facturas():
        """



        :return:
        :rtype:



        """
        i = 0
        query = QtSql.QSqlQuery()
        query.prepare('select cod_factura, fecha from facturas order by codfac desc')
        if query.exec_():
            var.ui.tbl_fac_listfact.setRowCount(i + 1)
            var.ui.tbl_fac_listfact(1, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
            var.ui.tbl_fac_listfact(i, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
        else:
            print("Error mostrar facturas: ", query.lastError().text())
        if i == 0:
            var.ui.tabFac.clearContents()

    @staticmethod
    def db_mostrar_facturas_por_cliente():
        """



        :return:
        :rtype:



        """
        dni = var.ui.editDniclifac.text()
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, fecha from facturas where dni = :dni order by codfac desc')
        query.bindValue(':dni', str(dni))
        i = 0
        if query.exec_():
            while query.next():
                codfac = query.value(0)
                fecha = query.value(1)
                var.ui.tabFac.setRowCount(i + 1)
                var.ui.tabFac.setItem(i, 0, QtWidgets.QTableWidgetItem(str(codfac)))
                var.ui.tabFac.setItem(i, 1, QtWidgets.QTableWidgetItem(str(fecha)))
                i += 1
            if i == 0:
                var.ui.tabFac.setRowCount(0)
                var.ui.lblstatus.setText('Cliente sin Facturas')
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
                var.ui.editDniclifac.setText(str(query.value(0)))
                var.ui.editApelclifac.setText(str(query.value(1)))
