from datetime import datetime

from PyQt5 import QtSql
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

import var


class Printer():

    @staticmethod
    def cabecera():
        logo = '.\\res\img\logo.jpg'
        var.rep.setTitle('INFORME CLIENTES')
        var.rep.setAuthor('Administración')
        var.rep.setFont('Helvetica', size=10)
        var.rep.line(45, 820, 525, 820)
        var.rep.line(45, 745, 525, 745)
        textcif = 'A00000000H'
        textnom = 'IMPORTACIÓN Y ESXPORTACIÓN TEIS, S.L.'
        textdir = 'Avenida Galicia, 101 - Vigo'
        texttlf = '886 12 04 04'
        var.rep.drawString(50, 805, textcif)
        var.rep.drawString(50, 790, textnom)
        var.rep.drawString(50, 775, textdir)
        var.rep.drawString(50, 760, texttlf)
        var.rep.drawImage(logo, 450, 752)

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
            print('Error en el pie de informe: %s' % str(error))

    @staticmethod
    def informe_cliente():
        try:
            var.rep = canvas.Canvas('informes/listadoclientes.pdf', pagesize=A4)
            Printer.cabecera()
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE CLIENTES'
            var.rep.drawString(100, 750, textlistado)
            var.rep.line(45, 725, 525, 725)
            itemcli = ['COD', 'DNI', 'APELLIDOS', 'NOMBRE', 'FECHA ALTA']
            var.rep.drawString(45, 710, itemcli[0])
            var.rep.drawString(90, 710, itemcli[1])
            var.rep.drawString(180, 710, itemcli[2])
            var.rep.drawString(325, 710, itemcli[3])
            var.rep.drawString(465, 710, itemcli[4])
            var.rep.line(45, 703, 525, 703)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, dni, apellidos, nombre, fechalta from clientes order by apellidos, nombre')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 50
                j = 690
                while query.next():
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i+30, j, str(query.value(1)))
                    var.rep.drawString(i+130, j, str(query.value(2)))
                    var.rep.drawString(i+280, j, str(query.value(3)))
                    var.rep.drawRightString(i+470, j, str(query.value(4)))
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
    def informe_productos():
        try:
            var.rep = canvas.Canvas('informes/listadoproducto.pdf', pagesize=A4)
            Printer.cabecera()
            var.rep.setFont('Helvetica-Bold', size=9)
            textlistado = 'LISTADO DE CLIENTES'
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
                    var.rep.drawString(i+100, j, str(query.value(1)))
                    var.rep.drawString(i+240, j, str(query.value(2)))
                    var.rep.drawString(i+360, j, str(query.value(3)))
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
