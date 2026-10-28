# Ejercicio 2: Sistema de Inventario con Persistencia JSON

## 📋 Descripción

Desarrollar un sistema de gestión de inventario que permita realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre productos, con persistencia en formato JSON.

## 🎯 Objetivos de Aprendizaje

- Trabajar con archivos JSON (`json.load`, `json.dump`)
- Implementar un sistema CRUD completo
- Usar `@property` para validación de datos
- Implementar serialización de objetos (`to_dict`, `from_dict`)
- Manejar persistencia de datos

## 📝 Requisitos Funcionales

1. Cargar inventario inicial desde `data/inventario.csv`
2. Convertirlo a formato JSON
3. Implementar operaciones:
   - Agregar producto
   - Buscar producto por código
   - Actualizar stock
   - Actualizar precio
   - Eliminar producto
   - Listar todos los productos
   - Calcular valor total del inventario
4. Guardar cambios en `output/inventario.json`
5. Productos con stock bajo (< 10) deben marcarse en el reporte

## 🏗️ Diseño Sugerido

### Clase `Producto`

```python
class Producto:
    def __init__(self, codigo, nombre, categoria, precio, stock, proveedor):
        # Usar properties para validación
    
    @property
    def precio(self):
        return self._precio
    
    @precio.setter
    def precio(self, valor):
        # Validar que sea positivo
    
    @property
    def valor_stock(self):
        # Calcular precio * stock
    
    def to_dict(self):
        # Para JSON
    
    @classmethod
    def from_dict(cls, datos):
        # Desde JSON
```

### Clase `GestorInventario`

```python
class GestorInventario:
    def __init__(self):
        self.productos = {}  # {codigo: Producto}
    
    def cargar_desde_csv(self, archivo):
        # Importar datos iniciales
    
    def cargar_desde_json(self, archivo):
        # Cargar inventario existente
    
    def guardar_json(self, archivo):
        # Persistir cambios
    
    def agregar_producto(self, producto):
        pass
    
    def buscar(self, codigo):
        pass
    
    def actualizar_stock(self, codigo, cantidad):
        pass
    
    def eliminar(self, codigo):
        pass
    
    def valor_total_inventario(self):
        pass
    
    def productos_stock_bajo(self, umbral=10):
        pass
```

## 📤 Salida Esperada

Archivo `output/inventario.json` con productos guardados.

Consola:
```
✅ Inventario cargado: 12 productos
💰 Valor total del inventario: $23,456.78
⚠️  Productos con stock bajo (< 10):
   - P009: Impresora HP (8 unidades)
```

## 💡 Tips

- Usa diccionario para búsqueda rápida por código
- `ensure_ascii=False` para caracteres especiales en JSON
- `indent=4` para formato legible

## ✅ Criterios de Evaluación

- [x] Carga correcta desde CSV y JSON
- [x] CRUD completo funcional
- [x] Validaciones con `@property`
- [x] Persistencia correcta en JSON
- [x] Cálculos de valor de inventario correctos
