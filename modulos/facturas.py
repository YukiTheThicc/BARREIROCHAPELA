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
                var.ui.edit_fac_fecha.setText(str(fila[1]))
                cls.db_cargar_fac(str(fila[0]))
        except Exception as error:
            print('Error en cargar_factura: %s ' % str(error))

    @classmethod
    def borrar_factura(cls):
        try:
            codigo = var.ui.lbl_fac_numero.text()
            cls.db_borrar_factura(codigo)

        except Exception as error:
            print('Error Borrar Factura en Cascada: %s ' % str(error))

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
            var.ui.lblstatus.setText('Factura Borrada')
            cls.db_mostrar_facturas()
        else:
            print("Error borrando factura en db_borrar_factura: ", query.lastError().text())
        query.prepare('delete from ventas where codfacventa = :codigo')
        query.bindValue(':codigo', int(codigo))
        if query.exec_():
            var.ui.lblstatus.setText('Factura Anulada')
        else:
            print("Error borrando ventas en db_borrar_factura: ", query.lastError().text())
        var.ui.lblSubtotal.setText('0.00')
        var.ui.lblIva.setText('0.00')
        var.ui.lblTotal.setText('0.00')
