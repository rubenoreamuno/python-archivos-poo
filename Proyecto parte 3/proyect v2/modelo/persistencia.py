import csv
import json

# Variables de configuración
path_inventario = "../../data/Inventariotrigueros.csv"
path_ventas = "../../data/Inventariotrigueros.csv"

columnas_inventario = ['codigo', 'nombre', 'categoria', 
                    'stock', 'stock_minimo', 'precio_compra',
                    'precio_venta', 'fecha_vencimiento']

# Inventario 

def leer_inventario():
    with open (path_inventario, "r", encoding = "utf-8") as archivo:
        lector = list(csv.DictReader(archivo, delimiter = ";"))
        data = [row for row in lector]
        return data

def existe_producto_inventario(codigo_producto: str):
    lector = leer_inventario()
    for fila in lector:
        if fila['codigo'] == codigo_producto:
            return True
    return False

def agregar_producto_inventario(producto : dict):
    # Fallar o avisar si el producto ya existe y si los datos del producto no vienen completos.

    # Paso 1: abrir el archivo para ver si ya existe el producto.
    if existe_producto_inventario(producto['codigo']) == True:
        print("El producto ya existe")
        return 0
            # Buscar si el producto ya existe, si sí existe mandar un mensaje o un error al usuario.
            # Tal ves desde la UI mostrar los detalles del producto que ya existe.
            #return 0
        
    # Paso 2: verificar que los datos del producto que pasa el usuario estén completos.
    # También se puede hacer verificación de tipos de datos.
    try:
        codigo = producto['codigo']
        nombre = producto['nombre']
        precio = float(producto['precio_venta'])
        stock = int(producto['stock'])
    except Exception as e:
        print(e)
        return 1


    # Paso 3: Agregar el producto al archivo.
    with open(path_inventario, 'a', encoding='utf-8', newline='') as f:
        columnas = columnas_inventario
        escritor = csv.DictWriter(f, fieldnames=columnas)
        escritor.writerow(producto)

    return 200
    

def sobreescribir_inventario(productos : list):
    # Sobreescribir todo el archivo de inventario.
    headers = columnas_inventario
    with open (path_inventario, "w", encoding = "utf-8") as archivo:
        fieldnames = headers
        writer = csv.DictWriter(archivo, fieldnames=fieldnames, delimiter = ",")
        writer.writeheader ()
        writer.writerows(productos)
    return writer


def eliminar_producto_inventario(codigo_producto: str): # solo el id del producto
    # Paso 1: verificar si el producto existe.
    if existe_producto_inventario(codigo_producto) == False:
        print("El producto no existe")
        return 0
    
    inventario = leer_inventario()

    for i in inventario:
        if i['codigo'] == codigo_producto:
            inventario.remove(i)
            break
    
    sobreescribir_inventario(inventario)

##############################################
# Ventas
def leer_ventas():
    with open (path_ventas, "r", encoding = "utf-8") as archivo:
        lector = list(csv.DictReader(archivo, delimiter = ";"))
        data = [row for row in lector]
        return data

def registrar_venta(venta : dict):
    pass

#leer_inventario()
#eliminar_producto_inventario('L001')
#ventas = leer_ventas()

agregar_producto_inventario({
    "codigo":'L021',
    "nombre":' Leche',
    "categoria":' lacteos',
    "stock":15,
    "stock_minimo":5,
    "precio_compra":1000.00,
    "precio_venta":1200.00,
    "fecha_vencimiento":'2026-10-31'
})




