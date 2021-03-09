from PyQt5 import QtSql, QtWidgets


def db_connect(filename):
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName(filename)
    if not db.open():
        QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos',
                                       'No se puede establecer conexion.\n'
                                       'Haz Click para Cancelar.', QtWidgets.QMessageBox.Cancel)
        return False
    return True
