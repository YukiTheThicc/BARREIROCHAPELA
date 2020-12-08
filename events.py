import sys
import var


class Eventos:

    @staticmethod
    def salir(event):
        """
        Modulo para cerrar el programa
        :return:
        """
        try:
            var.dlgSalir.show()
            if var.dlgSalir.exec_():
                sys.exit()
            else:
                var.dlgSalir.close()
                event.ignore()  # necesario para que ignore X de la ventana
        except Exception as error:
            print('Error %s' % str(error))

    @staticmethod
    def aviso(mensaje: str):
        """
        Modulo para cerrar el programa
        :return:
        """
        try:
            var.dlgAviso.show()
            var.dlgAviso.lbl_mensaje.setText(mensaje)
            if var.dlgAviso.btn_ok.clicked():
                var.dlgAviso.close()
        except Exception as error:
            print('Error: %s' % str(error))

    @staticmethod
    def cargarProv():
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