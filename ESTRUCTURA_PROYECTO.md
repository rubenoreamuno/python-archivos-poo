# 📂 Estructura del Proyecto

## 📁 Archivos Principales

- **README.md** - Guía visual completa con tablas, diagramas Mermaid, y ejemplos de código
- **CHEATSHEET.md** - Referencia rápida de una página con patrones POO + archivos
- **.gitignore** - Configurado para ignorar `output/` y archivos temporales

## 📊 Carpeta `data/` - Archivos de Práctica

### CSV (5 archivos)
- `estudiantes.csv` - 10 estudiantes con datos básicos
- `estudiantes_notas.csv` - 15 registros de calificaciones
- `inventario.csv` - 12 productos de tecnología
- `transacciones.csv` - 15 transacciones bancarias
- `productos_dirty.csv` - 9 productos con errores intencionales

### JSON (3 archivos)
- `biblioteca.json` - Biblioteca con 5 libros y préstamos anidados
- `config.json` - Configuración compleja de aplicación
- `empleados.json` - Empresa con 3 departamentos y 7 empleados

### TXT (3 archivos)
- `server.log` - 36 entradas de log de servidor
- `texto_analisis.txt` - Texto sobre programación (1933 caracteres)
- `ventas_formato_fijo.txt` - Ventas con formato de ancho fijo

## 🎯 Carpeta `ejercicios/` - 10 Ejercicios Progresivos

Cada ejercicio tiene:
- `enunciado.md` - Descripción, objetivos, requisitos, diseño sugerido
- `solucion.py` - Código completo, comentado, ejecutable

### Ejercicio 1: Gestor de Notas
- **Nivel:** Básico
- **Temas:** CSV DictReader, @classmethod, estadísticas básicas
- **Archivos:** estudiantes_notas.csv
- **Salida:** reporte_notas.txt

### Ejercicio 2: Inventario con Persistencia JSON
- **Nivel:** Básico-Intermedio
- **Temas:** JSON, CRUD, @property validación, to_dict/from_dict
- **Archivos:** inventario.csv
- **Salida:** inventario.json

### Ejercicio 3: Analizador de Logs
- **Nivel:** Intermedio
- **Temas:** Procesamiento TXT línea por línea, Counter, parseo
- **Archivos:** server.log
- **Salida:** analisis_logs.txt

### Ejercicio 4: Sistema de Biblioteca con Herencia
- **Nivel:** Intermedio
- **Temas:** Herencia, ABC, JSON anidado complejo, polimorfismo
- **Archivos:** biblioteca.json
- **Salida:** reporte_biblioteca.txt

### Ejercicio 5: Sistema Bancario con Excepciones
- **Nivel:** Intermedio
- **Temas:** Excepciones personalizadas, validación, @property
- **Archivos:** transacciones.csv
- **Salida:** reporte_bancario.txt, errores_transacciones.log

### Ejercicio 6: Conversor CSV ↔ JSON
- **Nivel:** Intermedio
- **Temas:** Conversión bidireccional, inferencia de tipos
- **Archivos:** Varios CSV y JSON
- **Salida:** Múltiples conversiones

### Ejercicio 7: Analizador de Frecuencia de Palabras
- **Nivel:** Intermedio
- **Temas:** Procesamiento de texto, Counter, histograma ASCII
- **Archivos:** texto_analisis.txt
- **Salida:** analisis_frecuencias.txt

### Ejercicio 8: Generador de Reportes Multi-Fuente
- **Nivel:** Intermedio-Avanzado
- **Temas:** Integración múltiples formatos, agregación, relacionar datos
- **Archivos:** estudiantes.csv, estudiantes_notas.csv, config.json
- **Salida:** reporte_completo.txt, resumen.json, alertas.txt

### Ejercicio 9: Validador de Datos con Reporte de Errores
- **Nivel:** Avanzado
- **Temas:** Validación robusta, manejo de datos sucios, reportes detallados
- **Archivos:** productos_dirty.csv
- **Salida:** productos_limpios.csv, reporte_errores_validacion.txt

### Ejercicio 10: Sistema CRUD Completo de Empleados
- **Nivel:** Avanzado
- **Temas:** Dataclasses, CRUD completo, búsquedas complejas, estadísticas
- **Archivos:** empleados.json
- **Salida:** empleados_actualizado.json, reporte_empleados_completo.txt

## ✅ Verificación

Todos los ejercicios han sido verificados y ejecutan correctamente:
- Ejecutables desde la raíz del repositorio
- Ejecutables desde su propia carpeta
- Generan salidas en `output/` (gitignored)
- Sin dependencias externas (solo biblioteca estándar)

## 🚀 Uso

```bash
# Ejecutar desde la raíz
python3 ejercicios/01_gestor_notas/solucion.py

# O desde la carpeta del ejercicio
cd ejercicios/01_gestor_notas
python3 solucion.py
```

## 📈 Progresión de Dificultad

1-2: **Básico** - CSV/JSON básico, clases simples
3-4: **Intermedio** - Herencia, estructuras complejas
5-7: **Intermedio** - Excepciones, conversiones, procesamiento
8-10: **Avanzado** - Integración, validación, sistemas completos
