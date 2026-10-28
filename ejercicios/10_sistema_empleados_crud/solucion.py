#!/usr/bin/env python3
"""
Ejercicio 10: Sistema CRUD Completo de Empleados
Sistema integral de gestión con CRUD, búsquedas avanzadas y estadísticas
"""

import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict


@dataclass
class Empleado:
    """Modelo de datos para un empleado usando dataclasses"""
    id: str
    nombre: str
    cargo: str
    salario: float
    fecha_ingreso: str
    habilidades: List[str] = field(default_factory=list)
    
    def to_dict(self):
        """Convierte el empleado a diccionario"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, datos):
        """Crea un empleado desde un diccionario"""
        return cls(**datos)
    
    def tiene_habilidad(self, habilidad):
        """Verifica si el empleado tiene una habilidad específica"""
        return any(h.lower() == habilidad.lower() for h in self.habilidades)
    
    def __str__(self):
        return f"{self.id}: {self.nombre} - {self.cargo} (${self.salario:,.2f})"


@dataclass
class Departamento:
    """Modelo de datos para un departamento"""
    id: str
    nombre: str
    empleados: List[Empleado] = field(default_factory=list)
    
    def agregar_empleado(self, empleado):
        """Agrega un empleado al departamento"""
        self.empleados.append(empleado)
    
    def eliminar_empleado(self, id_empleado):
        """Elimina un empleado del departamento"""
        self.empleados = [e for e in self.empleados if e.id != id_empleado]
    
    def buscar_empleado(self, id_empleado):
        """Busca un empleado por ID en este departamento"""
        for empleado in self.empleados:
            if empleado.id == id_empleado:
                return empleado
        return None
    
    def salario_promedio(self):
        """Calcula el salario promedio del departamento"""
        if not self.empleados:
            return 0.0
        return sum(e.salario for e in self.empleados) / len(self.empleados)
    
    def to_dict(self):
        """Convierte el departamento a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'empleados': [e.to_dict() for e in self.empleados]
        }
    
    @classmethod
    def from_dict(cls, datos):
        """Crea un departamento desde un diccionario"""
        empleados = [Empleado.from_dict(e) for e in datos.get('empleados', [])]
        return cls(
            id=datos['id'],
            nombre=datos['nombre'],
            empleados=empleados
        )
    
    def __str__(self):
        return f"{self.nombre} ({len(self.empleados)} empleados)"


