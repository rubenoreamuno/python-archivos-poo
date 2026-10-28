# Ejercicio 10: Sistema CRUD Completo de Empleados

## 📋 Descripción

Desarrollar un sistema completo de gestión de empleados con operaciones CRUD, búsquedas avanzadas, filtros, y persistencia en JSON. Este ejercicio integra todos los conceptos aprendidos.

## 🎯 Objetivos de Aprendizaje

- Implementar CRUD completo (Create, Read, Update, Delete)
- Trabajar con JSON anidado complejo
- Implementar búsquedas y filtros múltiples
- Usar dataclasses para modelos limpios
- Diseñar API de alto nivel

## 📝 Requisitos Funcionales

1. Cargar `data/empleados.json` (estructura anidada con departamentos)
2. Implementar CRUD completo:
   - **Create**: Agregar nuevo empleado a un departamento
   - **Read**: Buscar por ID, nombre, departamento, cargo
   - **Update**: Actualizar salario, cargo, habilidades
   - **Delete**: Eliminar empleado
3. Operaciones avanzadas:
   - Listar empleados por rango salarial
   - Buscar por habilidad
   - Calcular estadísticas (salario promedio por depto)
   - Generar organigrama
4. Persistencia: Guardar cambios en JSON

## 🏗️ Diseño Sugerido

```python
from dataclasses import dataclass, field, asdict
from typing import List

@dataclass
class Empleado:
    id: str
    nombre: str
    cargo: str
    salario: float
    fecha_ingreso: str
    habilidades: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, datos):
        return cls(**datos)

@dataclass
class Departamento:
    id: str
    nombre: str
    empleados: List[Empleado] = field(default_factory=list)

class SistemaEmpleados:
    def __init__(self):
        self.empresa = ""
        self.departamentos = {}
    
    # CRUD
    def crear_empleado(self, id_depto, empleado):
        pass
    
    def buscar_empleado(self, id_empleado):
        pass
    
    def actualizar_empleado(self, id_empleado, **kwargs):
        pass
    
    def eliminar_empleado(self, id_empleado):
        pass
    
    # Búsquedas avanzadas
    def buscar_por_nombre(self, nombre):
        pass
    
    def buscar_por_habilidad(self, habilidad):
        pass
    
    def filtrar_por_rango_salarial(self, min_sal, max_sal):
        pass
    
    # Estadísticas
    def salario_promedio_por_departamento(self):
        pass
    
    def total_empleados(self):
        pass
```

## 📤 Salida Esperada

```
========================================
    SISTEMA DE GESTIÓN DE EMPLEADOS
========================================

Empresa: TechCorp S.A.
Total de empleados: 7
Departamentos: 3

--- Operaciones CRUD ---
✅ Empleado agregado: EMP008
✅ Empleado actualizado: EMP001
✅ Empleado eliminado: EMP005

--- Búsquedas ---
Empleados con Python: 3 resultados
Empleados con salario $2000-$3000: 2 resultados

--- Estadísticas por Departamento ---
Desarrollo: $3,500.00 promedio (3 empleados)
Recursos Humanos: $3,250.00 promedio (2 empleados)
Ventas: $3,650.00 promedio (2 empleados)
```

## 💡 Tips

- `dataclasses` simplifican modelos de datos
- Usa `asdict()` para serialización fácil
- Diccionarios anidados para búsqueda rápida
- Conserva la estructura jerárquica en JSON

## ✅ Criterios de Evaluación

- [x] CRUD completo funcional
- [x] Búsquedas y filtros eficientes
- [x] Manejo correcto de JSON anidado
- [x] Estadísticas correctas
- [x] Código limpio con dataclasses
- [x] Persistencia correcta
