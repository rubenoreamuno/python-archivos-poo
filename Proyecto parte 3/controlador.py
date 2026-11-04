#Controlador
import modelo
import vista
from datetime import datetime, date
import json

IMPUESTO = 0.13
DIAS_ALERTA = 7
productos = []


def leer_variable_ubicacion_inventario():
    # Leer el archivo de configuración.
    with open('config.json', 'r', encoding='utf-8') as f:
        archivo = json.load(f)  # dict o list

    # Extraer el valor de la variable "inventario_path"
    inventario_path = archivo["inventario_path"]

    return inventario_path

inventario_path = leer_variable_ubicacion_inventario()

print(modelo.cargar_inventario(ruta = inventario_path))

def registrar_producto():
    codigo = vista.pedir_texto("Código: ")
    if codigo in modelo.catalogo_productos:
        vista.codigo_duplicado()
        return
    nombre = vista.pedir_texto("Nombre: ")
    categoria = vista.pedir_texto("Categoría: ")
    stock = vista.pedir_entero("Stock inicial: ", 0)
    stock_minimo = vista.pedir_entero("Stock mínimo: ", 0)
    precio_compra = vista.pedir_precio("Precio de compra: ")
    precio_venta = vista.pedir_precio("Precio de venta: ")
    fecha = vista.pedir_fecha()
    producto = modelo.crear_producto(codigo, nombre, categoria, stock, stock_minimo,
                                     precio_compra, precio_venta, fecha)
    modelo.agregar_producto(producto)
    vista.producto_registrado()


def actualizar_stock():
    codigo = vista.pedir_texto("Código del producto: ")
    if codigo not in modelo.catalogo_productos:
        vista.producto_no_encontrado()
        return
    cantidad = vista.pedir_entero("Cantidad a agregar: ", 1)
    producto = modelo.obtener_producto(codigo)
    modelo.actualizar_stock(codigo, producto["stock"] + cantidad)
    vista.mostrar_mensaje()


def realizar_venta():
    codigo = vista.pedir_texto("Código del producto: ")
    if codigo not in modelo.catalogo_productos:
        vista.producto_no_encontrado()
        return
    producto = modelo.obtener_producto(codigo)
    cantidad = vista.pedir_entero("Cantidad: ", 1)
    if cantidad > producto["stock"]:
        vista.stock_insuficiente()
        return

    subtotal = round(cantidad * producto["precio_venta"], 2)
    impuestos = round(subtotal * IMPUESTO, 2)
    total = round(subtotal + impuestos, 2)
    vista.mostrar_resumen_venta(producto["nombre"], cantidad, subtotal, impuestos, total)
    if not vista.confirmar_venta():
        return

    modelo.actualizar_stock(codigo, producto["stock"] - cantidad)
    numero = "F-" + str(len(modelo.registro_ventas) + 1)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    vendidos = [{"codigo": codigo, "cantidad": cantidad, "subtotal": subtotal}]
    modelo.registrar_venta(modelo.crear_venta(numero, fecha, vendidos, impuestos, total))
    vista.venta_realizada()


def consultar_alertas():
    modelo.alertas_temporales.clear()   
    for p in modelo.catalogo_productos.values():
        if p["stock"] <= p["stock_minimo"]:
            mensaje = "Stock bajo: " + p["nombre"] + " (quedan " + str(p["stock"]) + ")"
            modelo.registrar_alerta(modelo.crear_alerta(p["codigo"], "stock_bajo", mensaje))
        if p["fecha_vencimiento"] != "":
            try:
                vence = datetime.strptime(p["fecha_vencimiento"], "%Y-%m-%d").date()
                if (vence - date.today()).days <= DIAS_ALERTA:
                    mensaje = "Vencimiento próximo: " + p["nombre"] + " vence el " + p["fecha_vencimiento"]
                    modelo.registrar_alerta(modelo.crear_alerta(p["codigo"], "vencimiento_proximo", mensaje))
            except ValueError:
                pass   
    vista.mostrar_alertas(modelo.alertas_temporales)


def consultar_inventario(productos):
    #for p in productos:
        #copia = dict(p)    
        #if p["stock"] <= p["stock_minimo"]:
        #    copia["nombre"] = p["nombre"] + " *"
        #productos[codigo] = copia
    vista.mostrar_inventario(productos)


def consultar_ventas():
    total_impuestos = 0
    total_general = 0
    for venta in modelo.registro_ventas:
        total_impuestos += venta["total_impuestos"]
        total_general += venta["total_general"]
    vista.mostrar_ventas(modelo.registro_ventas)
    vista.mostrar_totales_ventas(round(total_impuestos, 2), round(total_general, 2))


def iniciar_proceso():
    productos = modelo.cargar_inventario()
    opcion = -1
    while opcion != 0:
        vista.mostrar_menu()
        opcion = vista.pedir_opcion()
        vista.mostrar_opcion(opcion)
        if opcion == 1:
            registrar_producto()
        elif opcion == 2:
            realizar_venta()
        elif opcion == 3:
            consultar_inventario(productos)
        elif opcion == 4:
            consultar_alertas()
        elif opcion == 5:
            consultar_ventas()
        elif opcion == 6:
            actualizar_stock()
