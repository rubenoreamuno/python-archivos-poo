#!/usr/bin/env python3
"""
Ejercicio 8: Generador de Reportes Multi-Fuente
Integración de múltiples archivos para generar reportes consolidados
"""

import csv
import json
from pathlib import Path
from collections import defaultdict


class Nota:
    """Representa una nota individual"""
    
    def __init__(self, materia, nota, creditos, periodo):
        self.materia = materia
        self.nota = float(nota)
        self.creditos = int(creditos)
        self.periodo = periodo
    
    def __str__(self):
        return f"{self.materia}: {self.nota} ({self.creditos} créditos)"


class EstudianteCompleto:
    """Estudiante con datos básicos y notas"""
    
    def __init__(self, id_estudiante, nombre, apellido, edad, carrera, semestre):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.edad = int(edad)
        self.carrera = carrera
        self.semestre = int(semestre)
        self.notas = []
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def agregar_nota(self, nota):
        """Agrega una nota al estudiante"""
        self.notas.append(nota)
    
    def promedio_simple(self):
        """Calcula promedio aritmético simple"""
        if not self.notas:
            return 0.0
        return sum(n.nota for n in self.notas) / len(self.notas)
    
    def promedio_ponderado(self):
        """Calcula promedio ponderado por créditos"""
        if not self.notas:
            return 0.0
        
        suma_ponderada = sum(n.nota * n.creditos for n in self.notas)
        total_creditos = sum(n.creditos for n in self.notas)
        
        return suma_ponderada / total_creditos if total_creditos > 0 else 0.0
    
    def total_creditos(self):
        """Total de créditos cursados"""
        return sum(n.creditos for n in self.notas)
    
    def esta_en_riesgo(self, nota_minima):
        """Verifica si el promedio está por debajo del mínimo"""
        return self.promedio_ponderado() < nota_minima
    
    def to_dict(self):
        """Convierte a diccionario para JSON"""
        return {
            'id': self.id,
            'nombre_completo': self.nombre_completo,
            'edad': self.edad,
            'carrera': self.carrera,
            'semestre': self.semestre,
            'promedio_ponderado': round(self.promedio_ponderado(), 2),
            'total_creditos': self.total_creditos(),
            'cantidad_materias': len(self.notas)
        }
    
    def __str__(self):
        return f"{self.nombre_completo} ({self.id}) - {self.carrera}"


