import sys
import var
from PyQt5 import QtWidgets


class Eventos:

    @staticmethod
    def salir(event):
        """
        Modulo para cerrar el programa
        :return:
        """
        try:
            var.dlgSalir.show()
            var.lbl_pregunta.setText("Seguro/a que quiere salir?")
            if var.dlgSalir.exec_():
                sys.exit()
            else:
                var.dlgSalir.close()
                event.ignore()  # necesario para que ignore X de la ventana
        except Exception as error:
            print('Error %s' % str(error))

    @staticmethod
    def abrir_buscador():
        try:
            var.dlgBuscador.show()
        except Exception as error:
            print('Error abrir explorador: %s ' % str(error))

    @staticmethod
    def abrir_impresora():
        try:
            var.dlgImprimir.setWindowTitle('Imprimir')
            var.dlgImprimir.setModal(True)
            var.dlgImprimir.show()
        except Exception as error:
            print('Error abrir imprimr: %s ' % str(error))

    @staticmethod
    def eliminar():
        """
        Funcion para llamar al dialogo de confirmacion y recoger el resultado
        :return:
        """
        try:
            var.dlgConfirmacion.show()
            var.dlgConfirmacion.pregunta.setText("Esta seguro/a que quiere borrar?")
        except Exception as error:
            print('Error: %s' % str(error))

    @staticmethod
    def aviso(mensaje: str):
        """
        Modulo para cerrar el programa
        :return:
        """
        try:
            var.dlgAviso.show()
            var.lbl_mensaje.setText(mensaje)
        except Exception as error:
            print('Error: %s' % str(error))

    @staticmethod
    def cargar_prov():
        '''
        Carga las provincias al iniciar el programa
        :return:
        '''
        try:
            prov = ['','Pontevedra','A Coruña','Lugo','Ourense']
            for i in prov:
                var.ui.cmb_prov.addItem(i)
        except Exception as error:
            print('Error %s' % str(error))