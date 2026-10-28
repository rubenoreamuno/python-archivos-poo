#!/usr/bin/env python3
"""
Ejercicio 6: Conversor CSV ↔ JSON
Conversión bidireccional entre formatos con inferencia de tipos
"""

import csv
import json
from pathlib import Path


class ConversorArchivos:
    """Utilidad para convertir entre formatos CSV y JSON"""
    
    @staticmethod
    def inferir_tipo(valor):
        """
        Intenta inferir y convertir el tipo de un valor string
        Intenta: int -> float -> bool -> string
        """
        if not isinstance(valor, str):
            return valor
        
        valor = valor.strip()
        
        # Intentar int
        try:
            return int(valor)
        except ValueError:
            pass
        
        # Intentar float
        try:
            return float(valor)
        except ValueError:
            pass
        
        # Booleanos
        if valor.lower() in ('true', 'verdadero', 'sí', 'si'):
            return True
        if valor.lower() in ('false', 'falso', 'no'):
            return False
        
        # Devolver como string
        return valor
    
    @staticmethod
    def csv_a_json(archivo_csv, archivo_json, inferir_tipos=True, indent=4):
        """
        Convierte un archivo CSV a JSON
        
        Args:
            archivo_csv: Ruta del archivo CSV de entrada
            archivo_json: Ruta del archivo JSON de salida
            inferir_tipos: Si True, intenta convertir strings a tipos apropiados
            indent: Espacios de indentación en el JSON
        """
        archivo_csv = Path(archivo_csv)
        archivo_json = Path(archivo_json)
        archivo_json.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(archivo_csv, 'r', encoding='utf-8', newline='') as f:
                lector = csv.DictReader(f)
                datos = []
                
                for fila in lector:
                    if inferir_tipos:
                        # Convertir cada valor a su tipo apropiado
                        fila_convertida = {
                            clave: ConversorArchivos.inferir_tipo(valor)
                            for clave, valor in fila.items()
                        }
                        datos.append(fila_convertida)
                    else:
                        datos.append(fila)
            
            # Escribir JSON
            with open(archivo_json, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=indent, ensure_ascii=False)
            
            print(f"✅ CSV → JSON: {archivo_csv} → {archivo_json}")
            print(f"   {len(datos)} registros convertidos")
            
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {archivo_csv}")
            raise
        except Exception as e:
            print(f"❌ Error en conversión CSV→JSON: {e}")
            raise
    
    @staticmethod
    def json_a_csv(archivo_json, archivo_csv, campos=None):
        """
        Convierte un archivo JSON a CSV
        
        Args:
            archivo_json: Ruta del archivo JSON de entrada (debe ser lista de objetos)
            archivo_csv: Ruta del archivo CSV de salida
            campos: Lista de campos a incluir (None = todos)
        """
        archivo_json = Path(archivo_json)
        archivo_csv = Path(archivo_csv)
        archivo_csv.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Leer JSON
            with open(archivo_json, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            if not isinstance(datos, list):
                raise ValueError("El JSON debe ser una lista de objetos")
            
            if not datos:
                print("⚠️  JSON vacío, no se generó CSV")
                return
            
            # Determinar campos
            if campos is None:
                # Usar todas las claves del primer objeto
                campos = list(datos[0].keys())
            
            # Escribir CSV
            with open(archivo_csv, 'w', encoding='utf-8', newline='') as f:
                escritor = csv.DictWriter(f, fieldnames=campos)
                escritor.writeheader()
                
                for objeto in datos:
                    # Filtrar solo los campos especificados
                    fila = {campo: objeto.get(campo, '') for campo in campos}
                    escritor.writerow(fila)
            
            print(f"✅ JSON → CSV: {archivo_json} → {archivo_csv}")
            print(f"   {len(datos)} registros convertidos")
            
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {archivo_json}")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ Error al leer JSON: {e}")
            raise
        except Exception as e:
            print(f"❌ Error en conversión JSON→CSV: {e}")
            raise
    
    @staticmethod
    def convertir_lote_csv_a_json(directorio_csv, directorio_json):
        """Convierte todos los archivos CSV de un directorio a JSON"""
        directorio_csv = Path(directorio_csv)
        directorio_json = Path(directorio_json)
        directorio_json.mkdir(parents=True, exist_ok=True)
        
        archivos_csv = list(directorio_csv.glob('*.csv'))
        print(f"\n📁 Conversión en lote: {len(archivos_csv)} archivos CSV encontrados")
        
        for archivo_csv in archivos_csv:
            archivo_json = directorio_json / f"{archivo_csv.stem}.json"
            try:
                ConversorArchivos.csv_a_json(archivo_csv, archivo_json)
            except Exception as e:
                print(f"   ⚠️  Error al convertir {archivo_csv.name}: {e}")


