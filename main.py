from PyQt5 import QtPrintSupport, QtSql

from modulos import productos as p
from modulos import clientes as c
from modulos import facturas as f
from modulos import ventas as v
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
        var.dlgAviso = Ui_ven_aviso()
        var.dlgAviso.setupUi(self)
        var.dlgAviso.btn_ok.clicked.connect(self.close)
        var.lbl_mensaje = var.dlgAviso.lbl_mensaje
        var.lbl_mensaje.setText("Mensaje por defecto")


class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.dlgSalir = Ui_ven_confirmacion()
        var.dlgSalir.setupUi(self)
        var.lbl_pregunta = var.dlgSalir.lbl_pregunta
        var.dlgSalir.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.salir)
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
        var.dlgAviso = Ui_ven_acercade()
        var.dlgAviso.setupUi(self)
        var.dlgAviso.btn_ok.clicked.connect(self.close)


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.dlgAbout = DialogAbout()
        var.dlgAviso = DialogAviso()
        var.dlgSalir = DialogSalir()
        var.dlgBuscador = DialogBuscador()
        var.dlgImprimir = DialogImpresora()

        var.ui.actionSalir.triggered.connect(events.Eventos.salir)
        var.ui.actionsalir.triggered.connect(events.Eventos.salir)
        var.ui.actionBuscador.triggered.connect(events.Eventos.abrir_buscador)
        var.ui.actionImpresora.triggered.connect(events.Eventos.abrir_impresora)
        var.ui.action_about.triggered.connect(events.Eventos.about)
        var.ui.action_i_clientes.triggered.connect(impresora.Printer.informe_cliente)
        var.ui.action_i_productos.triggered.connect(impresora.Printer.informe_productos)
        var.ui.action_i_facturas.triggered.connect(impresora.Printer.informe_facturas)
        var.ui.action_i_fac_cliente.triggered.connect(impresora.Printer.informe_facturas_cliente)
        var.ui.statusbar.addPermanentWidget(var.ui.lbl_status, 1)
        var.ui.lbl_status.setText('Buenos Días')

        self.db_connect(var.filebd)

        c.Clientes.crear_modulo()
        p.Productos.crear_modulo()
        f.Facturas.crear_modulo()
        v.Ventas.crear_modulo()

    @staticmethod
    def db_connect(filename):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filename)
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos',
                                           'No se puede establecer conexion.\n'
                                           'Haz Click para Cancelar.', QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexión Establecida')
        return True

    def closeEvent(self, event):
        if event:
            events.Eventos.salir(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
