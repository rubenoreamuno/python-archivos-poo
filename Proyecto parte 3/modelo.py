#modelo
import csv
catalogo_productos = {}
registro_ventas = []
alertas_temporales = []
def crear_producto (codigo, nombre, categoria, stock, stock_minimo, precio_compra, precio_venta, fecha_vencimiento):
    producto_armado = {"codigo":codigo, "nombre": nombre, "categoria": categoria, "stock":stock, "stock_minimo":stock_minimo, "precio_compra": precio_compra, "precio_venta":precio_venta, "fecha_vencimiento":fecha_vencimiento}
    return producto_armado
def crear_venta (numero_factura, fecha, productos_vendidos, total_impuestos, total_general):
    venta = {"numero_factura": numero_factura, "fecha": fecha, "productos_vendidos": productos_vendidos, "total_impuestos": total_impuestos, "total_general": total_general}
    return venta
def crear_alerta (codigo_producto, tipo_alerta, mensaje):
    alerta = {"codigo_producto":codigo_producto, "tipo_alerta": tipo_alerta, "mensaje":mensaje}
    return alerta
def agregar_producto (producto):
    catalogo_productos[producto["codigo"]] = producto
def obtener_producto (codigo):
    return catalogo_productos[codigo]
def actualizar_stock (codigo, nueva_cantidad): 
    catalogo_productos[codigo]["stock"] = nueva_cantidad
def registrar_venta(venta):
    registro_ventas.append(venta)
def registrar_alerta(alerta):
    alertas_temporales.append(alerta)
def cargar_inventario (ruta): 
    with open (ruta, "r", encoding = "utf-8") as archivo:
        lector = list(csv.DictReader(archivo, delimiter = ";"))
    return lector





