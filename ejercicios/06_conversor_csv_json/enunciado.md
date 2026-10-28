# Ejercicio 6: Conversor CSV ↔ JSON

## 📋 Descripción

Desarrollar una herramienta de conversión bidireccional entre formatos CSV y JSON, con validación y transformación de datos.

## 🎯 Objetivos de Aprendizaje

- Trabajar simultáneamente con CSV y JSON
- Implementar conversiones de formato
- Manejar tipos de datos correctamente
- Diseñar clases utilitarias reutilizables

## 📝 Requisitos Funcionales

1. Convertir CSV → JSON (con inferencia de tipos)
2. Convertir JSON → CSV (aplanar estructuras simples)
3. Preservar tipos de datos (números vs strings)
4. Permitir configuración (indentación, delimitador, encoding)
5. Generar ambas conversiones desde datos de ejemplo

## 🏗️ Diseño Sugerido

```python
class ConversorArchivos:
    @staticmethod
    def csv_a_json(archivo_csv, archivo_json, inferir_tipos=True):
        """Convierte CSV a JSON"""
    
    @staticmethod
    def json_a_csv(archivo_json, archivo_csv, campos=None):
        """Convierte JSON a CSV"""
    
    @staticmethod
    def inferir_tipo(valor):
        """Intenta convertir string a int/float"""
        # Retorna el valor con el tipo correcto
```

## 📤 Salida Esperada

Archivos convertidos correctamente en ambos formatos.

## 💡 Tips

- Usa `try-except` para inferencia de tipos
- JSON puede ser lista de objetos o objeto con listas
- CSV es siempre tabular (2D)

## ✅ Criterios de Evaluación

- [x] Conversión CSV→JSON correcta
- [x] Conversión JSON→CSV correcta
- [x] Tipos de datos preservados
- [x] Código limpio y reutilizable
