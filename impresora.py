from reportlab.pdfgen import canvas
import os

class Printer():

    @staticmethod
    def reportCli():
        try:
            c = canvas.Canvas('informes/listadoclientes.pdf')
            c.drawString(100,750,'Listado Clientes')
            c.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error reporcli %s' % str(error))
