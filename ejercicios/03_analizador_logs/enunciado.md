# Ejercicio 3: Analizador de Logs de Servidor

## 📋 Descripción

Desarrollar un analizador que procese archivos de log de servidor, extraiga información relevante, calcule estadísticas y genere reportes.

## 🎯 Objetivos de Aprendizaje

- Leer archivos de texto línea por línea
- Parsear texto con formato estructurado
- Usar diccionarios para contar frecuencias
- Procesar grandes archivos eficientemente
- Generar reportes estadísticos

## 📝 Requisitos Funcionales

1. Leer el archivo `data/server.log`
2. Parsear cada línea extrayendo: fecha, hora, nivel (INFO/WARNING/ERROR), mensaje
3. Calcular:
   - Total de eventos por nivel
   - Eventos por hora del día
   - Top 5 mensajes más frecuentes
   - Porcentaje de errores vs total
4. Identificar patrones críticos (errores, conexiones fallidas, etc.)
5. Generar reporte en `output/analisis_logs.txt`

## 🏗️ Diseño Sugerido

### Clase `EntradaLog`

```python
class EntradaLog:
    def __init__(self, fecha, hora, nivel, mensaje):
        # Atributos
    
    @classmethod
    def parsear_linea(cls, linea):
        # Parsear línea de log
        # Formato: "2024-01-20 08:15:23 INFO Server started"
    
    @property
    def es_error(self):
        return self.nivel == 'ERROR'
```

### Clase `AnalizadorLogs`

```python
class AnalizadorLogs:
    def __init__(self, archivo_log):
        self.entradas = []
    
    def cargar_log(self):
        # Leer y parsear línea por línea
    
    def contar_por_nivel(self):
        # {nivel: cantidad}
    
    def contar_por_hora(self):
        # {hora: cantidad}
    
    def mensajes_frecuentes(self, top_n=5):
        # Lista de (mensaje, cantidad)
    
    def porcentaje_errores(self):
        pass
    
    def generar_reporte(self, archivo_salida):
        pass
```

## 📤 Salida Esperada

```
========================================
    ANÁLISIS DE LOGS DE SERVIDOR
========================================

Total de eventos: 35

--- Eventos por Nivel ---
INFO: 25 (71.4%)
WARNING: 7 (20.0%)
ERROR: 3 (8.6%)

--- Eventos por Hora ---
08:00: 22 eventos
09:00: 8 eventos
...

--- Top 5 Mensajes Más Frecuentes ---
1. GET /api/... - 200 OK (8 veces)
2. Database connection established (3 veces)
...

⚠️ ALERTAS:
- 3 errores detectados (8.6% del total)
- 2 conexiones de BD fallidas
```

## 💡 Tips

- Usa `split()` para parsear líneas
- `collections.Counter` puede ayudar con frecuencias
- Itera línea por línea para eficiencia con archivos grandes

## ✅ Criterios de Evaluación

- [x] Parseo correcto de cada línea
- [x] Estadísticas precisas
- [x] Identificación de patrones críticos
- [x] Reporte bien formateado
