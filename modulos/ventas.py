from PyQt5 import QtSql


class Ventas:

    @classmethod
    def crear_modulo(cls):
        pass

    @staticmethod
    def db_recoger_codigo_precio(articulo: str):
        """



        :param articulo:
        :type articulo:
        :return:
        :rtype:



        """
        datos = []
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, precio_unidad from articulos where nombre = :articulo')
        query.bindValue(':codfac', articulo)
        if query.exec_():
            while query.next():
                datos = [str(query.value(0)), str(query.value(1))]
        return datos