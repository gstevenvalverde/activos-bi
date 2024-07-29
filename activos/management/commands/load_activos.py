import requests
from activos.models import Activos

def fetch_activos_from_api():
    url = "http://18.191.146.66:8080/graphql"
    query = """
    {
       allActivos {
            id
            nombre
            estado
            etiqueta
            fechaCompra
            serial
            ultimaAsignacion
            ultimaDesasignacion
            valorActual
            valorCompra
            asignadoA {
            nombre
            }
            modelo {
            nombre
            fabricante {
                nombre
            }
            categoria {
                nombre
            }
            }
            ubicacion {
            nombre
            }
            depreciacion {
            nombre
            }
        }
    }
    """
    response = requests.post(url, json={'query': query})
    if response.status_code == 200:
        return response.json()['data']['allActivos']
    else:
        raise Exception(f"Query failed with status code {response.status_code}")

def load_activos():
    
    Activos.objects.all().delete()
    
    activos_data = fetch_activos_from_api()
    objetos_activos = []
    for activo in activos_data:
        modelo_data = activo['modelo']
        fabricante_nombre = modelo_data['fabricante']['nombre']
        categoria_nombre = modelo_data['categoria']['nombre']
        ubicacion_nombre = activo['ubicacion']['nombre']
        depreciacion_nombre = activo['depreciacion']['nombre']
        
        activo_instance = Activos(
            id=activo['id'],
            nombre=activo['nombre'],
            serial=activo['serial'],
            estado=activo['estado'],
            etiqueta=activo['etiqueta'],
            ultimaAsignacion=activo['ultimaAsignacion'],
            ultimaDesasignacion=activo['ultimaDesasignacion'],
            fechaCompra=activo['fechaCompra'],
            valorCompra=activo['valorCompra'],
            valorActual=activo['valorActual'],
            persona = activo['asignadoA']['nombre'],
            modelo = modelo_data['nombre'],
            depreciacion = depreciacion_nombre,
            ubicacion = ubicacion_nombre,
            categoria = categoria_nombre,
            fabricante = fabricante_nombre
        )
        objetos_activos.append(activo_instance)
    
    Activos.objects.bulk_create(objetos_activos)


