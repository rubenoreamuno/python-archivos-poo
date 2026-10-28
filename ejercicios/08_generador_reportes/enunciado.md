# Ejercicio 8: Generador de Reportes Multi-Fuente

## 📋 Descripción

Desarrollar un sistema que lea múltiples archivos de diferentes formatos (CSV, JSON, TXT), integre la información y genere reportes consolidados.

## 🎯 Objetivos de Aprendizaje

- Integrar múltiples fuentes de datos
- Coordinar lectura de diferentes formatos
- Cruzar información de distintas fuentes
- Generar reportes complejos con múltiples secciones

## 📝 Requisitos Funcionales

1. Leer:
   - `data/estudiantes.csv`
   - `data/estudiantes_notas.csv`
   - `data/config.json` (configuración de límites)
2. Relacionar estudiantes con sus notas por ID
3. Calcular:
   - Promedios ponderados por créditos
   - Estudiantes que superan/no superan nota mínima
   - Ranking de mejores estudiantes
4. Generar:
   - Reporte completo en TXT
   - Resumen ejecutivo en JSON
   - Alertas de estudiantes en riesgo

## 🏗️ Diseño Sugerido

```python
class EstudianteCompleto:
    def __init__(self, datos_basicos, notas):
        # Combinar datos de múltiples fuentes
    
    def promedio_ponderado(self):
        # Calcular promedio con créditos
    
    def esta_en_riesgo(self, nota_minima):
        pass

class GeneradorReportes:
    def __init__(self):
        self.estudiantes = []
        self.config = {}
    
    def cargar_datos(self):
        # Leer todos los archivos
    
    def integrar_datos(self):
        # Combinar información
    
    def generar_reporte_completo(self):
        pass
    
    def generar_resumen_json(self):
        pass
```

## 📤 Salida Esperada

Tres archivos:
- `reporte_completo.txt` - Reporte detallado
- `resumen.json` - Métricas clave en JSON
- `alertas.txt` - Estudiantes en riesgo

## 💡 Tips

- Usa diccionarios para relacionar datos por ID
- `defaultdict` o `collections` puede ayudar
- Separa carga, procesamiento y generación

## ✅ Criterios de Evaluación

- [x] Integración correcta de múltiples fuentes
- [x] Cálculos ponderados correctos
- [x] Reportes bien estructurados
- [x] Código modular y organizado
