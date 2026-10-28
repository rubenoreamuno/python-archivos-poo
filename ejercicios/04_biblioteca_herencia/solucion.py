#!/usr/bin/env python3
"""
Ejercicio 4: Sistema de Biblioteca con Herencia
Gestión de libros y préstamos usando herencia y JSON anidado
"""

import json
from pathlib import Path
from abc import ABC, abstractmethod


class Publicacion(ABC):
    """Clase abstracta base para todas las publicaciones"""
    
    def __init__(self, titulo, autor, anio):
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
    
    @abstractmethod
    def to_dict(self):
        """Cada subclase debe implementar su serialización"""
        pass
    
    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.anio})"


class Prestamo:
    """Representa un préstamo de libro"""
    
    def __init__(self, id_prestamo, usuario, fecha_prestamo, fecha_devolucion, devuelto):
        self.id_prestamo = id_prestamo
        self.usuario = usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.devuelto = devuelto
    
    @classmethod
    def from_dict(cls, datos):
        """Crea un préstamo desde un diccionario"""
        return cls(
            id_prestamo=datos['id_prestamo'],
            usuario=datos['usuario'],
            fecha_prestamo=datos['fecha_prestamo'],
            fecha_devolucion=datos['fecha_devolucion'],
            devuelto=datos['devuelto']
        )
    
    def to_dict(self):
        """Convierte el préstamo a diccionario"""
        return {
            'id_prestamo': self.id_prestamo,
            'usuario': self.usuario,
            'fecha_prestamo': self.fecha_prestamo,
            'fecha_devolucion': self.fecha_devolucion,
            'devuelto': self.devuelto
        }
    
    def __str__(self):
        estado = "✅ Devuelto" if self.devuelto else "🔵 Activo"
        return f"{estado} | {self.usuario} - {self.fecha_prestamo}"


class Libro(Publicacion):
    """Representa un libro en la biblioteca"""
    
    def __init__(self, isbn, titulo, autor, anio, genero, disponibles, prestamos):
        super().__init__(titulo, autor, anio)
        self.isbn = isbn
        self.genero = genero
        self.disponibles = disponibles
        self.prestamos = prestamos if isinstance(prestamos, list) else []
    
    @classmethod
    def from_dict(cls, datos):
        """Crea un libro desde un diccionario (incluyendo préstamos anidados)"""
        # Convertir préstamos anidados
        prestamos_list = datos.get('prestamos', [])
        prestamos = [Prestamo.from_dict(p) for p in prestamos_list]
        
        return cls(
            isbn=datos['isbn'],
            titulo=datos['titulo'],
            autor=datos['autor'],
            anio=datos['anio'],
            genero=datos['genero'],
            disponibles=datos['disponibles'],
            prestamos=prestamos
        )
    
    def to_dict(self):
        """Convierte el libro a diccionario (incluyendo préstamos)"""
        return {
            'isbn': self.isbn,
            'titulo': self.titulo,
            'autor': self.autor,
            'anio': self.anio,
            'genero': self.genero,
            'disponibles': self.disponibles,
            'prestamos': [p.to_dict() for p in self.prestamos]
        }
    
    @property
    def prestamos_activos(self):
        """Retorna lista de préstamos no devueltos"""
        return [p for p in self.prestamos if not p.devuelto]
    
    @property
    def total_prestamos(self):
        """Total de préstamos históricos"""
        return len(self.prestamos)
    
    def __str__(self):
        return f"{self.titulo} - {self.autor} | ISBN: {self.isbn} | Disponibles: {self.disponibles}"


