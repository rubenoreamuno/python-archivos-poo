import producto
import csv

path_inventario = "../../data/Inventariotrigueros.csv"

def agregar_producto_inventario(producto : dict):
    with open(path_inventario, 'a', encoding='utf-8') as f:
        columnas = ['codigo', 'nombre', 'categoria', 
                    'stock', 'stock_minimo', 'precio_compra',
                    'precio_venta', 'fecha_vencimiento'
        ]
        escritor = csv.DictWriter(f, fieldnames=columnas, delimiter=';')
        escritor.writerow(producto)

def eliminar_producto_inventario():
    pass


prod = producto.Producto(
    codigo='L001',
    nombre=' Leche',
    categoria=' l\xa0cteos',
    stock='15',
    stock_minimo='5',
    precio_compra='1000',
    precio_venta='1200',
    fecha_vencimiento='2026-10-31'
)

prod_dict = prod.agregar_producto()
print(prod_dict)

agregar_producto_inventario(prod_dict)