class GeneradorReportes:
    """Sistema generador de reportes multi-fuente"""
    
    def __init__(self):
        self.estudiantes = {}  # {id: EstudianteCompleto}
        self.config = {}
    
    def cargar_estudiantes(self, archivo_csv):
        """Carga datos básicos de estudiantes"""
        archivo = Path(archivo_csv)
        try:
            with open(archivo, 'r', encoding='utf-8', newline='') as f:
                lector = csv.DictReader(f)
                for i, fila in enumerate(lector, 1001):
                    id_est = str(i)
                    estudiante = EstudianteCompleto(
                        id_estudiante=id_est,
                        nombre=fila['nombre'],
                        apellido=fila['apellido'],
                        edad=fila['edad'],
                        carrera=fila['carrera'],
                        semestre=fila['semestre']
                    )
                    self.estudiantes[id_est] = estudiante
            
            print(f"✅ Cargados {len(self.estudiantes)} estudiantes")
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {archivo}")
            raise
    
    def cargar_notas(self, archivo_csv):
        """Carga notas y las asocia a estudiantes"""
        archivo = Path(archivo_csv)
        notas_cargadas = 0
        notas_sin_estudiante = 0
        
        try:
            with open(archivo, 'r', encoding='utf-8', newline='') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    id_est = fila['id_estudiante']
                    
                    if id_est in self.estudiantes:
                        nota = Nota(
                            materia=fila['materia'],
                            nota=fila['nota'],
                            creditos=fila['creditos'],
                            periodo=fila['periodo']
                        )
                        self.estudiantes[id_est].agregar_nota(nota)
                        notas_cargadas += 1
                    else:
                        notas_sin_estudiante += 1
            
            print(f"✅ Cargadas {notas_cargadas} notas")
            if notas_sin_estudiante > 0:
                print(f"⚠️  {notas_sin_estudiante} notas sin estudiante asociado")
                
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {archivo}")
            raise
    
    def cargar_configuracion(self, archivo_json):
        """Carga configuración desde JSON"""
        archivo = Path(archivo_json)
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"✅ Configuración cargada")
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {archivo}")
            raise
    
    def ranking_estudiantes(self, top_n=10):
        """Retorna los N mejores estudiantes por promedio"""
        estudiantes_con_notas = [
            est for est in self.estudiantes.values()
            if len(est.notas) > 0
        ]
        return sorted(
            estudiantes_con_notas,
            key=lambda e: e.promedio_ponderado(),
            reverse=True
        )[:top_n]
    
    def estudiantes_en_riesgo(self):
        """Retorna estudiantes por debajo de la nota mínima"""
        nota_minima = self.config.get('limites', {}).get('nota_minima_aprobacion', 6.0)
        return [
            est for est in self.estudiantes.values()
            if len(est.notas) > 0 and est.esta_en_riesgo(nota_minima)
        ]
    
    def generar_reporte_completo(self, archivo_salida):
        """Genera reporte detallado en texto"""
        archivo = Path(archivo_salida)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        nota_minima = self.config.get('limites', {}).get('nota_minima_aprobacion', 6.0)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("=" * 70 + "\n")
            f.write("              REPORTE ACADÉMICO CONSOLIDADO\n")
            f.write("=" * 70 + "\n\n")
            
            # Información general
            f.write("--- Información General ---\n")
            f.write(f"Total de estudiantes: {len(self.estudiantes)}\n")
            estudiantes_con_notas = [e for e in self.estudiantes.values() if e.notas]
            f.write(f"Estudiantes con notas: {len(estudiantes_con_notas)}\n")
            f.write(f"Nota mínima de aprobación: {nota_minima}\n\n")
            
            # Ranking top 10
            f.write("--- Top 10 Mejores Estudiantes ---\n")
            top_10 = self.ranking_estudiantes(10)
            for i, est in enumerate(top_10, 1):
                f.write(f"\n{i}. {est.nombre_completo}\n")
                f.write(f"   Carrera: {est.carrera} (Semestre {est.semestre})\n")
                f.write(f"   Promedio ponderado: {est.promedio_ponderado():.2f}\n")
                f.write(f"   Créditos cursados: {est.total_creditos()}\n")
                f.write(f"   Materias: {len(est.notas)}\n")
            
            # Estudiantes en riesgo
            en_riesgo = self.estudiantes_en_riesgo()
            f.write("\n\n--- Estudiantes en Riesgo Académico ---\n")
            f.write(f"Total: {len(en_riesgo)} estudiantes\n\n")
            
            if en_riesgo:
                for est in sorted(en_riesgo, key=lambda e: e.promedio_ponderado()):
                    f.write(f"⚠️  {est.nombre_completo} ({est.id})\n")
                    f.write(f"   Carrera: {est.carrera}\n")
                    f.write(f"   Promedio: {est.promedio_ponderado():.2f}\n")
                    f.write(f"   Materias cursadas:\n")
                    for nota in est.notas:
                        f.write(f"      - {nota.materia}: {nota.nota}\n")
                    f.write("\n")
            else:
                f.write("✅ No hay estudiantes en riesgo\n")
        
        print(f"📄 Reporte completo generado: {archivo}")
    
    def generar_resumen_json(self, archivo_salida):
        """Genera resumen ejecutivo en JSON"""
        archivo = Path(archivo_salida)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        nota_minima = self.config.get('limites', {}).get('nota_minima_aprobacion', 6.0)
        
        # Calcular métricas
        estudiantes_con_notas = [e for e in self.estudiantes.values() if e.notas]
        promedios = [e.promedio_ponderado() for e in estudiantes_con_notas]
        
        resumen = {
            'fecha_generacion': '2024-01-28',
            'metricas_generales': {
                'total_estudiantes': len(self.estudiantes),
                'estudiantes_con_notas': len(estudiantes_con_notas),
                'promedio_general': round(sum(promedios) / len(promedios), 2) if promedios else 0,
                'nota_minima_aprobacion': nota_minima
            },
            'distribucion': {
                'estudiantes_en_riesgo': len(self.estudiantes_en_riesgo()),
                'estudiantes_aprobados': len([e for e in estudiantes_con_notas 
                                             if not e.esta_en_riesgo(nota_minima)])
            },
            'top_10': [est.to_dict() for est in self.ranking_estudiantes(10)],
            'en_riesgo': [est.to_dict() for est in self.estudiantes_en_riesgo()]
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(resumen, f, indent=4, ensure_ascii=False)
        
        print(f"📊 Resumen JSON generado: {archivo}")
    
    def generar_alertas(self, archivo_salida):
        """Genera archivo de alertas para estudiantes en riesgo"""
        archivo = Path(archivo_salida)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        en_riesgo = self.estudiantes_en_riesgo()
        nota_minima = self.config.get('limites', {}).get('nota_minima_aprobacion', 6.0)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("         ALERTAS ACADÉMICAS - ESTUDIANTES EN RIESGO\n")
            f.write("=" * 60 + "\n\n")
            
            if en_riesgo:
                f.write(f"⚠️  {len(en_riesgo)} estudiantes requieren atención\n")
                f.write(f"Criterio: Promedio < {nota_minima}\n\n")
                
                for est in sorted(en_riesgo, key=lambda e: e.promedio_ponderado()):
                    f.write(f"🔴 {est.nombre_completo}\n")
                    f.write(f"   ID: {est.id}\n")
                    f.write(f"   Carrera: {est.carrera} - Semestre {est.semestre}\n")
                    f.write(f"   Promedio: {est.promedio_ponderado():.2f}\n")
                    f.write(f"   Acción recomendada: Asesoría académica\n\n")
            else:
                f.write("✅ No hay estudiantes en riesgo académico\n")
        
        print(f"🚨 Alertas generadas: {archivo}")


def main():
    """Función principal"""
    print("📊 GENERADOR DE REPORTES MULTI-FUENTE\n")
    
    # Crear generador
    generador = GeneradorReportes()
    
    # Cargar datos de múltiples fuentes
    print("⚙️  Cargando datos...")
    generador.cargar_estudiantes('data/estudiantes.csv')
    generador.cargar_notas('data/estudiantes_notas.csv')
    generador.cargar_configuracion('data/config.json')
    
    # Generar reportes
    print("\n📝 Generando reportes...")
    generador.generar_reporte_completo('output/reporte_completo.txt')
    generador.generar_resumen_json('output/resumen.json')
    generador.generar_alertas('output/alertas.txt')
    
    print(f"\n✨ Todos los reportes generados exitosamente!\n")


if __name__ == '__main__':
    main()