class GestorBiblioteca:
    """Gestor principal del sistema de biblioteca"""
    
    def __init__(self):
        self.nombre = ""
        self.direccion = ""
        self.libros = []
    
    def cargar_desde_json(self, archivo):
        """Carga la biblioteca desde JSON con estructura anidada"""
        archivo = Path(archivo)
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                
                self.nombre = datos.get('nombre', '')
                self.direccion = datos.get('direccion', '')
                
                # Cargar libros (lista anidada con préstamos)
                self.libros = [
                    Libro.from_dict(libro_dict)
                    for libro_dict in datos.get('libros', [])
                ]
            
            print(f"✅ Biblioteca cargada: {len(self.libros)} libros")
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {archivo}")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ Error al leer JSON: {e}")
            raise
    
    def guardar_json(self, archivo):
        """Guarda la biblioteca en JSON"""
        archivo = Path(archivo)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        datos = {
            'nombre': self.nombre,
            'direccion': self.direccion,
            'libros': [libro.to_dict() for libro in self.libros]
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Biblioteca guardada en: {archivo}")
    
    def buscar_por_isbn(self, isbn):
        """Busca un libro por ISBN"""
        for libro in self.libros:
            if libro.isbn == isbn:
                return libro
        return None
    
    def buscar_por_titulo(self, titulo):
        """Busca libros por título (búsqueda parcial)"""
        return [
            libro for libro in self.libros
            if titulo.lower() in libro.titulo.lower()
        ]
    
    def buscar_por_autor(self, autor):
        """Busca libros por autor (búsqueda parcial)"""
        return [
            libro for libro in self.libros
            if autor.lower() in libro.autor.lower()
        ]
    
    def listar_todos(self):
        """Retorna todos los libros"""
        return self.libros
    
    def prestamos_activos(self):
        """Retorna todos los préstamos activos de toda la biblioteca"""
        activos = []
        for libro in self.libros:
            for prestamo in libro.prestamos_activos:
                activos.append((libro, prestamo))
        return activos
    
    def libros_disponibles(self):
        """Retorna libros con disponibilidad > 0"""
        return [libro for libro in self.libros if libro.disponibles > 0]
    
    def generar_reporte(self, archivo_salida):
        """Genera un reporte completo del sistema"""
        archivo_salida = Path(archivo_salida)
        archivo_salida.parent.mkdir(parents=True, exist_ok=True)
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("=" * 50 + "\n")
            f.write("        SISTEMA DE BIBLIOTECA\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Biblioteca: {self.nombre}\n")
            f.write(f"Dirección: {self.direccion}\n")
            f.write(f"Total de libros: {len(self.libros)}\n\n")
            
            # Libros disponibles
            f.write("--- Libros en Catálogo ---\n")
            for libro in self.libros:
                f.write(f"\n📚 {libro.titulo}\n")
                f.write(f"   Autor: {libro.autor}\n")
                f.write(f"   ISBN: {libro.isbn}\n")
                f.write(f"   Género: {libro.genero}\n")
                f.write(f"   Disponibles: {libro.disponibles}\n")
                f.write(f"   Préstamos activos: {len(libro.prestamos_activos)}\n")
                f.write(f"   Total préstamos (histórico): {libro.total_prestamos}\n")
            
            # Préstamos activos
            f.write("\n\n--- Préstamos Activos ---\n")
            activos = self.prestamos_activos()
            if activos:
                for libro, prestamo in activos:
                    f.write(f"\n🔵 {prestamo.usuario}\n")
                    f.write(f"   Libro: {libro.titulo}\n")
                    f.write(f"   Fecha préstamo: {prestamo.fecha_prestamo}\n")
                    f.write(f"   Debe devolver: {prestamo.fecha_devolucion}\n")
            else:
                f.write("✅ No hay préstamos activos\n")
            
            # Estadísticas
            f.write("\n\n--- Estadísticas ---\n")
            total_prestamos = sum(libro.total_prestamos for libro in self.libros)
            f.write(f"Total préstamos históricos: {total_prestamos}\n")
            f.write(f"Préstamos activos: {len(activos)}\n")
            f.write(f"Libros con disponibilidad: {len(self.libros_disponibles())}\n")
        
        print(f"📊 Reporte generado en: {archivo_salida}")


def main():
    """Función principal"""
    # Crear gestor
    gestor = GestorBiblioteca()
    
    # Cargar desde JSON
    gestor.cargar_desde_json('data/biblioteca.json')
    
    # Mostrar información básica
    print(f"\n📚 {gestor.nombre}")
    print(f"📍 {gestor.direccion}")
    print(f"📖 Total de libros: {len(gestor.libros)}")
    
    # Préstamos activos
    activos = gestor.prestamos_activos()
    print(f"🔵 Préstamos activos: {len(activos)}")
    
    # Demostrar búsquedas
    print("\n🔍 Demostrando búsquedas:")
    
    libro = gestor.buscar_por_isbn('978-0307474728')
    if libro:
        print(f"   Por ISBN: {libro.titulo}")
    
    resultados = gestor.buscar_por_autor('García')
    print(f"   Por autor 'García': {len(resultados)} resultados")
    
    # Generar reporte
    gestor.generar_reporte('output/reporte_biblioteca.txt')
    
    print(f"\n✨ Proceso completado!\n")


if __name__ == '__main__':
    main()
