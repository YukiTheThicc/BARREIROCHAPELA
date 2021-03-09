import os
import shutil
import sys
import zipfile
import xlrd
from datetime import datetime

from conexion import *
from modulos import productos as p
from modulos import clientes as c
from modulos import facturas as f

import var


def salir(event):
    """

    Lanza una ventana de confirmación para salir del programa.

    :return: None

    Si cancela no hace nada, y si acepta sale de la aplicación.

    """
    try:
        var.dlg_salir.show()
        var.lbl_pregunta.setText("Seguro/a que quiere salir?")
        if var.dlg_salir.exec_():
            sys.exit()
        else:
            var.dlg_salir.close()
            event.ignore()
    except Exception as error:
        print('Error en salir: %s' % str(error))


def abrir_buscador():
    """

    Abre la ventana de diálogo del buscador de archivos.

    :return: None

    """
    try:
        var.dlg_buscador.show()
    except Exception as error:
        print('Error en abrir_buscador: %s ' % str(error))


def abrir_impresora():
    """

    Abre la ventana de diálogo de impresora

    :return: None

    """
    try:
        var.dlg_imprimir.setWindowTitle('Imprimir')
        var.dlg_imprimir.setModal(True)
        var.dlg_imprimir.show()
    except Exception as error:
        print('Error en abrir_impresora: %s ' % str(error))


def aviso(mensaje: str):
    """

    Lanza una ventana de aviso con el mensaje que se le pase como parámetro

    :return: None

    """
    try:
        var.dlg_aviso.show()
        var.lbl_mensaje.setText(mensaje)
    except Exception as error:
        print('Error en aviso: %s' % str(error))


def about():
    """

    Lanza una ventana con la información acerca de.

    :return: None

    """
    try:
        var.dlg_about.show()
    except Exception as error:
        print('Error en about: %s' % str(error))


def copia_seguridad():
    """

    Método que hace una copia de seguridad.

    :return: None

    Recoge la fecha y hora del momento de hacer la copia, y abre la ventana del navegador de archivos. Si el usuario
    selecciona una ruta en el navegador de archivos para hacer la copia, procede a hacer la copia en archivo .zip y la
    mueve al directorio seleccionado por el usuario.

    """
    try:
        fecha = datetime.today()
        fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
        copia = (str(fecha) + '_backup.zip')
        option = QtWidgets.QFileDialog.Options()
        directorio, filename = var.dlg_buscador.getSaveFileName(None, 'Guardar Copia', copia, '.zip', options=option)
        if var.dlg_buscador.Accepted and filename != '' and copia is not None:
            fichzip = zipfile.ZipFile(copia, 'w')
            fichzip.write(var.filebd, os.path.basename(var.filebd), zipfile.ZIP_DEFLATED)
            fichzip.close()
            var.ui.lbl_status.setText('Copia de seguridad creada en ' + directorio)
            shutil.move(str(copia), str(directorio))
    except Exception as error:
        print('Error en copia_seguridad: %s' % str(error))


def recuperar_copia():
    """

    Método que restaura una copia de seguridad en la base de datos.

    :return: None

    Abre una ventana de diálogo del navegador de archivos para que el usuario seleccione un .zip de una backup de la
    base de datos. Si ha seleccionado un archivo, extrae los datos de dicho archivo en la base de datos y actualiza las
    tablas de los módulos.

    """
    try:
        option = QtWidgets.QFileDialog.Options()
        filename = var.dlg_buscador.getOpenFileName(None, 'Restaurar Copia de Seguridad', '', '*.zip;;All Files',
                                                    options=option)
        if var.dlg_buscador.Accepted and filename[0] != '':
            file = filename[0]
            with zipfile.ZipFile(str(file), 'r') as bbdd:
                bbdd.extractall(pwd=None)
            bbdd.close()
            db_connect(var.filebd)
            c.Clientes.db_mostrar_clientes()
            p.Productos.db_actualizar_tabla_pro()
            f.Facturas.db_mostrar_facturas()
            var.ui.lbl_status.setText('Se ha restaurado la base de datos desde: ' + filename[0])
    except Exception as error:
        print('Error en recuperar_copia: %s ' % str(error))


def seleccion_fichero_productos():
    """

    Método que permite al usuario abrir un .xls para importar datos.

    :return: None

    Abre una ventana de diálogo del navegador de archivos para que el usuario seleccione un .xls para importar datos. A
    continuación se le pide confirmación al usuario para importar los datos del archivo. Los datos de la ruta del
    fichero los guarda dentro de la ventana de confirmación para que la función de importar sepa donde está el archivo.

    """
    try:
        option = QtWidgets.QFileDialog.Options()
        filename = var.dlg_buscador.getOpenFileName(None, 'Importar datos', '', '*.xls;;All Files',
                                                    options=option)
        if var.dlg_buscador.Accepted and filename[0] != '':
            var.dlg_confirmar_importe.pregunta.setText("¿Esta seguro/a de importar estos datos?")
            var.dlg_confirmar_importe.filename = filename[0]
            var.dlg_confirmar_importe.show()
    except Exception as error:
        print('Error en seleccion_fichero_productos: %s ' % str(error))


def importar_productos():
    """

    Método que importa productos de un fichero .xls en la tabla de productos.

    :return: None

    Recupera la ruta del archivo de la ventana de confirmación, y si no está vacía, lee el .xls y recoge los datos de
    cada fila en un array que le pasa a la función de Productos de importar_producto, la cual se encargará de gestionar
    si el producto es nuevo o ya existe.

    """
    try:
        filename = var.dlg_confirmar_importe.filename
        if filename is not None and filename != "":
            documento = xlrd.open_workbook(filename)
            datos_productos = documento.sheet_by_index(0)
            n_productos = datos_productos.nrows
            for i in range(1, n_productos):
                datos_fila = datos_productos.row(i)
                datos = [datos_fila[0].value, datos_fila[1].value, int(datos_fila[2].value)]
                p.Productos.importar_producto(datos)
            var.ui.lbl_status.setText('Se han importado datos desde: ' + filename)
            p.Productos.db_actualizar_tabla_pro()
    except Exception as error:
        print('Error en importar_productos: %s ' % str(error))
