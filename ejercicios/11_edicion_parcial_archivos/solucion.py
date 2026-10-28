#!/usr/bin/env python3
"""
Ejercicio 11: Edición Parcial de Archivos (In-Place)
Técnicas avanzadas de edición sin reescribir archivos completos

⚠️ ADVERTENCIA: Estas técnicas son avanzadas y riesgosas.
   Para la mayoría de casos, PREFERIR leer→modificar→escribir completo.
"""

import shutil
from pathlib import Path
from datetime import datetime


class EditorParcialArchivos:
    """
    Demostración de técnicas de edición parcial de archivos.
    
    ⚠️ IMPORTANTE: Estas técnicas deben usarse con extremo cuidado.
    """
    
    @staticmethod
    def crear_respaldo(archivo):
        """Crea un respaldo del archivo antes de editarlo"""
        archivo = Path(archivo)
        if not archivo.exists():
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        respaldo = archivo.parent / f"{archivo.stem}_backup_{timestamp}{archivo.suffix}"
        shutil.copy2(archivo, respaldo)
        print(f"📋 Respaldo creado: {respaldo}")
        return respaldo
    
    @staticmethod
    def ejemplo_1_seek_tell():
        """
        Ejemplo 1: Demostración básica de seek() y tell()
        """
        print("\n" + "=" * 60)
        print("EJEMPLO 1: seek() y tell() - Posicionamiento en archivos")
        print("=" * 60)
        
        # Crear archivo de ejemplo
        archivo = Path('output/ejemplo_seek.txt')
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        # Escribir contenido inicial
        contenido = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        archivo.write_text(contenido, encoding='utf-8')
        print(f"\n📄 Archivo creado: {contenido}")
        
        # Demostrar seek y tell
        with open(archivo, 'r', encoding='utf-8') as f:
            print(f"\n🔍 Posición inicial: {f.tell()}")  # 0
            
            # Leer 10 caracteres
            datos = f.read(10)
            print(f"   Leído: '{datos}'")
            print(f"   Posición actual: {f.tell()}")  # 10
            
            # Ir al byte 20
            f.seek(20)
            print(f"\n↪️  Después de seek(20): {f.tell()}")
            datos = f.read(5)
            print(f"   Leído: '{datos}'")
            
            # Ir al inicio de nuevo
            f.seek(0)
            print(f"\n↩️  De vuelta al inicio: {f.tell()}")
            
            # Saltar 5 bytes desde posición actual
            f.read(5)  # Avanzar 5
            print(f"   Después de leer 5: {f.tell()}")
            datos = f.read(10)
            print(f"   Leído: '{datos}'")
    
    @staticmethod
    def ejemplo_2_modo_r_plus():
        """
        Ejemplo 2: Modo r+ (lectura y escritura)
        """
        print("\n" + "=" * 60)
        print("EJEMPLO 2: Modo r+ - Lectura y Escritura Simultánea")
        print("=" * 60)
        
        archivo = Path('output/ejemplo_r_plus.txt')
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        # Contenido inicial
        lineas_iniciales = [
            "Línea 1: Estado original\n",
            "Línea 2: Estado original\n",
            "Línea 3: Estado original\n",
        ]
        archivo.write_text(''.join(lineas_iniciales), encoding='utf-8')
        
        print("\n📄 Contenido inicial:")
        print(archivo.read_text(encoding='utf-8'))
        
        # Editar con r+
        with open(archivo, 'r+', encoding='utf-8') as f:
            # Leer todo
            contenido = f.read()
            print("✏️  Modificando 'original' → 'MODIFICADO'")
            
            # Modificar
            contenido_nuevo = contenido.replace('original', 'MODIFICADO')
            
            # Volver al inicio y escribir
            f.seek(0)
            f.write(contenido_nuevo)
            f.truncate()  # Importante: cortar si el nuevo es más corto
        
        print("\n📄 Contenido después de r+:")
        print(archivo.read_text(encoding='utf-8'))
    
    @staticmethod
    def ejemplo_3_actualizar_linea_especifica():
        """
        Ejemplo 3: Actualizar una línea específica
        
        ⚠️ LIMITACIÓN: Solo funciona si la nueva línea tiene el MISMO tamaño
        """
        print("\n" + "=" * 60)
        print("EJEMPLO 3: Actualizar Línea Específica (mismo tamaño)")
        print("=" * 60)
        
        archivo = Path('output/ejemplo_linea_especifica.txt')
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        # Crear archivo con líneas de tamaño fijo
        lineas = [
            "ID:001|Producto A |100.00|050\n",  # 30 chars
            "ID:002|Producto B |200.00|030\n",
            "ID:003|Producto C |150.00|020\n",
            "ID:004|Producto D |300.00|010\n",
        ]
        archivo.write_text(''.join(lineas), encoding='utf-8')
        
        print("\n📄 Archivo inicial (formato fijo):")
        print(archivo.read_text(encoding='utf-8'))
        
        # Actualizar línea 2 (índice 1)
        linea_a_actualizar = 1
        nueva_linea = "ID:002|Producto B |250.00|028\n"  # MISMO tamaño
        
        print(f"✏️  Actualizando línea {linea_a_actualizar + 1}:")
        print(f"   Nueva: {nueva_linea.strip()}")
        
        # Método 1: Leer todo, modificar, escribir (RECOMENDADO)
        with open(archivo, 'r+', encoding='utf-8') as f:
            lineas = f.readlines()
            
            # Verificar que el tamaño sea igual
            if len(nueva_linea) != len(lineas[linea_a_actualizar]):
                print("   ⚠️  ERROR: La nueva línea no tiene el mismo tamaño!")
                return
            
            lineas[linea_a_actualizar] = nueva_linea
            
            # Reescribir todo (más seguro)
            f.seek(0)
            f.writelines(lineas)
            f.truncate()
        
        print("\n📄 Archivo después de actualizar:")
        print(archivo.read_text(encoding='utf-8'))
    
    @staticmethod
    def ejemplo_4_edicion_parcial_real():
        """
        Ejemplo 4: Edición parcial verdadera (solo el fragmento modificado)
        
        ⚠️ PELIGROSO: Solo para demostración educativa
        """
        print("\n" + "=" * 60)
        print("EJEMPLO 4: Edición Parcial Real (AVANZADO)")
        print("=" * 60)
        
        archivo = Path('output/ejemplo_parcial_real.txt')
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        # Crear archivo con formato fijo conocido
        # Cada registro: 39 bytes exactos (incluyendo \n)
        registros = [
            "REG001|STATUS:ACTIVE  |DATA:0000000001\n",  # 39 bytes
            "REG002|STATUS:ACTIVE  |DATA:0000000002\n",
            "REG003|STATUS:PENDING |DATA:0000000003\n",
            "REG004|STATUS:ACTIVE  |DATA:0000000004\n",
        ]
        archivo.write_text(''.join(registros), encoding='utf-8')
        
        print("\n📄 Archivo inicial:")
        print(archivo.read_text(encoding='utf-8'))
        
        # Cambiar STATUS del registro 2 (índice 1) de ACTIVE a CLOSED
        # Formato: "REG002|STATUS:ACTIVE  |DATA:0000000002\n"
        #          0123456789012345678901234567890123456789
        #                ^7=S  ^14=A (ACTIVE empieza en 14)
        registro_a_modificar = 1
        tamanio_registro = 39  # 39 bytes por línea
        offset_status = 14  # Posición de "ACTIVE" en cada línea
        nuevo_status = "CLOSED"  # MISMO tamaño que "ACTIVE"
        
        print(f"\n✏️  Cambiando STATUS del registro {registro_a_modificar + 1}:")
        print(f"   De: 'ACTIVE ' → A: 'CLOSED '")
        
        # Crear respaldo primero
        EditorParcialArchivos.crear_respaldo(archivo)
        
        try:
            with open(archivo, 'r+', encoding='utf-8') as f:
                # Calcular posición exacta
                posicion = (registro_a_modificar * tamanio_registro) + offset_status
                
                print(f"   📍 Posición calculada: byte {posicion}")
                
                # Ir a la posición
                f.seek(posicion)
                
                # Leer el valor actual (verificación)
                valor_actual = f.read(len(nuevo_status))
                print(f"   📖 Valor actual: '{valor_actual}'")
                
                # Volver a la posición y escribir
                f.seek(posicion)
                f.write(nuevo_status)
                
                print(f"   ✅ Escritura parcial completada")
        
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            print("   💡 Restaurar desde respaldo si es necesario")
            return
        
        print("\n📄 Archivo después de edición parcial:")
        print(archivo.read_text(encoding='utf-8'))
        
        print("\n💡 NOTA: Esta técnica:")
        print("   ✅ Solo modificó 7 bytes en lugar de reescribir 160")
        print("   ⚠️  Requiere conocimiento exacto de posiciones")
        print("   ⚠️  Es riesgosa si se interrumpe")
    
    @staticmethod
    def ejemplo_5_cuando_no_usar():
        """
        Ejemplo 5: Cuándo NO usar edición parcial
        """
        print("\n" + "=" * 60)
        print("EJEMPLO 5: Cuándo NO Usar Edición Parcial")
        print("=" * 60)
        
        print("\n❌ CASO 1: Cambio de tamaño variable")
        print("   Problema: Insertar o eliminar contenido desplaza todo")
        print("   Solución: Leer → modificar → escribir completo")
        
        print("\n❌ CASO 2: Archivos estructurados (CSV, JSON)")
        print("   Problema: Cambiar un valor puede alterar delimitadores")
        print("   Solución: Usar bibliotecas (csv, json) que reescriben")
        
        print("\n❌ CASO 3: Sin respaldo ni rollback")
        print("   Problema: Error a mitad deja archivo corrupto")
        print("   Solución: Siempre crear respaldo o usar temp + rename")
        
        print("\n❌ CASO 4: Archivos pequeños (< 1 MB)")
        print("   Problema: La optimización no vale la complejidad")
        print("   Solución: Reescribir completo es más simple y seguro")
        
        print("\n✅ CASO VÁLIDO: Archivo de 10 GB, cambiar 1 byte")
        print("   Ejemplo: Base de datos custom, flags de configuración")
        print("   Condición: Posición exacta conocida, mismo tamaño")


