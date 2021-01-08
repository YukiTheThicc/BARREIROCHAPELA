import conexion
import var
import events


class Productos:

    @staticmethod
    def alta_producto():
        nombre = var.ui.edit_pro_nombre.text()
        precio = var.ui.dspin_pro_precio.value()
        if not nombre == '':
            to_insert = [nombre, precio]
            conexion.Conexion.alta_producto(to_insert)
        else:
            events.Eventos.aviso("Necesita un nombre")

    @staticmethod
    def sel_producto():
        try:
            tupla_elegida = var.ui.tbl_pro_tabla.selectedItems()
            campos_producto = {"nombre": var.ui.edit_pro_nombre, "precio": var.ui.dspin_pro_precio,
                               "codigo": var.ui.lbl_pro_muestra_codigo}
            campos_producto["codigo"].setText(tupla_elegida[0].text())
            campos_producto["nombre"].setText(tupla_elegida[1].text())
            campos_producto["precio"].setValue(float(tupla_elegida[2].text()))
        except Exception as error:
            print('Error en cargarCli: %s ' % str(error))

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
        except Exception as error:
            print('Error en limpiarCliente: %s ' % str(error))

    @staticmethod
    def baja_producto():
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            conexion.Conexion.baja_producto(codigo)
            conexion.Conexion.actualizar_tabla_pro()
            Productos.limpiar_campos()
        except Exception as error:
            print('Error en bajaCliente: %s ' % str(error))

    @staticmethod
    def modif_producto():
        try:
            codigo = var.ui.lbl_pro_muestra_codigo.text()
            newdata = [var.ui.edit_pro_nombre.text(), var.ui.dspin_pro_precio.value()]
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
            print('Error en recargar: %s ' % str(error))

    @staticmethod
    def buscar():
        try:
            nombre = var.ui.lbl_pro_nombre.text()
            if nombre != '':
                conexion.Conexion.buscar_producto(nombre)
            else:
                print('Se ha intentado buscar por un nombre vacio')
        except Exception as error:
            print('Error en buscar producto: %s ' % str(error))
