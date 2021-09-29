from base64 import b64encode
from subprocess import Popen, PIPE
from string import Template

from config import STATIC_DIR
from common.helpers import show, get_html, redirect


class HomeView(object):
    
    @staticmethod
    def show_img(self):
        ruta = "{}/img/servilet.ico".format(STATIC_DIR)
        cmd = ['file', '--mime-type', ruta]
        process = Popen(cmd, stdout=PIPE)
        mime = process.stdout.read().decode('utf-8')
        mime = mime.split(': ')[1].replace('/n', '')
        
        with open(ruta, 'rb') as f:
            image = f.read()
        contenido = b64encode(image).decode('utf-8')
        
        show("<img src='data: {}; base64,{}'>".format(mime, contenido))
        
    def index(self):
        html = get_html('template')
        inner = get_html('home') 
        html = Template(html).safe_substitute(contenido=inner)
        show(html)
    


class HomeController(object):
    
    def __init__(self, api):
        self.api = api
        self.view = HomeView()
        
    def index(self):
        self.view.index()

