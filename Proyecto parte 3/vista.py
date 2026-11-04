#vision y validacion 4
import controlador
# VISTA

def mostrar_menu():
    print('\n===== SUPERMERCADO TRIGUEROS =====')
    print('1. Registrar mercancía')
    print('2. Registrar venta')
    print('3. Consultar inventario')
    print('4. Consultar alertas')
    print('5. Consultar ventas')
    print('6. Actualizar stock')  
    print('0. Salir')

def solicitar_opcion():
    """Solicita una opción del menú."""
    return input("Seleccione una opción: ").strip()

def mostrar_opcion(opcion):
    if opcion == 1:
        print("Seleccionó: Registrar mercancía")

    elif opcion == 2:
        print("Seleccionó: Registrar venta")
    elif opcion == 3:
        print("Seleccionó: Consultar inventario")
    elif opcion == 4:
        print("Seleccionó: Consultar alertas")
    elif opcion == 5:
        print("Seleccionó: Consultar ventas")
    elif opcion == 6:  # NUEVO
        print("Seleccionó: Actualizar stock")
    elif opcion == 0:
        print("Gracias por utilizar el sistema.")

def mostrar_mensaje():
    print('Operación realizada correctamente.')

def mostrar_error():
    print('Error: Los datos ingresados no son válidos.')

def producto_registrado():
    print('Producto registrado correctamente.')

def venta_realizada():
    print('Venta realizada correctamente.')

def venta_cancelada():
    print('La venta fue cancelada.')

def producto_no_encontrado():
    print('Error: El producto no existe en el inventario.')

def stock_insuficiente():
    print('Error: No hay suficiente cantidad del producto.')

def opcion_invalida():
    print('Error: La opción seleccionada no es válida.')

def mostrar_inventario(productos):
    print('\n===== INVENTARIO =====')
    print('Código | Producto | Stock | Precio')
    if not productos:
        print('No hay productos registrados.')
    for producto in productos:
        print(producto['codigo'], '|', producto['nombre'], '|',
              producto['stock'], '|', producto['precio_venta'])
    print('* = stock bajo')

def mostrar_ventas(ventas):
    print('\n===== VENTAS =====')
    if not ventas:
        print('No hay ventas registradas.')
    for venta in ventas:
        print('Factura:', venta['numero_factura'],
              '| Fecha:', venta['fecha'],
              '| Total:', venta['total_general'])

def mostrar_alertas(alertas):
    print('\n===== ALERTAS =====')
    if not alertas:
        print('No hay alertas registradas.')
    for alerta in alertas:
        print(alerta['mensaje'])

def codigo_duplicado():
    print('Error: el código ingresado ya existe.')

def mostrar_resumen_venta(nombre, cantidad, subtotal, impuestos, total):  
    print('\n--- Resumen de la venta ---')
    print(cantidad, 'x', nombre)
    print('Subtotal:        ', subtotal)
    print('Impuestos (13%): ', impuestos)
    print('TOTAL:           ', total)

def mostrar_totales_ventas(total_impuestos, total_general):  
    print('Impuestos acumulados:', total_impuestos)
    print('Total acumulado:     ', total_general)

def confirmar_venta():
    while True:
        respuesta = input('¿Desea finalizar la venta? (s/n): ').strip().lower()
        if respuesta == 's':
            return True
        elif respuesta == 'n':
            venta_cancelada()
            return False
        else:
            print('Error: Ingrese s o n.')


# VALIDACIONES

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto != '':
            return texto
        print('Error: El campo no puede estar vacío.')

def pedir_entero(mensaje, minimo=1):
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= minimo:
                return numero
            print('Error: El número debe ser mayor o igual a', minimo)
        except ValueError:
            print('Error: Debe ingresar un número entero.')

def pedir_precio(mensaje):
    while True:
        try:
            precio = float(input(mensaje))
            if 0 < precio < float('inf'):
                return precio
            print('Error: El precio debe ser mayor que cero.')
        except ValueError:
            print('Error: Debe ingresar un precio válido.')

def pedir_fecha():
    
    while True:
        fecha = input('Fecha de vencimiento (AAAA-MM-DD, vacío si no aplica): ').strip()
        if fecha == '': 
            return fecha
        partes = fecha.split('-')
        if len(partes) == 3:
            anio, mes, dia = partes
            if (len(anio) == 4 and len(mes) == 2 and len(dia) == 2
                    and anio.isdigit() and mes.isdigit() and dia.isdigit()):
                if 1 <= int(mes) <= 12 and 1 <= int(dia) <= 31:
                    return fecha
        print('Error: Ingrese una fecha en formato AAAA-MM-DD.')

def pedir_opcion():
    while True:
        try:
            opcion = int(input('Seleccione una opción: '))
            if 0 <= opcion <= 6:
                return opcion
            opcion_invalida()
        except ValueError:
            print('Error: Debe ingresar un número.')