def main():
    """Función principal - demostración de todas las técnicas"""
    print("📝 EDICIÓN PARCIAL DE ARCHIVOS (IN-PLACE)")
    print("⚠️  TÉCNICAS AVANZADAS - Usar con precaución")
    
    editor = EditorParcialArchivos()
    
    # Ejecutar ejemplos
    editor.ejemplo_1_seek_tell()
    editor.ejemplo_2_modo_r_plus()
    editor.ejemplo_3_actualizar_linea_especifica()
    editor.ejemplo_4_edicion_parcial_real()
    editor.ejemplo_5_cuando_no_usar()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📚 RESUMEN Y RECOMENDACIONES")
    print("=" * 60)
    print("\n✅ PARA ESTUDIANTES:")
    print("   1. Aprender PRIMERO: leer → modificar → escribir (ejercicios 1-10)")
    print("   2. Entender edición parcial como optimización avanzada")
    print("   3. En la práctica: preferir siempre reescritura completa")
    print("   4. Solo usar edición parcial con:")
    print("      • Archivos muy grandes (GB+)")
    print("      • Formato fijo conocido")
    print("      • Sistema de respaldo")
    print("      • Mismo tamaño exacto")
    
    print("\n✅ PATRÓN RECOMENDADO (99% de los casos):")
    print("""
    # Seguro, simple, atómico
    datos = leer_archivo()
    datos_modificados = procesar(datos)
    escribir_archivo(datos_modificados)
    """)
    
    print("\n⚠️  EDICIÓN PARCIAL: Solo cuando sea absolutamente necesario")
    print("   y entiendas completamente los riesgos.\n")


if __name__ == '__main__':
    main()
