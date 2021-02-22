import conexion
import var
import events
from venConfirmacion import *


class DialogEliminarProducto(QtWidgets.QDialog):
    def __init__(self):
        super(DialogEliminarProducto, self).__init__()
        Productos.dlgEliminarProducto = Ui_ven_confirmacion()
        Productos.dlgEliminarProducto.setupUi(self)
        self.pregunta = Productos.dlgEliminarProducto.lbl_pregunta
        Productos.dlgEliminarProducto.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(Productos.baja_producto)
        Productos.dlgEliminarProducto.btnbox_confirmar.button(QtWidgets.QDialogButtonBox.No).clicked.connect(self.close)


class Productos:

    dlgEliminarProducto = None

    @classmethod
    def crear_modulo(cls):
        cls.dlgEliminarProducto = DialogEliminarProducto()

        # Salir
        var.ui.btn_pro_salir.clicked.connect(events.Eventos.salir)
        # Alta
        var.ui.btn_pro_guardar.clicked.connect(Productos.alta_producto)
        # Seleccionar de la tabla
        var.ui.tbl_pro_tabla.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tbl_pro_tabla.clicked.connect(Productos.sel_producto)
        # Eliminar
        var.ui.btn_pro_eliminar.clicked.connect(Productos.eliminar_producto)
        # Limpiar
        var.ui.btn_pro_limpiar.clicked.connect(Productos.limpiar_campos)
        # Modificar
        var.ui.btn_pro_modificar.clicked.connect(events.Eventos.modificar_producto)
        # Recargar
        var.ui.btn_pro_recargar.clicked.connect(Productos.recargar)

    @staticmethod
    def alta_producto():
        nombre = var.ui.edit_pro_nombre.text()
        precio = var.ui.dspin_pro_precio.value()
        stock = var.ui.spin_pro_stock.value()
        if not nombre == '':
            to_insert = [nombre, precio, stock]
            conexion.Conexion.alta_producto(to_insert)
        else:
            events.Eventos.aviso("Necesita un nombre")

    @staticmethod
    def sel_producto():
        try:
            tupla_elegida = var.ui.tbl_pro_tabla.selectedItems()
            campos_producto = {"nombre": var.ui.edit_pro_nombre, "precio": var.ui.dspin_pro_precio,
                               "codigo": var.ui.lbl_pro_muestra_codigo, "stock": var.ui.spin_pro_stock}
            campos_producto["codigo"].setText(tupla_elegida[0].text())
            campos_producto["nombre"].setText(tupla_elegida[1].text())
            campos_producto["precio"].setValue(float(tupla_elegida[2].text()))
            campos_producto["stock"].setValue(int(tupla_elegida[3].text()))
        except Exception as error:
            print('Error en sel_producto: %s ' % str(error))

    @staticmethod
    def limpiar_campos():
        '''
        limpia los datos del formulario cliente
        :return: none
        '''
        try:
            var.ui.edit_pro_nombre.setText('')
            var.ui.lbl_pro_muestra_codigo.setText('')
            var.ui.dspin_pro_precio.setValue(0.01)
            var.ui.edit_pro_stock.setValue(0)
        except Exception as error:
            print('Error en limpiar_producto: %s ' % str(error))

    @classmethod
    def eliminar_producto(cls):
        """
        Funcion para llamar al dialogo de confirmacion y recoger el resultado
        :return:
        """
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            if codigo != '':
                cls.dlgEliminarProducto.show()
                cls.dlgEliminarProducto.pregunta.setText("Esta seguro/a que quiere borrar\n"
                                                         "este producto?")
            else:
                events.Eventos.aviso("Seleccione un producto")
        except Exception as error:
            print('Error: %s' % str(error))

    @staticmethod
    def baja_producto():
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            conexion.Conexion.baja_producto(codigo)
            conexion.Conexion.actualizar_tabla_pro()
            Productos.limpiar_campos()
        except Exception as error:
            print('Error en baja_producto: %s ' % str(error))

    @staticmethod
    def modif_producto():
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            newdata = [var.ui.edit_pro_nombre.text(), var.ui.dspin_pro_precio.value(), var.ui.spin_pro_stock.value()]
            conexion.Conexion.modif_producto(codigo, newdata)
            conexion.Conexion.actualizar_tabla_pro()
        except Exception as error:
            print('Error en modif_producto productos: %s ' % str(error))

    @staticmethod
    def recargar():
        try:
            Productos.limpiar_campos()
            conexion.Conexion.actualizar_tabla_pro()
            print('Recargando...')
        except Exception as error:
            print('Error en recargar_producto: %s ' % str(error))

    @staticmethod
    def buscar():
        try:
            nombre = var.ui.lbl_pro_nombre.text()
            if nombre != '':
                conexion.Conexion.buscar_producto(nombre)
            else:
                print('Se ha intentado buscar por un nombre vacio')
        except Exception as error:
            print('Error en buscar_producto: %s ' % str(error))
