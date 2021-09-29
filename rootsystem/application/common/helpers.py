#!/usr/bin/env python3
from string import digits
from random import choice

from config import STATIC_DIR
from settings import HOST


def show(content=""):
    print("Content-Type: text/html; coding:utf-8")
    print("")
    print(content)
    
def get_html(nombre):
    with open("{}/{}.html".format(STATIC_DIR, nombre)) as f:
        html = f.read()
    return html
    
def redirect(recurso):
    print("Content-type: text/html; charset=utf-8")
    print("Location: {}{}".format(HOST, recurso))
    print("")


def show_json(content=""):
    print("Content-type: application/json; charset=utf-8")
    print("Access-Control-Allow-Origin: *")
    print("")
    print(content)
    
def ajax(content=""):
    print("Content-type: text/html; Charset=utf-8")
    print("Access-Control-Allow-Origin: *")
    print("")
    print(content)
    
    
def get_sku(categoria, denominacion):
    l = 4
    chars = digits
    a = denominacion[:3].upper()
    cod = ''.join(choice(chars) for _ in range(l))
    sku = "ID{}{}{}".format(categoria, a, cod)
    return sku
  
