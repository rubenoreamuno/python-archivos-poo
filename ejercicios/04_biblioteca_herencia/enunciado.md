# Ejercicio 4: Sistema de Biblioteca con Herencia

## 📋 Descripción

Desarrollar un sistema de gestión de biblioteca que maneje diferentes tipos de publicaciones (libros, revistas) usando herencia, con datos anidados en JSON.

## 🎯 Objetivos de Aprendizaje

- Trabajar con JSON anidado y estructuras complejas
- Implementar herencia de clases
- Usar clases abstractas (`ABC`, `@abstractmethod`)
- Patrón Factory para crear objetos polimórficos
- Navegar estructuras de datos jerárquicas

## 📝 Requisitos Funcionales

1. Leer `data/biblioteca.json` (estructura anidada)
2. Implementar jerarquía de clases:
   - `Publicacion` (abstracta): base para libros/revistas
   - `Libro`: hereda de Publicacion
   - `Prestamo`: información de préstamos
3. Operaciones:
   - Listar todos los libros
   - Buscar por ISBN, título o autor
   - Listar préstamos activos (no devueltos)
   - Calcular disponibilidad real
   - Generar reporte de uso
4. Guardar cambios en JSON

## 🏗️ Diseño Sugerido

### Jerarquía de Clases

```python
from abc import ABC, abstractmethod

class Publicacion(ABC):
    """Clase abstracta base para publicaciones"""
    
    def __init__(self, titulo, autor, anio):
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
    
    @abstractmethod
    def to_dict(self):
        """Cada subclase implementa su serialización"""
        pass
    
    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.anio})"

class Libro(Publicacion):
    def __init__(self, isbn, titulo, autor, anio, genero, disponibles, prestamos):
        super().__init__(titulo, autor, anio)
        self.isbn = isbn
        self.genero = genero
        self.disponibles = disponibles
        self.prestamos = [Prestamo.from_dict(p) for p in prestamos]
    
    @property
    def prestamos_activos(self):
        return [p for p in self.prestamos if not p.devuelto]

class Prestamo:
    def __init__(self, id_prestamo, usuario, fecha_prestamo, fecha_devolucion, devuelto):
        # Atributos
```

### Gestor

```python
class GestorBiblioteca:
    def __init__(self):
        self.nombre = ""
        self.libros = []
    
    def cargar_desde_json(self, archivo):
        # Parsear JSON anidado
    
    def buscar_por_isbn(self, isbn):
        pass
    
    def prestamos_activos(self):
        # Retornar todos los préstamos no devueltos
```

## 📤 Salida Esperada

```
========================================
    SISTEMA DE BIBLIOTECA
========================================

Biblioteca: Biblioteca Central Universidad
Total de libros: 5

--- Libros Disponibles ---
✅ Cien Años de Soledad (ISBN: 978-0307474728)
   Disponibles: 3 | Préstamos activos: 1

--- Préstamos Activos ---
🔵 Luis Martínez - Cien Años de Soledad
   Fecha préstamo: 2024-01-20
   Debe devolver: 2024-02-03
```

## 💡 Tips

- Usa `isinstance()` para verificar tipos
- Factory pattern: función que crea objetos según tipo
- Navegación JSON: `datos['libros'][0]['prestamos']`

## ✅ Criterios de Evaluación

- [x] Herencia correctamente implementada
- [x] Carga de JSON anidado exitosa
- [x] Búsquedas funcionan correctamente
- [x] Cálculo de disponibilidad correcto
- [x] Código usa POO apropiadamente
