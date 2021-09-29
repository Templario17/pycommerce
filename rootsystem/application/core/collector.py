from core.db import DBQuery
from settings import PACKAGE


class Collector(object): 

    def __init__(self):
        self.coleccion = []

    def get(self, clase):
        sql = "SELECT {c}_id FROM {c}".format(c=clase.lower())
        pids = DBQuery().execute(sql)
        
        modulo = __import__(PACKAGE, fromlist=[clase])
        
        for pid in pids:
            modelo = getattr(modulo, clase)()
            vars(modelo)["{}_id".format(clase.lower())] = pid[0]
            modelo.select()
            self.coleccion.append(modelo)
