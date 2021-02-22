from PyQt5 import QtSql
import var
from venPrincipal import *


class Conexion():

    @staticmethod
    def db_connect(filename):
        '''
        Conexion con la base de datos tipo sqlite.
        :param filename:
        :return:
        '''
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
