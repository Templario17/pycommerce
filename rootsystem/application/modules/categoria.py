from cgi import FieldStorage
from string import Template
from base64 import b64encode
from re import compile
from os.path import isfile
from subprocess import Popen, PIPE
import json

from common.helpers import show, get_html, redirect, show_json, ajax
from core.api import APIRESTFul
from core.collector import Collector
from core.db import DBQuery
from settings import ARG, PRIVATE_DIR
from modules.producto import Producto



class Categoria(object):
    
    def __init__(self):
        self.categoria_id = 0
        self.denominacion = ""
        self.producto_collection = [] #propiedad collectora de productos

        
    def insert(self):
        sql = """INSERT INTO categoria(denominacion)
                 VALUES('{}')""".format(self.denominacion)
        self.categoria_id = DBQuery().execute(sql)
        
    def update(self):
        pass
    
    def select(self):
        #TODO implementar get_auxiliar para objeto colector 
        sql = """SELECT denominacion 
                 FROM categoria 
                 WHERE categoria_id={}""".format(self.categoria_id)
        
        resultado = DBQuery().execute(sql)[0]
        self.denominacion = resultado[0]
        
        productos = Producto().get_producto(self.categoria_id)
        for compositor in productos:
            p = Producto()
            p.producto_id = compositor[0]
            p.select()
            self.producto_collection.append(p)
                
        
        
class CategoriaView(object):

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
            etiqueta = """src="https://dummyimage.com/{}/dee2e6/6c757d.jpg" 
                        alt="..." """.format(longitud)
            return etiqueta
    
    def agregar(self):
        html = get_html('template')
        inner = get_html('categoria_agregar')
        html = Template(html).safe_substitute(contenido=inner)
        show(html)
        
    def guardar(self):
        show('Datos Guardados !')
        
    def listar(self, objetos):
        html = get_html('template')
        inner = get_html('categoria_listar')
        html = Template(html).safe_substitute(contenido=inner)  
        
        regex = compile("<!--select-->(.|\n){1,}<!--select-->")
        busca = regex.search(html).group(0)
        string = []

        for obj in objetos:
            dicc = vars(obj)
            dicc['categoria_id'] = obj.categoria_id
            dicc['denominacion'] = obj.denominacion
            render = Template(busca).safe_substitute(dicc)
            string.append(render)

        render = str("\n".join(string))
        contenido = html.replace(busca, render)

        show(contenido)
        
    def productos(self, objetos):
        html = get_html('categoria_producto')
        regex = compile("<!--lista-->(.|\n){1,}<!--lista-->")
        busca = regex.search(html).group(0)
        string = []
        
        for obj in objetos:
            dicc = vars(obj)
            dicc['imagen'] = CategoriaView().get_image(obj.producto_id, "250x200")
            render = Template(busca).safe_substitute(dicc)
            string.append(render)
        
        render = str("\n".join(string))
        contenido = html.replace(busca, render)
        
        show(contenido)
        

class CategoriaController(object):
    
    def __init__(self, api):
        self.api = api
        self.model = Categoria()
        self.view = CategoriaView()
        
    def agregar(self):
        self.view.agregar()
        
    def guardar(self):
        form = FieldStorage()
        denominacion = form['denominacion'].value
        #TODO falta realizar validaciones
        
        self.model.denominacion = denominacion
        self.model.insert()
        redirect("/categoria/listar")
        
    def listar(self):
        c = Collector()
        c.get('Categoria')
        if self.api is True:
           redirect("/api/producto/listar")
        else:
            self.view.listar(c.coleccion)

    def productos(self):      
        self.model.categoria_id = ARG
        self.model.select()
        
        self.view.productos(self.model.producto_collection)
        
