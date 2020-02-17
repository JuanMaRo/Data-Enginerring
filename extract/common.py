import yaml


__config = None


def config():
    global __config # para usar una variable global dentro de nuestra funcion
    if not __config:
        with open('config.yaml', mode='r') as f:
            __config = yaml.safe_load(f)

    return __config
