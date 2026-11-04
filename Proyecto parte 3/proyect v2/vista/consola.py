import sys

sys.path.append("/Workspace/Users/ruben.oreamuno2000@gmail.com/python-archivos-poo/Proyecto parte 3/proyect v2/")

from modelo import producto, persistencia

codigo = str(input("Ingrese el código del producto nuevo "))
nombre = input("Ingrese el nombre del producto nuevo ")
categoria = input("Ingrese la categoría del producto nuevo ")
stock = int(input("Ingrese el stock del producto nuevo "))
stock_minimo = int(input("Ingrese el stock mínimo del producto nuevo "))
precio_compra = float(input("Ingrese el precio de compra del producto nuevo "))
precio_venta = float(input("Ingrese el precio de venta del producto nuevo "))
fecha_vencimiento = input("Ingrese la fecha de vencimiento del producto nuevo ")


prod = producto.Producto(
    codigo=codigo,
    nombre=nombre,
    categoria=categoria,
    stock=stock,
    stock_minimo=stock_minimo,
    precio_compra=precio_compra,
    precio_venta=precio_venta,
    fecha_vencimiento=fecha_vencimiento
)

prod_dict = prod.agregar_producto()

persistencia.agregar_producto_inventario(prod_dict)

print("Producto agregado con éxito") 