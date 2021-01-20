import sys


from ventanas.venPrincipal import *
from ventanas.venAcercaDe import *

from modulos.productos import prep_productos as p
from modulos.clientes import clients as c

import dialogs as d
import impresora
import conexion
import events
import var

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.dlgAbout = d.DialogAbout()
        var.dlgAviso = d.DialogAviso()
        var.dlgSalir = d.DialogSalir()

        var.dlgBuscador = d.DialogBuscador()
        var.dlgImprimir = d.DialogImpresora()
        var.dni_valido = False

        # Arrays con los botones chk y rbt
        var.rbtSex = (var.ui.rbt_fem, var.ui.rbt_mas)
        var.chkPago = (var.ui.chk_efect, var.ui.chk_tarje, var.ui.chk_trans)

        var.ui.statusbar.addPermanentWidget(var.ui.lbl_status, 1)
        var.ui.lbl_status.setText('Buenos Días')

        var.ui.actionsalir.triggered.connect(events.Eventos.salir)
        var.ui.actionBuscador.triggered.connect(events.Eventos.abrir_buscador)
        var.ui.actionImpresora.triggered.connect(events.Eventos.abrir_impresora)

        # --------------------------- PARA EXAMEN -------------------------
        p.PrepProductos.crear_conexiones()

        var.ui.action_about.triggered.connect(events.Eventos.about)
        # --------------------------- FIN DE PARA EXAMEN -------------------------

        # --------------------------- PARA INFORMES ---------------------------
        var.ui.action_i_clientes.triggered.connect(impresora.Printer.informe_cliente)
        var.ui.action_i_productos.triggered.connect(impresora.Printer.informe_productos)
        # --------------------------- FIN DE PARA INFORMES ---------------------------

        # Conexion con la base de datos
        conexion.Conexion.db_connect(var.filebd)
        # Muestra en la tabla los clientes guardados en la base de datos
        conexion.Conexion.mostrar_clientes()
        conexion.Conexion.actualizar_tabla_pro()

    def closeEvent(self, event):
        if event:
            events.Eventos.salir(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
