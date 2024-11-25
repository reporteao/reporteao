import tomllib

def cargar_configuracion(archivo):
    data = None
    with open(archivo, "rb") as f:
        data = tomllib.load(f)
    return data
