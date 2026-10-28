# Ejercicio 9: Validador de Datos CSV con Reporte de Errores

## 📋 Descripción

Desarrollar un sistema de validación de datos que procese archivos CSV, detecte errores, valide tipos y formatos, y genere reportes detallados de problemas encontrados.

## 🎯 Objetivos de Aprendizaje

- Implementar validaciones robustas de datos
- Procesar datos "sucios" (con errores intencionales)
- Generar reportes de errores detallados
- Usar excepciones para control de flujo
- Separar datos válidos de inválidos

## 📝 Requisitos Funcionales

1. Leer `data/productos_dirty.csv` (contiene errores intencionales)
2. Validar cada fila:
   - `codigo`: no vacío, formato correcto
   - `nombre`: no vacío, longitud mínima
   - `precio`: número positivo
   - `stock`: entero no negativo
3. Clasificar filas en:
   - Válidas: pasan todas las validaciones
   - Inválidas: tienen uno o más errores
4. Generar:
   - CSV con datos limpios (solo válidos)
   - Reporte de errores detallado
   - Estadísticas de validación

## 🏗️ Diseño Sugerido

```python
class ErrorValidacion(Exception):
    """Excepción para errores de validación"""
    pass

class ValidadorProducto:
    @staticmethod
    def validar_codigo(codigo):
        if not codigo or codigo.strip() == '':
            raise ErrorValidacion("Código vacío")
    
    @staticmethod
    def validar_precio(precio_str):
        try:
            precio = float(precio_str)
            if precio < 0:
                raise ErrorValidacion("Precio negativo")
            return precio
        except ValueError:
            raise ErrorValidacion(f"Precio inválido: {precio_str}")
    
    # Más validadores...

class ValidadorCSV:
    def __init__(self, archivo_entrada):
        self.filas_validas = []
        self.filas_invalidas = []
        self.errores = []
    
    def validar_fila(self, fila, num_fila):
        errores_fila = []
        # Validar cada campo
        # Retornar (valida, fila_limpia, errores)
    
    def procesar_archivo(self):
        # Leer y validar cada fila
    
    def generar_csv_limpio(self, archivo_salida):
        pass
    
    def generar_reporte_errores(self, archivo_salida):
        pass
```

## 📤 Salida Esperada

```
========================================
    REPORTE DE VALIDACIÓN DE DATOS
========================================

Total de filas procesadas: 9
Filas válidas: 5 (55.6%)
Filas inválidas: 4 (44.4%)

--- Errores Encontrados ---

Fila 2:
  ❌ Campo 'precio': Precio inválido: invalid_price

Fila 4:
  ❌ Campo 'stock': Stock negativo: -5

Fila 5:
  ❌ Campo 'nombre': Nombre vacío
...
```

## 💡 Tips

- Usa `try-except` para cada validación
- Acumula todos los errores de una fila antes de rechazarla
- Mantén registro de número de línea para debugging

## ✅ Criterios de Evaluación

- [x] Todas las validaciones implementadas
- [x] Detección correcta de errores
- [x] CSV limpio generado correctamente
- [x] Reporte de errores detallado y útil
- [x] Código robusto y mantenible
