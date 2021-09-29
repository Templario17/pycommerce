from base64 import b64encode
from subprocess import Popen, PIPE
from cgi import FieldStorage
from os.path import isfile
from re import compile
from string import Template
import json

from core.db import DBQuery
from core.api import APIRESTFul
from core.collector import Collector
from common.helpers import show, get_html, get_sku, show_json, redirect
#from modules.categoria import Categoria
from settings import ARG, PRIVATE_DIR



class Producto(object):
    
    def __init__(self):
        self.producto_id = 0
        self.denominacion = ''
        self.descripcion = ''
        self.precio_lista = 0.0
        self.precio_oferta = 0.0
        self.sku = ""
        self.categoria = 0 #propiedad de dependencia
    
    @staticmethod
    def get_producto(categoria_id):
        sql = """SELECT producto_id FROM producto WHERE categoria={}""".format(
                categoria_id)
        return DBQuery().execute(sql)

    def insert(self):
        sql = """INSERT INTO producto
                            (denominacion, descripcion, precio_lista, precio_oferta, sku, categoria)
                VALUES("{}", "{}", {}, {}, "{}", {})
        """.format(
            self.denominacion,
            self.descripcion, 
            self.precio_lista,
            self.precio_oferta,
            self.sku,
            self.categoria
        )
        self.producto_id = DBQuery().execute(sql)

    def update(self):
        sql = """UPDATE producto
                 SET denominacion = '{}', 
                     descripcion = '{}', 
                     precio_lista = {},
                     precio_oferta = {}
                 WHERE producto_id = {}""".format(
                 self.denominacion,
                 self.descripcion,
                 self.precio_lista,
                 self.precio_oferta,
                 self.producto_id)
        
        DBQuery().execute(sql)
        
    def select(self):
        sql = """SELECT denominacion, descripcion, precio_lista, precio_oferta, sku, categoria
                 FROM producto
                 WHERE producto_id = {}""".format(self.producto_id)
        
        resultado = DBQuery().execute(sql)[0]
        
        self.denominacion = resultado[0]
        self.descripcion = resultado[1]
        self.precio_lista = float(resultado[2])
        self.precio_oferta = float(resultado[3])
        self.sku = resultado[4]
        self.categoria = resultado[5]
        
        
    def delete(self):
        sql = """DELETE FROM producto WHERE producto_id = {}""".format(
            self.producto_id)
        DBQuery().execute(sql)      
        
class ProductoView(object):
    
    @staticmethod
    def get_image(producto_id, longitud):
        ruta = "{}/producto/{}.jpeg".format(PRIVATE_DIR, producto_id)
        if isfile(ruta):
            cmd = ['file', '--mime-type', ruta]
            process = Popen(cmd, stdout=PIPE)
            mime = process.stdout.read().decode('utf-8')
            mime = mime.split(': ')[1].replace('/n', '')
            
            with open(ruta, 'rb') as f:
                image = f.read()
                
            contenido = b64encode(image).decode('utf-8')
            etiqueta = """
                    src='data: {}; base64, {}'""".format(mime, contenido)
            return etiqueta
         
        else:
            etiqueta = """
                src="https://dummyimage.com/{}/dee2e6/6c757d.jpg" 
                alt="..." 
            """.format(longitud)
            return etiqueta
    
    def catalogo(self, objetos):
        html = get_html('template')
        inner = get_html('producto_listar')
        html = Template(html).safe_substitute(contenido=inner)
        
        regex = compile("<!--producto-->(.|\n){1,}<!--producto-->")
        busca = regex.search(html).group(0)
        string = []
        
        for obj in objetos:
            dicc = vars(obj)
            dicc['imagen'] = ProductoView().get_image(obj.producto_id, "450x300") 
            render = Template(busca).safe_substitute(dicc)
            string.append(render)
            
        render = str("\n".join(string))
        contenido = html.replace(busca, render)
        show(contenido)
        
    def ver(self, objeto):
        dicc = vars(objeto)
        img = ProductoView().get_image(objeto.producto_id, "600x700")
        dicc['imagen'] = img
        
        html = get_html('template')
        inner = get_html('producto_ver')
        render = Template(inner).safe_substitute(dicc)       
        html = Template(html).safe_substitute(contenido=render)
        show(html)
        
    def pedido(self):
        html = get_html('template')
        inner = get_html('carrito_compras')
        html = Template(html).safe_substitute(contenido=inner)
        show(html)

    def agregar(self):
        html = get_html('template')
        inner = get_html('producto_agregar')
        html = Template(html).safe_substitute(contenido=inner)
        
        show(html)
   
    def listar(self, objetos):
        pass
        
    def inventario(self, productos):
        html = get_html('template')
        inner = get_html('producto_inventario')
        html = Template(html).safe_substitute(contenido=inner)
        
        regex = compile("<!--lista-->(.|\n){1,}<!--lista-->")
        busca = regex.search(html).group(0)
        string = []
        
        for obj in productos:
            dicc = vars(obj)
            dicc['imagen'] = ProductoView().get_image(obj.producto_id, "60x60")
            render = Template(busca).safe_substitute(dicc)
            string.append(render)
            
        render = str("\n".join(string))
        contenido = html.replace(busca, render)
        show(contenido)
        
    def editar(self, objeto):
        html = get_html('template') 
        inner = get_html('producto_editar')
        html = Template(html).safe_substitute(contenido=inner)
        
        dicc = vars(objeto)
        dicc['imagen'] = ProductoView().get_image(objeto.producto_id, "450x300")
        render = Template(html).safe_substitute(dicc)
                              
        show(render)
        
        
