class Producto:
    def __init__(self, 
                codigo, nombre, categoria, 
                stock, stock_minimo, precio_compra, precio_venta, fecha_vencimiento):
    
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.stock = stock
        self.stock_minimo = stock_minimo
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.fecha_vencimiento = fecha_vencimiento

    def agregar_producto(self):
        nuevo_producto = {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'stock': self.stock,
            'stock_minimo': self.stock_minimo,
            'precio_compra': self.precio_compra,
            'precio_venta': self.precio_venta,
            'fecha_vencimiento': self.fecha_vencimiento
        }
        return nuevo_producto
        

    @classmethod
    def eliminar_producto(cls, codigo, productos : list):

        # Retornar el diccionario sin el producto.
        for producto in productos:
            if producto['codigo'] == codigo:
                productos.remove(producto)

        return productos



#Producto.eliminar_producto('L001', productos=productos)