def main():
    """Función principal - demostración de conversiones"""
    print("🔄 CONVERSOR DE ARCHIVOS CSV ↔ JSON\n")
    
    # === Conversión 1: Estudiantes CSV → JSON ===
    print("=" * 50)
    print("Conversión 1: Estudiantes CSV → JSON")
    print("=" * 50)
    ConversorArchivos.csv_a_json(
        'data/estudiantes.csv',
        'output/estudiantes.json',
        inferir_tipos=True
    )
    
    # === Conversión 2: Notas CSV → JSON ===
    print("\n" + "=" * 50)
    print("Conversión 2: Notas CSV → JSON (con inferencia de tipos)")
    print("=" * 50)
    ConversorArchivos.csv_a_json(
        'data/estudiantes_notas.csv',
        'output/estudiantes_notas.json',
        inferir_tipos=True
    )
    
    # === Conversión 3: JSON → CSV ===
    print("\n" + "=" * 50)
    print("Conversión 3: Empleados JSON → CSV")
    print("=" * 50)
    
    # Primero necesitamos aplanar el JSON anidado de empleados
    # Extraer empleados de todos los departamentos
    with open('data/empleados.json', 'r', encoding='utf-8') as f:
        datos_empresa = json.load(f)
    
    empleados_planos = []
    for depto in datos_empresa['departamentos']:
        for emp in depto['empleados']:
            empleado_plano = {
                'id': emp['id'],
                'nombre': emp['nombre'],
                'cargo': emp['cargo'],
                'salario': emp['salario'],
                'fecha_ingreso': emp['fecha_ingreso'],
                'departamento': depto['nombre']
            }
            empleados_planos.append(empleado_plano)
    
    # Guardar JSON aplanado temporal
    json_temp = Path('output/empleados_plano.json')
    json_temp.parent.mkdir(parents=True, exist_ok=True)
    with open(json_temp, 'w', encoding='utf-8') as f:
        json.dump(empleados_planos, f, indent=4, ensure_ascii=False)
    
    # Convertir a CSV
    ConversorArchivos.json_a_csv(
        'output/empleados_plano.json',
        'output/empleados.csv'
    )
    
    # === Conversión 4: Round-trip (CSV → JSON → CSV) ===
    print("\n" + "=" * 50)
    print("Conversión 4: Round-trip - Inventario")
    print("CSV → JSON → CSV (verificar integridad)")
    print("=" * 50)
    
    # CSV → JSON
    ConversorArchivos.csv_a_json(
        'data/inventario.csv',
        'output/inventario_convertido.json',
        inferir_tipos=True
    )
    
    # JSON → CSV
    ConversorArchivos.json_a_csv(
        'output/inventario_convertido.json',
        'output/inventario_round_trip.csv'
    )
    
    print("\n" + "=" * 50)
    print("✨ Todas las conversiones completadas!")
    print("=" * 50)
    print("\n📂 Archivos generados en: output/")
    print("   - estudiantes.json")
    print("   - estudiantes_notas.json")
    print("   - empleados.csv")
    print("   - inventario_convertido.json")
    print("   - inventario_round_trip.csv")
    print()


if __name__ == '__main__':
    main()
