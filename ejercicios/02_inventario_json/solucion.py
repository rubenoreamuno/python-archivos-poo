#!/usr/bin/env python3
"""
Ejercicio 2: Sistema de Inventario con Persistencia JSON
CRUD completo de productos con validación y persistencia
"""

import csv
import json
from pathlib import Path


class Producto:
    """Representa un producto del inventario con validación"""
    
    def __init__(self, codigo, nombre, categoria, precio, stock, proveedor):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.proveedor = proveedor
        # Usar setters para validación
        self._precio = 0.0
        self._stock = 0
        self.precio = float(precio)
        self.stock = int(stock)
    
    @property
    def precio(self):
        return self._precio
    
    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError(f"El precio no puede ser negativo: {valor}")
        self._precio = valor
    
    @property
    def stock(self):
        return self._stock
    
    @stock.setter
    def stock(self, valor):
        if valor < 0:
            raise ValueError(f"El stock no puede ser negativo: {valor}")
        self._stock = valor
    
    @property
    def valor_stock(self):
        """Calcula el valor total del stock de este producto"""
        return self._precio * self._stock
    
    def to_dict(self):
        """Convierte el producto a diccionario para JSON"""
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'precio': self._precio,
            'stock': self._stock,
            'proveedor': self.proveedor
        }
    
    @classmethod
    def from_dict(cls, datos):
        """Crea un producto desde un diccionario"""
        return cls(
            codigo=datos['codigo'],
            nombre=datos['nombre'],
            categoria=datos['categoria'],
            precio=datos['precio'],
            stock=datos['stock'],
            proveedor=datos['proveedor']
        )
    
    @classmethod
    def from_csv_row(cls, fila):
        """Crea un producto desde una fila CSV"""
        return cls(
            codigo=fila['codigo'],
            nombre=fila['nombre'],
            categoria=fila['categoria'],
            precio=fila['precio'],
            stock=fila['stock'],
            proveedor=fila['proveedor']
        )
    
    def __str__(self):
        return f"{self.codigo}: {self.nombre} - ${self._precio:.2f} ({self._stock} unid.)"
    
    def __repr__(self):
        return f"Producto({self.codigo!r}, {self.nombre!r}, ${self._precio:.2f})"


class GestorInventario:
    """Gestor CRUD para productos con persistencia JSON"""
    
    def __init__(self):
        self.productos = {}  # {codigo: Producto}
    
    def cargar_desde_csv(self, archivo):
        """Carga productos desde un archivo CSV"""
        archivo = Path(archivo)
        try:
            with open(archivo, 'r', encoding='utf-8', newline='') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    producto = Producto.from_csv_row(fila)
                    self.productos[producto.codigo] = producto
            print(f"✅ Cargados {len(self.productos)} productos desde CSV")
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {archivo}")
            raise
    
    def cargar_desde_json(self, archivo):
        """Carga productos desde un archivo JSON"""
        archivo = Path(archivo)
        if not archivo.exists():
            print(f"⚠️  Archivo JSON no existe: {archivo}")
            return
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.productos = {
                    codigo: Producto.from_dict(prod_dict)
                    for codigo, prod_dict in datos.items()
                }
            print(f"✅ Cargados {len(self.productos)} productos desde JSON")
        except json.JSONDecodeError as e:
            print(f"❌ Error al leer JSON: {e}")
            raise
    
    def guardar_json(self, archivo):
        """Guarda el inventario en formato JSON"""
        archivo = Path(archivo)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        # Convertir todos los productos a diccionarios
        datos = {
            codigo: producto.to_dict()
            for codigo, producto in self.productos.items()
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        
        print(f"💾 Inventario guardado en: {archivo}")
    
    def agregar_producto(self, producto):
        """Agrega un nuevo producto al inventario"""
        if producto.codigo in self.productos:
            print(f"⚠️  El producto {producto.codigo} ya existe")
            return False
        self.productos[producto.codigo] = producto
        print(f"✅ Producto {producto.codigo} agregado")
        return True
    
    def buscar(self, codigo):
        """Busca un producto por código"""
        return self.productos.get(codigo)
    
    def actualizar_stock(self, codigo, cantidad):
        """Actualiza el stock de un producto"""
        producto = self.buscar(codigo)
        if not producto:
            print(f"❌ Producto {codigo} no encontrado")
            return False
        
        producto.stock = cantidad
        print(f"✅ Stock actualizado: {producto}")
        return True
    
    def actualizar_precio(self, codigo, nuevo_precio):
        """Actualiza el precio de un producto"""
        producto = self.buscar(codigo)
        if not producto:
            print(f"❌ Producto {codigo} no encontrado")
            return False
        
        producto.precio = nuevo_precio
        print(f"✅ Precio actualizado: {producto}")
        return True
    
    def eliminar(self, codigo):
        """Elimina un producto del inventario"""
        if codigo in self.productos:
            producto = self.productos.pop(codigo)
            print(f"🗑️  Producto eliminado: {producto}")
            return True
        print(f"❌ Producto {codigo} no encontrado")
        return False
    
    def listar_todos(self):
        """Retorna lista de todos los productos"""
        return list(self.productos.values())
    
    def valor_total_inventario(self):
        """Calcula el valor total del inventario"""
        return sum(prod.valor_stock for prod in self.productos.values())
    
    def productos_stock_bajo(self, umbral=10):
        """Retorna productos con stock por debajo del umbral"""
        return [
            prod for prod in self.productos.values()
            if prod.stock < umbral
        ]


def main():
    """Función principal"""
    # Crear gestor
    gestor = GestorInventario()
    
    # Cargar desde CSV
    gestor.cargar_desde_csv('data/inventario.csv')
    
    # Mostrar inventario inicial
    print(f"\n📦 Total de productos: {len(gestor.listar_todos())}")
    print(f"💰 Valor total del inventario: ${gestor.valor_total_inventario():,.2f}")
    
    # Productos con stock bajo
    stock_bajo = gestor.productos_stock_bajo(umbral=10)
    if stock_bajo:
        print(f"\n⚠️  Productos con stock bajo (< 10):")
        for prod in stock_bajo:
            print(f"   - {prod.codigo}: {prod.nombre} ({prod.stock} unidades)")
    
    # Demostrar operaciones CRUD
    print("\n🔧 Demostrando operaciones CRUD:")
    
    # Actualizar stock
    gestor.actualizar_stock('P001', 20)
    
    # Actualizar precio
    gestor.actualizar_precio('P002', 29.99)
    
    # Agregar nuevo producto
    nuevo_producto = Producto(
        'P013', 'SSD 500GB', 'Almacenamiento', 120.00, 15, 'DataWorld'
    )
    gestor.agregar_producto(nuevo_producto)
    
    # Guardar en JSON
    gestor.guardar_json('output/inventario.json')
    
    print(f"\n✨ Proceso completado!\n")


if __name__ == '__main__':
    main()
