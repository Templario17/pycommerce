from os import environ

from config import *

URI = environ['REQUEST_URI']
API = True if URI.startswith('/api') else False
URL_LIST = environ.get('REQUEST_URI', '/')[1:].split('/')


if API:
    URL_LIST[0].replace('api', '')
    MODULE = URL_LIST[1].replace('.', '')
    PACKAGE = "modules.{}".format(MODULE)
    MODULE_PATH = "{}.py".format(PACKAGE.replace('.', '/'))
    CONTROLLER = "{}Controller".format(MODULE.title())
    RESOURCE = URL_LIST[2] if len(URL_LIST) > 2 else ''
    ARG = URL_LIST[3] if len(URL_LIST) > 3 else 0
else:
    MODULE = URL_LIST[0].replace('.', '')
    PACKAGE = "modules.{}".format(MODULE)
    MODULE_PATH = "{}.py".format(PACKAGE.replace('.', '/'))
    CONTROLLER = "{}Controller".format(MODULE.title())
    RESOURCE = URL_LIST[1] if len(URL_LIST) > 1 else ''
    ARG = URL_LIST[2] if len(URL_LIST) > 2 else 0

ARG = int(ARG)
HTTP_404 = "Status: 404 Not Found"
HTTP_HTML = "Content-type: text/html; charset=utf-8"
HOST = "http://{}".format(environ.get('SERVER_NAME', 'localhost'))
HTTP_REDIRECT = "Location: {}{}".format(HOST, DEFAULT_RESOURCE)