class ProductoController(object):
    
    def __init__(self, api):
        self.api = api
        self.model = Producto()
        self.view = ProductoView()
        
    def catalogo(self):
        self.view.catalogo()
        
    def ver(self):
        self.model.producto_id = ARG
        self.model.select()
        if self.api is True:
            show_json(APIRESTFul(self.model).json_data)
        else:
            self.view.ver(self.model)
        
    def pedido(self):
        self.view.pedido()

    def agregar(self):
        self.view.agregar()

    def guardar(self):
        form = FieldStorage()
        denominacion = form['denominacion'].value
        descripcion = form['descripcion'].value
        lista = form['lista'].value
        oferta = form['oferta'].value
        categoria = form['categoria'].value
        imagen = form['imagen'].value
        
        try:
            lista = float(lista)
            oferta = float(oferta)
        except:
            lista = 0.0
            oferta = 0.0
            
        if not oferta < lista:
            oferta = lista

        self.model.denominacion = denominacion
        self.model.descripcion = descripcion
        self.model.precio_lista = lista
        self.model.precio_oferta = oferta
        self.model.categoria = categoria
        self.model.sku = get_sku(self.model.categoria, denominacion)
     
        self.model.insert()
        
        if not len(imagen) == 0:
            ruta= "{}producto/{}.jpeg".format(PRIVATE_DIR, self.model.producto_id)
            with open(ruta, 'wb') as f:
                f.write(imagen)
        
        redirect("/producto/inventario")
    
    def listar(self): 
        c = Collector()
        c.get("Producto")
        
        if self.api is True:
            data = []
            for i in c.coleccion:
                data.append(APIRESTFul(i).json_data)
            show_json(json.dumps(data))
        else:
            self.view.catalogo(c.coleccion)
            
    def inventario(self):
        c = Collector()
        c.get('Producto')
        
        self.view.inventario(c.coleccion)
        
    def eliminar(self):
        self.model.producto_id = ARG
        self.model.delete()
        if self.api is True:
            show_json('{"status":"200", "msg": "OK"}')
        else:
            redirect("/producto/listar")
            
    def editar(self):
        self.model.producto_id = ARG
        self.model.select()
        
        self.view.editar(self.model)
        
    def actualizar(self):
        form = FieldStorage()
        
        producto_id = form['producto_id'].value
        denominacion = form['denominacion'].value
        descripcion = form['descripcion'].value
        lista = form['precio_lista'].value
        oferta = form['precio_oferta'].value
        imagen = form['imagen'].value
        
        if not len(imagen) == 0:
            ruta= "{}producto/{}.jpeg".format(PRIVATE_DIR, producto_id)
            with open(ruta, 'wb') as f:
                f.write(imagen)
        
        self.model.producto_id = producto_id
        self.model.denominacion = denominacion
        self.model.descripcion = descripcion
        self.model.precio_lista = lista
        self.model.precio_oferta = oferta
        
        
        self.model.update()
        
        redirect('/producto/ver/{}'.format(self.model.producto_id))
       
        
        
        
        
        

