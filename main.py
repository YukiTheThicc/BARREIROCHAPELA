from PyQt5 import QtPrintSupport
from PyQt5.QtGui import QIcon

from modulos import productos as p
from modulos import clientes as c
from modulos import facturas as f
from modulos import ventas as v
from conexion import *
import impresora
import events
import sys
import var

from venAviso import *
from venPrincipal import *
from venConfirmacion import *
from venAcercaDe import *


class DialogAviso(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAviso, self).__init__()
        var.dlg_aviso = Ui_ven_aviso()
        var.dlg_aviso.setupUi(self)
        var.dlg_aviso.btn_ok.clicked.connect(self.close)
        var.lbl_mensaje = var.dlg_aviso.lbl_mensaje
        var.lbl_mensaje.setText("Mensaje por defecto")


class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.dlg_salir = Ui_ven_confirmacion()
        var.dlg_salir.setupUi(self)
        var.lbl_pregunta = var.dlg_salir.lbl_pregunta
        var.dlg_salir.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.salir)
        var.lbl_pregunta.setText("")


class DialogBuscador(QtWidgets.QFileDialog):
    def __init__(self):
        super(DialogBuscador, self).__init__()
        self.setWindowTitle('Abrir Archivo')
        self.setModal(True)


class DialogImpresora(QtPrintSupport.QPrintDialog):
    def __init__(self):
        super(DialogImpresora, self).__init__()


class DialogAbout(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAbout, self).__init__()
        var.dlg_aviso = Ui_ven_acercade()
        var.dlg_aviso.setupUi(self)
        var.dlg_aviso.btn_ok.clicked.connect(self.close)


class DialogConfirmarImporte(QtWidgets.QDialog):
    def __init__(self):
        super(DialogConfirmarImporte, self).__init__()
        var.dlg_confirmar_importe = Ui_ven_confirmacion()
        var.dlg_confirmar_importe.setupUi(self)
        self.pregunta = var.dlg_confirmar_importe.lbl_pregunta
        self.filename = ""
        var.dlg_confirmar_importe.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            events.importar_productos)
        var.dlg_confirmar_importe.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.No).clicked.connect(self.close)


def closeEvent(event):
    if event:
        events.salir(event)


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        """

        Crea la instancia del programa con todas las ventanas y conexiones necesarias para que la interfaz principal
        funcione.

        """
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.dlg_about = DialogAbout()
        var.dlg_aviso = DialogAviso()
        var.dlg_salir = DialogSalir()
        var.dlg_buscador = DialogBuscador()
        var.dlg_imprimir = DialogImpresora()
        var.dlg_confirmar_importe = DialogConfirmarImporte()

        var.ui.action_menu_salir.triggered.connect(events.salir)
        var.ui.action_salir.triggered.connect(events.salir)

        var.ui.action_recuperar.triggered.connect(events.recuperar_copia)
        var.ui.action_menu_recuperar.triggered.connect(events.recuperar_copia)

        var.ui.action_backup.triggered.connect(events.copia_seguridad)
        var.ui.action_menu_backup.triggered.connect(events.copia_seguridad)

        var.ui.action_importar_productos.triggered.connect(events.seleccion_fichero_productos)
        var.ui.action_impresora.triggered.connect(events.abrir_impresora)
        var.ui.action_about.triggered.connect(events.about)
        var.ui.action_i_clientes.triggered.connect(impresora.Printer.informe_cliente)
        var.ui.action_i_productos.triggered.connect(impresora.Printer.informe_productos)
        var.ui.action_i_facturas.triggered.connect(impresora.Printer.informe_facturas)
        var.ui.action_i_fac_cliente.triggered.connect(impresora.Printer.informe_facturas_cliente)
        var.ui.statusbar.addPermanentWidget(var.ui.lbl_status, 1)
        var.ui.lbl_status.setText('Buenos Días')

        conexion = db_connect(var.filebd)
        if not conexion:
            sys.exit()

        c.Clientes.crear_modulo()
        p.Productos.crear_modulo()
        f.Facturas.crear_modulo()
        v.Ventas.crear_modulo()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    window.setWindowTitle("BARREIROCHAPELA")
    window.setWindowIcon(QIcon("res/icono.ico"))
    sys.exit(app.exec())
