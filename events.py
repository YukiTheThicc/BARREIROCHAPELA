import sys
import var
from modulos import productos as p
from modulos.clientes import Clientes


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
            Clientes.dlgEliminarCliente.show()
            Clientes.dlgEliminarCliente.pregunta.setText("Esta seguro/a que quiere borrar?")
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

    @staticmethod
    def about():
        try:
            var.dlgAbout.show()
        except Exception as error:
            print('Error en about events %s' % str(error))

# =============================================== EVENTOS PARA PRODUCTOS ===============================================

    @staticmethod
    def eliminar_producto():
        """
        Funcion para llamar al dialogo de confirmacion y recoger el resultado
        :return:
        """
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            if codigo != '':
                var.dlgEliminarProducto.show()
                var.dlgEliminarProducto.pregunta.setText("Esta seguro/a que quiere borrar\n"
                                                         "este producto?")
            else:
                Eventos.aviso("Seleccione un producto")
        except Exception as error:
            print('Error: %s' % str(error))

    @staticmethod
    def modificar_producto():
        """
        Funcion para llamar al dialogo de confirmacion y recoger el resultado
        :return:
        """
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            nombre = var.ui.lbl_pro_nombre.text()
            print(nombre)
            if codigo != '':
                if nombre != '':
                    p.Productos.modif_producto()
                else:
                    Eventos.aviso("Necesita un nombre")
            else:
                Eventos.aviso("Seleccione un producto")
        except Exception as error:
            print('Error en modificar_producto events: %s' % str(error))

# ============================================ EVENTOS PARA FACTURAS/VENTAS ============================================
