# Ejercicio 1: Gestor de Notas Estudiantiles

## 📋 Descripción

Desarrollar un sistema de gestión de notas que permita cargar calificaciones desde un archivo CSV, calcular estadísticas y generar reportes.

## 🎯 Objetivos de Aprendizaje

- Leer archivos CSV con `csv.DictReader`
- Crear clases para representar entidades
- Implementar métodos `@classmethod` para constructores alternativos
- Calcular estadísticas con listas de objetos
- Escribir resultados en archivos de texto

## 📝 Requisitos Funcionales

1. Leer el archivo `data/estudiantes_notas.csv`
2. Crear objetos `Nota` a partir de cada fila
3. Implementar un `GestorNotas` que contenga la lista de notas
4. Calcular:
   - Promedio general de todas las notas
   - Promedio por estudiante
   - Promedio por materia
   - Nota máxima y mínima
5. Generar un reporte en `output/reporte_notas.txt`

## 🏗️ Diseño Sugerido

### Clase `Nota`

```python
class Nota:
    def __init__(self, id_estudiante, materia, nota, creditos, periodo):
        # Atributos
    
    @classmethod
    def from_csv_row(cls, fila):
        # Constructor desde diccionario CSV
    
    def __str__(self):
        # Representación legible
```

### Clase `GestorNotas`

```python
class GestorNotas:
    def __init__(self, archivo_csv):
        self.notas = []
    
    def cargar_notas(self):
        # Leer CSV y crear objetos Nota
    
    def promedio_general(self):
        # Calcular promedio de todas las notas
    
    def promedio_por_estudiante(self):
        # Retornar dict {id_estudiante: promedio}
    
    def promedio_por_materia(self):
        # Retornar dict {materia: promedio}
    
    def nota_maxima(self):
        # Retornar la nota más alta
    
    def nota_minima(self):
        # Retornar la nota más baja
    
    def generar_reporte(self, archivo_salida):
        # Escribir reporte en TXT
```

## 📤 Salida Esperada

Archivo `output/reporte_notas.txt`:

```
========================================
    REPORTE DE NOTAS ESTUDIANTILES
========================================

Promedio General: 8.95

--- Promedio por Estudiante ---
ID 1001: 9.40
ID 1002: 8.23
ID 1003: 9.77
ID 1004: 8.10
ID 1005: 9.03

--- Promedio por Materia ---
Cálculo I: 8.63
Programación I: 9.63
Física I: 8.40
...

Nota Máxima: 10.00 (ID 1001 - Programación I)
Nota Mínima: 6.50 (ID 1004 - Cálculo II)
```

## 💡 Tips

- Usa `pathlib.Path` para rutas multiplataforma
- Crea el directorio `output/` si no existe con `mkdir(exist_ok=True)`
- Agrupa notas por estudiante/materia usando diccionarios
- Maneja excepciones `FileNotFoundError` y `ValueError`

## ✅ Criterios de Evaluación

- [x] Lectura correcta del CSV
- [x] Clases bien estructuradas con métodos apropiados
- [x] Cálculos estadísticos correctos
- [x] Reporte generado en formato legible
- [x] Código limpio y comentado
- [x] Manejo de excepciones
