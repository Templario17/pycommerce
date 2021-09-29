from string import Template

from core.db import DBQuery
from common.helpers import get_html, show
from config import STATIC_DIR


class Pedido(object):
    
    def __init__(self):
        self.pedido_id = 0
        self.cliente = 0  #propiedad de dependecia
        self.fecha = ""
        self.estado = 0
        self.producto_collection = []
        
    def insert(self):
        pass
        
    def select(self):
        pass
        
    def update(self):
        pass
    
    def delete(self):
        pass


class PedidoView(object):
    
    def listar(self):
        html = get_html('template')
        inner = get_html('pedido_listar')
        html = Template(html).safe_substitute(contenido=inner)
        show(html)
    
    
class PedidoController(object):
    
    def __init__(self, api):
        self.api = api
        self.model = Pedido()
        self.view = PedidoView()
        
    def listar(self):
        self.view.listar()
        
        
    
