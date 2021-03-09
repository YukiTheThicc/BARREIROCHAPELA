import unittest

from conexion import *
import var

from modulos import clientes as c


class MyTestCase(unittest.TestCase):

    def test_conexion(self):
        value = db_connect(var.filebd)
        msg = 'Conexión no válida'
        self.assertTrue(value, msg)

    def test_dni(self):
        dni = '00000000T'
        value = c.Clientes.validar_dni(str(dni))
        msg = 'Proba Errónea'
        self.assertTrue(value, msg)


if __name__ == '__main__':
    unittest.main()
