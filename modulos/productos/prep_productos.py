import var
import events
from modulos.productos import productos as p

from ventanas.venConfirmacion import *


class DialogEliminarProducto(QtWidgets.QDialog):
    def __init__(self):
        super(DialogEliminarProducto, self).__init__()
        var.dlgEliminarProducto = Ui_ven_confirmacion()
        var.dlgEliminarProducto.setupUi(self)
        self.pregunta = var.dlgEliminarProducto.lbl_pregunta
        var.dlgEliminarProducto.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(p.Productos.baja_producto)
        var.dlgEliminarProducto.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.No).clicked.connect(self.close)


class PrepProductos:

    @staticmethod
    def crear_conexiones():
        var.dlgEliminarProducto = DialogEliminarProducto()

        # Salir
        var.ui.btn_pro_salir.clicked.connect(events.Eventos.salir)
        # Alta
        var.ui.btn_pro_guardar.clicked.connect(p.Productos.alta_producto)
        # Seleccionar de la tabla
        var.ui.tbl_pro_tabla.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tbl_pro_tabla.clicked.connect(p.Productos.sel_producto)
        # Eliminar
        var.ui.btn_pro_eliminar.clicked.connect(events.Eventos.eliminar_producto)
        # Limpiar
        var.ui.btn_pro_limpiar.clicked.connect(p.Productos.limpiar_campos)
        # Modificar
        var.ui.btn_pro_modificar.clicked.connect(events.Eventos.modificar_producto)
        # Recargar
        var.ui.btn_pro_recargar.clicked.connect(p.Productos.recargar)
