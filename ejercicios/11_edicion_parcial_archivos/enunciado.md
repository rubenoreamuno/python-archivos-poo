# Ejercicio 11: Edición Parcial de Archivos (In-Place)

## 📋 Descripción

Demostrar técnicas avanzadas de edición parcial de archivos sin reescribir todo el contenido, usando `seek()`, `tell()`, y modos de lectura/escritura combinados.

## 🎯 Objetivos de Aprendizaje

- Usar `seek()` y `tell()` para posicionarse en archivos
- Modo `r+` para lectura y escritura simultánea
- Editar líneas específicas sin reescribir todo
- Entender cuándo usar edición parcial vs. reescritura completa
- Limitaciones y riesgos de edición in-place

## ⚠️ Advertencias Importantes

**La edición in-place tiene riesgos:**
- ❌ Si se interrumpe, el archivo puede quedar corrupto
- ❌ No funciona bien si cambia el tamaño del contenido
- ❌ Difícil de deshacer si hay errores
- ✅ Solo recomendada para archivos de **tamaño fijo** o cambios exactos

**Preferir siempre:**
```python
# ✅ RECOMENDADO: Seguro, atómico
leer_archivo() → modificar_en_memoria() → escribir_nuevo_archivo()
```

**Usar edición parcial solo cuando:**
- El archivo es muy grande (GB+)
- Se modifican solo bytes/líneas específicas
- El contenido nuevo tiene exactamente el mismo tamaño

## 📝 Técnicas Demostradas

### 1. Métodos de Posicionamiento

```python
# seek(offset, whence)
# whence: 0=inicio, 1=actual, 2=final

f.seek(0)        # Ir al inicio
f.seek(10)       # Ir al byte 10
f.seek(-5, 2)    # Ir 5 bytes antes del final
pos = f.tell()   # Obtener posición actual
```

### 2. Modo `r+` (Lectura + Escritura)

```python
with open('archivo.txt', 'r+', encoding='utf-8') as f:
    contenido = f.read()
    f.seek(0)  # Volver al inicio
    f.write(nuevo_contenido)
    f.truncate()  # Cortar si el nuevo es más corto
```

### 3. Actualizar Línea Específica (Mismo Tamaño)

```python
# Solo funciona si la nueva línea tiene EXACTAMENTE el mismo tamaño
with open('datos.txt', 'r+') as f:
    lineas = f.readlines()
    lineas[2] = 'Nueva línea del mismo tamaño\n'
    f.seek(0)
    f.writelines(lineas)
```

## 🏗️ Casos de Uso

### Caso 1: Actualizar Metadatos en Archivo de Log
- Archivo: `server.log`
- Acción: Cambiar nivel de log específico (INFO → WARN)
- Condición: Mismo número de caracteres

### Caso 2: Modificar CSV - Campo Numérico
- Archivo: Inventario con campos de ancho fijo
- Acción: Incrementar stock en 1
- Condición: Números con padding

### Caso 3: Edición Binaria de Configuración
- Archivo: Configuración binaria
- Acción: Cambiar flag específico
- Condición: Posición exacta conocida

## 💡 Comparación

| Aspecto | Reescritura Completa | Edición Parcial |
|---------|---------------------|-----------------|
| **Seguridad** | ✅ Alta (original intacto hasta el final) | ⚠️ Baja (riesgo de corrupción) |
| **Velocidad (archivos pequeños)** | ✅ Rápida | ⚠️ Similar o más lenta |
| **Velocidad (archivos grandes)** | ❌ Lenta (lee/escribe todo) | ✅ Rápida (solo cambios) |
| **Flexibilidad** | ✅ Cambios de cualquier tamaño | ❌ Solo mismo tamaño o menor |
| **Atomicidad** | ✅ Sí (con rename) | ❌ No |
| **Complejidad** | ✅ Simple | ⚠️ Compleja |

## 🎓 Recomendación Pedagógica

Para estudiantes:
1. **Aprender primero** el patrón leer→modificar→escribir (ejercicios 1-10)
2. **Luego** entender edición parcial como optimización avanzada
3. **Preferir siempre** reescritura completa a menos que haya razón específica
4. **En producción**: Usar bibliotecas especializadas para edición in-place segura

## ✅ Criterios de Evaluación

- [x] Entender `seek()` y `tell()`
- [x] Saber cuándo NO usar edición parcial
- [x] Implementar edición segura con respaldo
- [x] Manejar errores y rollback
