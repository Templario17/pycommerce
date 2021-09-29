from core.db import DBQuery
from config import STATIC_DIR


class Precio(object):
    
    def __init__(self):
        self.precio_id = 0
        self.lista = 0.0
        self.oferta = 0.0
    
    def insert(self):
        sql = """INSERT INTO precio (lista, oferta) 
                 VALUES({}, {})""".format(self.lista, self.oferta)
        self.precio_id = DBQuery().execute(sql)


    def select(self):
        sql = """SELECT lista, oferta 
                 FROM precio 
                 WHERE precio_id = {}""".format(self.precio_id)
        resultado = DBQuery().execute(sql)[0]
        
        self.lista = resultado[0]
        self.oferta = resultado[1]
    
    def update(self):
        pass


class PrecioView(object):
    pass


class PrecioController(object):
    
    def __init__(self, api):
        self.api = api
        self.model = Precio()
        self.view = PrecioView()

    def guardar(self, lista, oferta):
        self.model.lista = lista
        self.model.ofeta = oferta
        self.model.insert()