class SistemaEmpleados:
    """Sistema completo de gestión de empleados"""
    
    def __init__(self):
        self.empresa = ""
        self.departamentos: Dict[str, Departamento] = {}
    
    def cargar_desde_json(self, archivo):
        """Carga datos desde JSON con estructura anidada"""
        archivo = Path(archivo)
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                
                self.empresa = datos.get('empresa', '')
                
                for depto_dict in datos.get('departamentos', []):
                    depto = Departamento.from_dict(depto_dict)
                    self.departamentos[depto.id] = depto
            
            print(f"✅ Sistema cargado: {len(self.departamentos)} departamentos")
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {archivo}")
            raise
    
    def guardar_json(self, archivo):
        """Guarda los datos en JSON"""
        archivo = Path(archivo)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        datos = {
            'empresa': self.empresa,
            'departamentos': [depto.to_dict() for depto in self.departamentos.values()]
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Sistema guardado: {archivo}")
    
    # ========== CRUD: CREATE ==========
    
    def crear_empleado(self, id_depto, empleado):
        """Agrega un nuevo empleado a un departamento"""
        if id_depto not in self.departamentos:
            print(f"❌ Departamento {id_depto} no existe")
            return False
        
        # Verificar que el ID no exista
        if self.buscar_empleado(empleado.id):
            print(f"❌ Ya existe un empleado con ID {empleado.id}")
            return False
        
        self.departamentos[id_depto].agregar_empleado(empleado)
        print(f"✅ Empleado {empleado.id} agregado a {self.departamentos[id_depto].nombre}")
        return True
    
    # ========== CRUD: READ ==========
    
    def buscar_empleado(self, id_empleado) -> Optional[Empleado]:
        """Busca un empleado por ID en todos los departamentos"""
        for depto in self.departamentos.values():
            empleado = depto.buscar_empleado(id_empleado)
            if empleado:
                return empleado
        return None
    
    def buscar_por_nombre(self, nombre):
        """Busca empleados por nombre (búsqueda parcial)"""
        resultados = []
        nombre_lower = nombre.lower()
        
        for depto in self.departamentos.values():
            for empleado in depto.empleados:
                if nombre_lower in empleado.nombre.lower():
                    resultados.append((depto.nombre, empleado))
        
        return resultados
    
    def buscar_por_cargo(self, cargo):
        """Busca empleados por cargo"""
        resultados = []
        cargo_lower = cargo.lower()
        
        for depto in self.departamentos.values():
            for empleado in depto.empleados:
                if cargo_lower in empleado.cargo.lower():
                    resultados.append((depto.nombre, empleado))
        
        return resultados
    
    def buscar_por_habilidad(self, habilidad):
        """Busca empleados que tienen una habilidad específica"""
        resultados = []
        
        for depto in self.departamentos.values():
            for empleado in depto.empleados:
                if empleado.tiene_habilidad(habilidad):
                    resultados.append((depto.nombre, empleado))
        
        return resultados
    
    def filtrar_por_rango_salarial(self, min_sal, max_sal):
        """Filtra empleados por rango salarial"""
        resultados = []
        
        for depto in self.departamentos.values():
            for empleado in depto.empleados:
                if min_sal <= empleado.salario <= max_sal:
                    resultados.append((depto.nombre, empleado))
        
        return resultados
    
    def listar_por_departamento(self, id_depto):
        """Lista todos los empleados de un departamento"""
        if id_depto not in self.departamentos:
            return []
        return self.departamentos[id_depto].empleados
    
    # ========== CRUD: UPDATE ==========
    
    def actualizar_empleado(self, id_empleado, **kwargs):
        """Actualiza campos de un empleado"""
        empleado = self.buscar_empleado(id_empleado)
        if not empleado:
            print(f"❌ Empleado {id_empleado} no encontrado")
            return False
        
        # Actualizar campos permitidos
        if 'salario' in kwargs:
            empleado.salario = float(kwargs['salario'])
        if 'cargo' in kwargs:
            empleado.cargo = kwargs['cargo']
        if 'habilidades' in kwargs:
            empleado.habilidades = kwargs['habilidades']
        if 'nombre' in kwargs:
            empleado.nombre = kwargs['nombre']
        
        print(f"✅ Empleado {id_empleado} actualizado")
        return True
    
    # ========== CRUD: DELETE ==========
    
    def eliminar_empleado(self, id_empleado):
        """Elimina un empleado del sistema"""
        for depto in self.departamentos.values():
            if depto.buscar_empleado(id_empleado):
                depto.eliminar_empleado(id_empleado)
                print(f"✅ Empleado {id_empleado} eliminado")
                return True
        
        print(f"❌ Empleado {id_empleado} no encontrado")
        return False
    
    # ========== ESTADÍSTICAS ==========
    
    def total_empleados(self):
        """Total de empleados en la empresa"""
        return sum(len(depto.empleados) for depto in self.departamentos.values())
    
    def salario_promedio_por_departamento(self):
        """Calcula salario promedio de cada departamento"""
        return {
            depto.nombre: depto.salario_promedio()
            for depto in self.departamentos.values()
        }
    
    def salario_promedio_empresa(self):
        """Calcula salario promedio de toda la empresa"""
        total_empleados = self.total_empleados()
        if total_empleados == 0:
            return 0.0
        
        suma_salarios = sum(
            sum(e.salario for e in depto.empleados)
            for depto in self.departamentos.values()
        )
        return suma_salarios / total_empleados
    
    def estadisticas_habilidades(self):
        """Cuenta cuántos empleados tienen cada habilidad"""
        from collections import Counter
        
        todas_habilidades = []
        for depto in self.departamentos.values():
            for empleado in depto.empleados:
                todas_habilidades.extend(empleado.habilidades)
        
        return Counter(todas_habilidades)
    
    # ========== REPORTES ==========
    
    def generar_reporte(self, archivo_salida):
        """Genera un reporte completo del sistema"""
        archivo = Path(archivo_salida)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("=" * 70 + "\n")
            f.write("          SISTEMA DE GESTIÓN DE EMPLEADOS\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Empresa: {self.empresa}\n")
            f.write(f"Total de empleados: {self.total_empleados()}\n")
            f.write(f"Número de departamentos: {len(self.departamentos)}\n")
            f.write(f"Salario promedio empresa: ${self.salario_promedio_empresa():,.2f}\n\n")
            
            # Departamentos
            f.write("--- Departamentos y Empleados ---\n\n")
            for depto in self.departamentos.values():
                f.write(f"📂 {depto.nombre}\n")
                f.write(f"   Total empleados: {len(depto.empleados)}\n")
                f.write(f"   Salario promedio: ${depto.salario_promedio():,.2f}\n")
                f.write(f"   Empleados:\n")
                
                for empleado in sorted(depto.empleados, key=lambda e: e.nombre):
                    f.write(f"     • {empleado.nombre} ({empleado.id})\n")
                    f.write(f"       Cargo: {empleado.cargo}\n")
                    f.write(f"       Salario: ${empleado.salario:,.2f}\n")
                    f.write(f"       Habilidades: {', '.join(empleado.habilidades)}\n")
                f.write("\n")
            
            # Habilidades más comunes
            f.write("--- Habilidades Más Comunes ---\n")
            habilidades = self.estadisticas_habilidades()
            for habilidad, cantidad in habilidades.most_common(10):
                f.write(f"  {habilidad}: {cantidad} empleados\n")
        
        print(f"📊 Reporte generado: {archivo}")


def main():
    """Función principal - demostración del sistema"""
    print("👥 SISTEMA DE GESTIÓN DE EMPLEADOS\n")
    
    # Cargar sistema
    sistema = SistemaEmpleados()
    sistema.cargar_desde_json('data/empleados.json')
    
    print(f"\n🏢 {sistema.empresa}")
    print(f"👥 Total de empleados: {sistema.total_empleados()}")
    print(f"📊 Departamentos: {len(sistema.departamentos)}")
    
    # ========== Demostrar CRUD ==========
    print("\n" + "=" * 50)
    print("DEMOSTRANDO OPERACIONES CRUD")
    print("=" * 50)
    
    # CREATE
    print("\n--- CREATE: Agregar nuevo empleado ---")
    nuevo_empleado = Empleado(
        id='EMP008',
        nombre='Patricia Gómez',
        cargo='QA Engineer',
        salario=2300.00,
        fecha_ingreso='2024-01-15',
        habilidades=['Testing', 'Selenium', 'Python']
    )
    sistema.crear_empleado('DEP001', nuevo_empleado)
    
    # READ
    print("\n--- READ: Buscar empleado ---")
    empleado = sistema.buscar_empleado('EMP001')
    if empleado:
        print(f"Encontrado: {empleado}")
    
    # UPDATE
    print("\n--- UPDATE: Actualizar salario ---")
    sistema.actualizar_empleado('EMP002', salario=2200.00, cargo='Desarrollador Mid')
    
    # DELETE (comentado para no alterar los datos)
    # print("\n--- DELETE: Eliminar empleado ---")
    # sistema.eliminar_empleado('EMP005')
    
    # ========== Búsquedas Avanzadas ==========
    print("\n" + "=" * 50)
    print("BÚSQUEDAS AVANZADAS")
    print("=" * 50)
    
    print("\n🔍 Empleados con habilidad 'Python':")
    resultados = sistema.buscar_por_habilidad('Python')
    for depto, emp in resultados:
        print(f"   • {emp.nombre} ({depto})")
    
    print("\n💰 Empleados con salario $2000-$3000:")
    resultados = sistema.filtrar_por_rango_salarial(2000, 3000)
    for depto, emp in resultados:
        print(f"   • {emp.nombre}: ${emp.salario:,.2f} ({depto})")
    
    # ========== Estadísticas ==========
    print("\n" + "=" * 50)
    print("ESTADÍSTICAS")
    print("=" * 50)
    
    print("\n📊 Salario promedio por departamento:")
    promedios = sistema.salario_promedio_por_departamento()
    for depto, promedio in promedios.items():
        print(f"   • {depto}: ${promedio:,.2f}")
    
    print(f"\n💵 Salario promedio empresa: ${sistema.salario_promedio_empresa():,.2f}")
    
    print("\n🎯 Top 5 habilidades más comunes:")
    habilidades = sistema.estadisticas_habilidades()
    for habilidad, cantidad in habilidades.most_common(5):
        print(f"   • {habilidad}: {cantidad} empleados")
    
    # ========== Guardar y Generar Reportes ==========
    print("\n" + "=" * 50)
    print("GENERANDO REPORTES")
    print("=" * 50 + "\n")
    
    sistema.guardar_json('output/empleados_actualizado.json')
    sistema.generar_reporte('output/reporte_empleados_completo.txt')
    
    print(f"\n✨ Demostración completada!\n")


if __name__ == '__main__':
    main()
