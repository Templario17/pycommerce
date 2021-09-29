from os import environ
from json import loads

#TODO configurar variables para produccion
with open('secret.json') as f:
    secret = loads(f.read())

def get_secrets(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = 'la variable {} no existe !'.format(secret_name)
        raise msg

DB_HOST = "localhost"
DB_USER = get_secrets("DB_USER")
DB_PASS = get_secrets("DB_PASS")
DB_NAME = get_secrets("DB_NAME")
PRIVATE_DIR = get_secrets("PRIVATE_DIR")

DEFAULT_RESOURCE = "/producto/catalogo"
SHOW_ERROR_404 = False
ROOT_DIR = environ.get("DOCUMENT_ROOT", "/home/daniel/Proyectos/pycommerce/rootsystem")
STATIC_DIR = "{}/static".format(ROOT_DIR)
