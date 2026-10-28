# Ejercicio 7: Analizador de Frecuencia de Palabras

## 📋 Descripción

Desarrollar un analizador de texto que procese archivos, cuente frecuencias de palabras, identifique patrones y genere estadísticas lingüísticas.

## 🎯 Objetivos de Aprendizaje

- Procesar texto: limpieza, normalización, tokenización
- Usar `collections.Counter` eficientemente
- Calcular estadísticas de texto
- Generar visualizaciones textuales (histogramas ASCII)

## 📝 Requisitos Funcionales

1. Leer `data/texto_analisis.txt`
2. Procesar texto:
   - Convertir a minúsculas
   - Eliminar puntuación
   - Separar en palabras
   - Filtrar palabras vacías (stopwords)
3. Calcular:
   - Top 10 palabras más frecuentes
   - Total de palabras únicas
   - Longitud promedio de palabras
   - Palabras que aparecen solo una vez
4. Generar reporte con histograma ASCII

## 🏗️ Diseño Sugerido

```python
from collections import Counter

class AnalizadorTexto:
    def __init__(self, archivo_texto):
        self.texto = ""
        self.palabras = []
        self.stopwords = set(['el', 'la', 'de', 'y', 'a', ...])
    
    def cargar_texto(self):
        pass
    
    def limpiar_texto(self):
        # Eliminar puntuación, minúsculas
    
    def tokenizar(self):
        # Separar en palabras
    
    def filtrar_stopwords(self):
        pass
    
    def contar_frecuencias(self):
        return Counter(self.palabras)
    
    def top_palabras(self, n=10):
        pass
    
    def generar_histograma_ascii(self, frecuencias, max_barras=20):
        # Histograma con caracteres
```

## 📤 Salida Esperada

```
========================================
   ANÁLISIS DE FRECUENCIA DE PALABRAS
========================================

Total de palabras: 245
Palabras únicas: 87
Longitud promedio: 6.8 caracteres

--- Top 10 Palabras Más Frecuentes ---

1. programación    ████████████████████ 12
2. python          ████████████████     10
3. archivos        █████████████        8
4. datos           ███████████          7
...

--- Palabras Únicas (solo 1 aparición) ---
Total: 45 palabras
```

## 💡 Tips

- `str.translate()` para eliminar puntuación
- `collections.Counter` tiene `.most_common()`
- Normaliza antes de contar

## ✅ Criterios de Evaluación

- [x] Procesamiento de texto correcto
- [x] Estadísticas precisas
- [x] Histograma ASCII bien formateado
- [x] Código eficiente con Counter
