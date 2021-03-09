from datetime import datetime

from PyQt5 import QtSql
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

import var


class Printer():

    @staticmethod
    def cabecera():
        """

        Imprime la cabecera de todos los informes.

        :return: None

        """
        try:
            logo = './res/img/logo.jpg'
            var.rep.setTitle('INFORMES')
            var.rep.setAuthor('Administración')
            var.rep.setFont('Helvetica', size=10)
            var.rep.line(45, 820, 525, 820)
            var.rep.line(45, 745, 525, 745)
            textcif = 'CIF: B050000S'
            textnom = 'EMPRESA, S.L.'
            textdir = 'O Casal nº 6, Moaña'
            texttlfo = 'Tlfo: 986 31 55 55'
            var.rep.drawString(50, 805, textcif)
            var.rep.drawString(50, 790, textnom)
            var.rep.drawString(50, 775, textdir)
            var.rep.drawString(50, 760, texttlfo)
            var.rep.drawImage(logo, 450, 752)
        except Exception as error:
            print("Error en cabecera: %s" % str(error))

    @staticmethod
    def cabecera_cliente():
        """

        Imprime la cabecera del informe de clientes.

        :return: None

        """
        try:
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE CLIENTES'
            var.rep.drawString(255, 735, textlistado)
            var.rep.line(45, 730, 525, 730)
            itemcli = ['Cod', 'DNI', 'APELLIDOS', 'NOMBRE', 'FECHA ALTA']
            var.rep.drawString(45, 710, itemcli[0])
            var.rep.drawString(90, 710, itemcli[1])
            var.rep.drawString(180, 710, itemcli[2])
            var.rep.drawString(325, 710, itemcli[3])
            var.rep.drawString(465, 710, itemcli[4])
            var.rep.line(45, 703, 525, 703)
        except Exception as error:
            print('Error en cabecera_cliente: %s' % str(error))

    @staticmethod
    def cabecera_producto():
        """

        Imprime la cabecera del informe de productos.

        :return: None

        """
        try:
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE PRODUCTOS'
            var.rep.drawString(255, 735, textlistado)
            var.rep.line(45, 730, 525, 730)
            itempro = ['Código', 'NOMBRE', 'PRECIO (€/kg)', 'STOCK (kg)']
            var.rep.drawString(45, 710, itempro[0])
            var.rep.drawString(170, 710, itempro[1])
            var.rep.drawString(340, 710, itempro[2])
            var.rep.drawString(475, 710, itempro[3])
            var.rep.line(45, 703, 525, 703)
        except Exception as error:
            print('Error en cabecera 2 de productos : %s' % str(error))

    @staticmethod
    def cabecera_factura(codfac):
        """

        Imprime la cabecera del informe de facturas.

        :param codfac: int, codigo de factura
        :return: None

        Imprime la cabecera del informe de una factura según el código pasado como parámetro.

        """
        try:
            var.rep.setFont('Helvetica-Bold', size=11)
            var.rep.drawString(55, 725, 'Cliente: ')
            var.rep.setFont('Helvetica', size=10)
            var.rep.drawString(50, 650, 'Factura nº : %s' % str(codfac))
            var.rep.line(45, 665, 525, 665)
            var.rep.line(45, 640, 525, 640)
            var.rep.setFont('Helvetica', size=10)
            query = QtSql.QSqlQuery()
            query.prepare('select dni, fecha from facturas where codfac = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                while query.next():
                    dni = str(query.value(0))
                    var.rep.drawString(55, 710, 'DNI: %s' % str(query.value(0)))
                    var.rep.drawString(420, 650, 'Fecha: %s' % str(query.value(1)))
            query1 = QtSql.QSqlQuery()
            query1.prepare('select apellidos, nombre, direccion, provincia, formaspago from clientes where dni = :dni')
            query1.bindValue(':dni', str(dni))
            if query1.exec_():
                while query1.next():
                    var.rep.drawString(55, 695, str(query1.value(0)) + ', ' + str(query1.value(1)))
                    var.rep.drawString(300, 695, 'Formas de Pago: ')
                    var.rep.drawString(55, 680, str(query1.value(2)) + ' - ' + str(query1.value(3)))
                    var.rep.drawString(300, 680, str(query1.value(4).strip('[]').replace('\'', '').replace(',',
                                                                                                           ' -')))  # \ caracter escape indica que lo siguiente tiene un significado especial
            var.rep.line(45, 625, 525, 625)
            var.rep.setFont('Helvetica-Bold', size=10)
            temven = ['CodVenta', 'Artículo', 'Cantidad', 'Precio-Unidad(€)', 'Subtotal(€)']
            var.rep.drawString(50, 630, temven[0])
            var.rep.drawString(140, 630, temven[1])
            var.rep.drawString(275, 630, temven[2])
            var.rep.drawString(360, 630, temven[3])
            var.rep.drawString(470, 630, temven[4])
            var.rep.setFont('Helvetica-Bold', size=12)
            var.rep.drawRightString(500, 160, 'Subtotal:   ' + "{0:.2f}".format(float(
                var.ui.lbl_fac_subtotal.text())) + ' €')
            var.rep.drawRightString(500, 140, 'IVA:     ' + "{0:.2f}".format(float(var.ui.lbl_fac_iva.text())) + ' €')
            var.rep.drawRightString(500, 115, 'Total Factura: ' + "{0:.2f}".format(float(
                var.ui.lbl_fac_total.text())) + ' €')
        except Exception as error:
            print('Error en cabecera_factura %s' % str(error))

    @staticmethod
    def pie(textlistado):
        try:
            var.rep.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d.%m.%Y  %H.%M.%S')
            var.rep.setFont('Helvetica-Oblique', size=7)
            var.rep.drawString(460, 40, str(fecha))
            var.rep.drawString(275, 40, str('Página %s' % var.rep.getPageNumber))
            var.rep.drawString(50, 40, str(textlistado))

        except Exception as error:
            print('Error en pie: %s' % str(error))


    @staticmethod
    def recoger_nombre_articulo(codigo):
        """

        Método que recoge el nombre de un artículo según su código.

        :param codigo: int, código de artículo
        :return: None

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select nombre from articulos where codigo = :codigo')
            query.bindValue(':codigo', int(codigo))
            if query.exec_():
                while query.next():
                    articulo = query.value(0)
                    return articulo
        except Exception as error:
            print('Error en recoger_nombre_articulo:  %s ' % str(error))

    @staticmethod
    def informe_cliente():
        """

        Crea el cuerpo del informe de clientes.

        :return: None

        """
        try:
            textlistado = 'LISTADO DE CLIENTES'
            var.rep = canvas.Canvas('informes/listadoclientes.pdf', pagesize=A4)
            Printer.cabecera()
            Printer.cabecera_cliente()
            Printer.pie(textlistado)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, dni, apellidos, nombre, fechalta from clientes order by apellidos, nombre')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 50  # valores del eje X
                j = 690  # valores del eje Y
                while query.next():
                    if j <= 80:
                        var.rep.drawString(440, 70, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.pie(textlistado)
                        Printer.cabecera_cliente()
                        i = 55
                        j = 690
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i + 30, j, str(query.value(1)))
                    var.rep.drawString(i + 130, j, str(query.value(2)))
                    var.rep.drawString(i + 275, j, str(query.value(3)))
                    var.rep.drawRightString(i + 465, j, str(query.value(4)))
                    j = j - 25
            var.rep.save()
            root_path = ".\\informes"
            cont = 0
            for file in os.listdir(root_path):
                if file.endswith('listadoclientes.pdf'):
                    os.startfile("%s/%s" % (root_path, file))
                cont = cont + 1
        except Exception as error:
            print('Error reporcli %s' % str(error))

    @staticmethod
    def informe_productos():
        """

        Crea el cuerpo del informe de productos.

        :return: None

        """
        try:
            var.rep = canvas.Canvas('informes/listadoproducto.pdf', pagesize=A4)
            Printer.cabecera()
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE PRODUCTOS'
            var.rep.drawString(100, 750, textlistado)
            var.rep.line(45, 725, 525, 725)
            itemcli = ['CÓDIGO', 'NOMBRE', 'PRECIO/UNIDAD (€)', 'STOCK']
            var.rep.drawString(85, 710, itemcli[0])
            var.rep.drawString(205, 710, itemcli[1])
            var.rep.drawString(315, 710, itemcli[2])
            var.rep.drawString(445, 710, itemcli[3])
            var.rep.line(45, 703, 525, 703)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, precio_unidad, stock from articulos')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 100
                j = 690
                while query.next():
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i + 100, j, str(query.value(1)))
                    var.rep.drawString(i + 240, j, str(query.value(2)))
                    var.rep.drawString(i + 360, j, str(query.value(3)))
                    j -= 30
            Printer.pie(textlistado)
            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error reporcli %s' % str(error))

    @staticmethod
    def informe_facturas():
        """

        Crea el cuerpo del informe de facturas.

        :return: None

        """
        try:
            textlistado = 'FACTURA'
            var.rep = canvas.Canvas('informes/factura.pdf', pagesize=A4)
            Printer.cabecera()
            Printer.pie(textlistado)
            codfac = var.ui.lbl_fac_numero.text()
            Printer.cabecera_factura(codfac)
            query = QtSql.QSqlQuery()
            query.prepare('select cod_venta, cod_articulo_venta, cantidad, coste from ventas where cod_factura_venta = '
                          ':codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                i = 55
                j = 600
                while query.next():
                    if j <= 100:
                        var.rep.drawString(440, 110, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.pie(textlistado)
                        Printer.cabecera_factura(codfac)
                        i = 50
                        j = 600
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    articulo = Printer.recoger_nombre_articulo(str(query.value(1)))
                    var.rep.drawString(i + 85, j, str(articulo))
                    var.rep.drawRightString(i + 245, j, str(query.value(2)))
                    var.rep.drawRightString(i + 355, j, "{0:.2f}".format(float(query.value(3))))
                    subtotal = round(float(query.value(2)) * float(query.value(3)), 2)
                    var.rep.drawRightString(i + 450, j, "{0:.2f}".format(float(subtotal)) + ' €')
                    j = j - 20
            var.rep.save()
            root_path = ".\\informes"
            cont = 0
            for file in os.listdir(root_path):
                if file.endswith('factura.pdf'):
                    os.startfile("%s/%s" % (root_path, file))
                cont = cont + 1
        except Exception as error:
            print('Error informe_facturas %s' % str(error))

    @staticmethod
    def informe_facturas_cliente():
        """

        Crea el cuerpo del informe de las facturas de un cliente.

        :return: None

        """
        try:
            textlistado = 'FACTURAS POR CLIENTE'
            var.rep = canvas.Canvas('informes/facturasporcliente.pdf', pagesize=A4)
            Printer.cabecera()
            Printer.pie(textlistado)
            dni = var.ui.edit_fac_dni.text()
            nombre = var.ui.edit_fac_nombre.text()
            var.rep.drawString(230, 720, textlistado)
            var.rep.line(45, 710, 525, 710)
            var.rep.drawString(45, 730, 'Cliente: %s ' % str(nombre) + '       DNI: %s' % str(dni))
            itempro = ['Nº Factura', 'FECHA FACTURA', 'Total (€)']
            var.rep.line(45, 680, 525, 680)
            var.rep.drawString(45, 690, itempro[0])
            var.rep.drawString(245, 690, itempro[1])
            var.rep.drawString(470, 690, itempro[2])
            query = QtSql.QSqlQuery()
            query.prepare('select codfac, fecha from facturas where dni = :dni')
            query.bindValue(':dni', str(dni))
            total = 0.00
            if query.exec_():
                i = 55
                j = 650
                while query.next():
                    if j <= 100:
                        var.rep.drawString(440, 110, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.pie(textlistado)
                        Printer.cabecera_factura(query.value(0))
                        i = 50
                        j = 600
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawRightString(i + 240, j, str(query.value(1)))

                    query1 = QtSql.QSqlQuery()
                    query1.prepare('select cantidad, coste from ventas where cod_factura_venta = :codfacventa')
                    query1.bindValue(':codfacventa', int(query.value(0)))
                    subtotal = 0.00
                    if query1.exec_():
                        while query1.next():
                            subtotal = subtotal + float(query1.value(0)) * float(query1.value(1))
                        var.rep.drawRightString(i + 440, j, "{0:.2f}".format(float(subtotal) * 1.21) + ' €')
                        total = total + subtotal
                    j = j - 20
            var.rep.drawRightString(i + 430, 120,
                                    'Total Facturación Cliente:   ' + "{0:.2f}".format(float(total) * 1.21)
                                    + ' €')
            var.rep.save()
            root_path = ".\\informes"
            cont = 0
            for file in os.listdir(root_path):
                if file.endswith('facturasporcliente.pdf'):
                    os.startfile("%s/%s" % (root_path, file))
                cont = cont + 1
        except Exception as error:
            print('Error en informe_facturas_cliente:  %s ' % str(error))
