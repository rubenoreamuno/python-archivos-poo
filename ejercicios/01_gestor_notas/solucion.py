#!/usr/bin/env python3
"""
Ejercicio 1: Gestor de Notas Estudiantiles
Sistema para cargar, analizar y generar reportes de notas desde CSV
"""

import csv
from pathlib import Path


class Nota:
    """Representa una calificación de un estudiante en una materia"""
    
    def __init__(self, id_estudiante, materia, nota, creditos, periodo):
        self.id_estudiante = id_estudiante
        self.materia = materia
        self.nota = float(nota)
        self.creditos = int(creditos)
        self.periodo = periodo
    
    @classmethod
    def from_csv_row(cls, fila):
        """Constructor alternativo desde una fila CSV (diccionario)"""
        return cls(
            id_estudiante=fila['id_estudiante'],
            materia=fila['materia'],
            nota=fila['nota'],
            creditos=fila['creditos'],
            periodo=fila['periodo']
        )
    
    def __str__(self):
        return f"{self.id_estudiante} - {self.materia}: {self.nota}"
    
    def __repr__(self):
        return f"Nota({self.id_estudiante!r}, {self.materia!r}, {self.nota})"


class GestorNotas:
    """Gestor para cargar, analizar y generar reportes de notas"""
    
    def __init__(self, archivo_csv):
        self.archivo_csv = Path(archivo_csv)
        self.notas = []
    
    def cargar_notas(self):
        """Carga las notas desde el archivo CSV"""
        try:
            with open(self.archivo_csv, 'r', encoding='utf-8', newline='') as f:
                lector = csv.DictReader(f)
                self.notas = [Nota.from_csv_row(fila) for fila in lector]
            print(f"✅ Se cargaron {len(self.notas)} notas desde {self.archivo_csv}")
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo {self.archivo_csv}")
            raise
        except ValueError as e:
            print(f"❌ Error al convertir datos: {e}")
            raise
    
    def promedio_general(self):
        """Calcula el promedio de todas las notas"""
        if not self.notas:
            return 0.0
        return sum(nota.nota for nota in self.notas) / len(self.notas)
    
    def promedio_por_estudiante(self):
        """Calcula el promedio de cada estudiante"""
        estudiantes = {}
        for nota in self.notas:
            if nota.id_estudiante not in estudiantes:
                estudiantes[nota.id_estudiante] = []
            estudiantes[nota.id_estudiante].append(nota.nota)
        
        # Calcular promedio de cada estudiante
        return {
            id_est: sum(notas) / len(notas)
            for id_est, notas in estudiantes.items()
        }
    
    def promedio_por_materia(self):
        """Calcula el promedio de cada materia"""
        materias = {}
        for nota in self.notas:
            if nota.materia not in materias:
                materias[nota.materia] = []
            materias[nota.materia].append(nota.nota)
        
        # Calcular promedio de cada materia
        return {
            materia: sum(notas) / len(notas)
            for materia, notas in materias.items()
        }
    
    def nota_maxima(self):
        """Encuentra la nota más alta"""
        if not self.notas:
            return None
        return max(self.notas, key=lambda n: n.nota)
    
    def nota_minima(self):
        """Encuentra la nota más baja"""
        if not self.notas:
            return None
        return min(self.notas, key=lambda n: n.nota)
    
    def generar_reporte(self, archivo_salida):
        """Genera un reporte de texto con todas las estadísticas"""
        archivo_salida = Path(archivo_salida)
        
        # Crear directorio output si no existe
        archivo_salida.parent.mkdir(parents=True, exist_ok=True)
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("=" * 40 + "\n")
            f.write("    REPORTE DE NOTAS ESTUDIANTILES\n")
            f.write("=" * 40 + "\n\n")
            
            # Promedio general
            f.write(f"Promedio General: {self.promedio_general():.2f}\n\n")
            
            # Promedio por estudiante
            f.write("--- Promedio por Estudiante ---\n")
            promedios_est = self.promedio_por_estudiante()
            for id_est in sorted(promedios_est.keys()):
                f.write(f"ID {id_est}: {promedios_est[id_est]:.2f}\n")
            f.write("\n")
            
            # Promedio por materia
            f.write("--- Promedio por Materia ---\n")
            promedios_mat = self.promedio_por_materia()
            for materia in sorted(promedios_mat.keys()):
                f.write(f"{materia}: {promedios_mat[materia]:.2f}\n")
            f.write("\n")
            
            # Nota máxima y mínima
            nota_max = self.nota_maxima()
            nota_min = self.nota_minima()
            
            if nota_max:
                f.write(f"Nota Máxima: {nota_max.nota:.2f} ")
                f.write(f"(ID {nota_max.id_estudiante} - {nota_max.materia})\n")
            
            if nota_min:
                f.write(f"Nota Mínima: {nota_min.nota:.2f} ")
                f.write(f"(ID {nota_min.id_estudiante} - {nota_min.materia})\n")
        
        print(f"✅ Reporte generado en: {archivo_salida}")


def main():
    """Función principal"""
    # Rutas relativas desde la raíz del repositorio
    archivo_csv = Path('data/estudiantes_notas.csv')
    archivo_reporte = Path('output/reporte_notas.txt')
    
    # Crear gestor y procesar
    gestor = GestorNotas(archivo_csv)
    gestor.cargar_notas()
    
    # Mostrar algunas estadísticas en consola
    print(f"\n📊 Estadísticas:")
    print(f"   Total de notas: {len(gestor.notas)}")
    print(f"   Promedio general: {gestor.promedio_general():.2f}")
    print(f"   Nota máxima: {gestor.nota_maxima().nota:.2f}")
    print(f"   Nota mínima: {gestor.nota_minima().nota:.2f}")
    
    # Generar reporte
    gestor.generar_reporte(archivo_reporte)
    print(f"\n✨ ¡Proceso completado exitosamente!\n")


if __name__ == '__main__':
    main()
