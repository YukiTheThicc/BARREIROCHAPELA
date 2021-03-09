import unittest
from PyQt5 import QtSql

import conexion
import var

from modulos import productos as p
from modulos import clientes as c
from modulos import facturas as f
from modulos import ventas as v


class MyTestCase(unittest.TestCase):

    def test_conexion(self):
        value = conexion.db_connect(var.filebd)
        msg = 'Conexión no válida'
        self.assertTrue(value, msg)

    def test_dni(self):
        dni = '00000000T'
        value = c.Clientes.validar_dni(str(dni))
        msg = 'Proba Errónea'
        self.assertTrue(value, msg)

"""    def test_fact(self):
        valor = 40.02
        codfac = 91
        try:
            msg = 'Cálculos incorrectos'
            var.subfac = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad from ventas where codfacventa = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                while query.next():
                    codarticventa = query.value(1)
                    cantidad = query.value(2)
                    query1.prepare('select producto, precio from productos where codigo = :codarticventa')
                    query1.bindValue(':codarticventa', int(codarticventa))
                    if query1.exec_():
                        while query1.next():
                            precio = query1.value(1)
                            subtotal = round(float(cantidad) * float(precio), 2)
                    var.subfac = round(float(subtotal) + float(var.subfac), 2)
            var.iva = round(float(var.subfac) * 0.21, 2)
            var.fac = round(float(var.iva) + float(var.subfac), 2)
        except Exception as error:
            print('Error Listado de la tabla de ventas: %s ' % str(error))
        self.assertEqual(round(float(valor), 2), round(float(var.fac), 2), msg)"""


if __name__ == '__main__':
    unittest.main()
