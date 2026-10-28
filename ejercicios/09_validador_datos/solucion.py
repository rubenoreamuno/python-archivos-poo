#!/usr/bin/env python3
"""
Ejercicio 9: Validador de Datos CSV con Reporte de Errores
Sistema de validación y limpieza de datos con reporte detallado
"""

import csv
from pathlib import Path


class ErrorValidacion(Exception):
    """Excepción para errores de validación de datos"""
    pass


class ValidadorProducto:
    """Validadores estáticos para campos de producto"""
    
    @staticmethod
    def validar_codigo(codigo):
        """Valida que el código no esté vacío y tenga formato correcto"""
        if not codigo or codigo.strip() == '':
            raise ErrorValidacion("Código vacío")
        
        if len(codigo) < 3:
            raise ErrorValidacion(f"Código muy corto: '{codigo}'")
        
        return codigo.strip()
    
    @staticmethod
    def validar_nombre(nombre):
        """Valida que el nombre no esté vacío"""
        if not nombre or nombre.strip() == '':
            raise ErrorValidacion("Nombre vacío")
        
        if len(nombre.strip()) < 2:
            raise ErrorValidacion(f"Nombre muy corto: '{nombre}'")
        
        return nombre.strip()
    
    @staticmethod
    def validar_precio(precio_str):
        """Valida que el precio sea un número positivo"""
        try:
            precio = float(precio_str)
        except ValueError:
            raise ErrorValidacion(f"Precio inválido (no es número): '{precio_str}'")
        
        if precio < 0:
            raise ErrorValidacion(f"Precio negativo: {precio}")
        
        if precio == 0:
            raise ErrorValidacion("Precio es cero")
        
        return precio
    
    @staticmethod
    def validar_stock(stock_str):
        """Valida que el stock sea un entero no negativo"""
        try:
            stock = int(stock_str)
        except ValueError:
            raise ErrorValidacion(f"Stock inválido (no es entero): '{stock_str}'")
        
        if stock < 0:
            raise ErrorValidacion(f"Stock negativo: {stock}")
        
        return stock


class ValidadorCSV:
    """Sistema de validación de archivos CSV"""
    
    def __init__(self, archivo_entrada):
        self.archivo_entrada = Path(archivo_entrada)
        self.filas_validas = []
        self.filas_invalidas = []
        self.columnas = []
    
    def validar_fila(self, fila, num_fila):
        """
        Valida una fila completa
        Retorna: (es_valida, fila_limpia, lista_errores)
        """
        errores = []
        fila_limpia = {}
        
        # Validar código
        try:
            fila_limpia['codigo'] = ValidadorProducto.validar_codigo(fila.get('codigo', ''))
        except ErrorValidacion as e:
            errores.append(('codigo', str(e)))
        
        # Validar nombre
        try:
            fila_limpia['nombre'] = ValidadorProducto.validar_nombre(fila.get('nombre', ''))
        except ErrorValidacion as e:
            errores.append(('nombre', str(e)))
        
        # Validar precio
        try:
            fila_limpia['precio'] = ValidadorProducto.validar_precio(fila.get('precio', ''))
        except ErrorValidacion as e:
            errores.append(('precio', str(e)))
        
        # Validar stock
        try:
            fila_limpia['stock'] = ValidadorProducto.validar_stock(fila.get('stock', ''))
        except ErrorValidacion as e:
            errores.append(('stock', str(e)))
        
        es_valida = len(errores) == 0
        
        return es_valida, fila_limpia if es_valida else fila, errores
    
    def procesar_archivo(self):
        """Procesa el archivo CSV completo y valida cada fila"""
        try:
            with open(self.archivo_entrada, 'r', encoding='utf-8', newline='') as f:
                lector = csv.DictReader(f)
                self.columnas = lector.fieldnames
                
                for num_fila, fila in enumerate(lector, start=2):  # Start at 2 (header = 1)
                    es_valida, fila_procesada, errores = self.validar_fila(fila, num_fila)
                    
                    if es_valida:
                        self.filas_validas.append(fila_procesada)
                    else:
                        self.filas_invalidas.append({
                            'num_fila': num_fila,
                            'fila': fila,
                            'errores': errores
                        })
            
            print(f"✅ Archivo procesado: {self.archivo_entrada}")
            print(f"   Filas válidas: {len(self.filas_validas)}")
            print(f"   Filas inválidas: {len(self.filas_invalidas)}")
            
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {self.archivo_entrada}")
            raise
    
    def generar_csv_limpio(self, archivo_salida):
        """Genera CSV solo con filas válidas"""
        archivo = Path(archivo_salida)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.filas_validas:
            print("⚠️  No hay datos válidos para guardar")
            return
        
        with open(archivo, 'w', encoding='utf-8', newline='') as f:
            escritor = csv.DictWriter(f, fieldnames=self.columnas)
            escritor.writeheader()
            
            for fila in self.filas_validas:
                escritor.writerow(fila)
        
        print(f"💾 CSV limpio generado: {archivo} ({len(self.filas_validas)} filas)")
    
    def generar_reporte_errores(self, archivo_salida):
        """Genera reporte detallado de errores encontrados"""
        archivo = Path(archivo_salida)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        total_filas = len(self.filas_validas) + len(self.filas_invalidas)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("=" * 70 + "\n")
            f.write("           REPORTE DE VALIDACIÓN DE DATOS\n")
            f.write("=" * 70 + "\n\n")
            
            # Resumen
            f.write("--- Resumen ---\n")
            f.write(f"Archivo procesado: {self.archivo_entrada.name}\n")
            f.write(f"Total de filas procesadas: {total_filas}\n")
            f.write(f"Filas válidas: {len(self.filas_validas)} " +
                   f"({len(self.filas_validas)/total_filas*100:.1f}%)\n")
            f.write(f"Filas inválidas: {len(self.filas_invalidas)} " +
                   f"({len(self.filas_invalidas)/total_filas*100:.1f}%)\n\n")
            
            # Detalle de errores
            if self.filas_invalidas:
                f.write("--- Errores Encontrados (Detalle) ---\n\n")
                
                for info in self.filas_invalidas:
                    f.write(f"▶ Fila {info['num_fila']}:\n")
                    f.write(f"  Datos: {info['fila']}\n")
                    f.write(f"  Errores detectados:\n")
                    
                    for campo, error in info['errores']:
                        f.write(f"    ❌ Campo '{campo}': {error}\n")
                    
                    f.write("\n")
                
                # Estadísticas de errores por campo
                f.write("\n--- Estadísticas de Errores por Campo ---\n")
                errores_por_campo = {}
                for info in self.filas_invalidas:
                    for campo, _ in info['errores']:
                        errores_por_campo[campo] = errores_por_campo.get(campo, 0) + 1
                
                for campo, cantidad in sorted(errores_por_campo.items(), 
                                             key=lambda x: x[1], reverse=True):
                    f.write(f"  {campo}: {cantidad} errores\n")
            else:
                f.write("✅ No se encontraron errores. Todos los datos son válidos.\n")
        
        print(f"📋 Reporte de errores generado: {archivo}")
    
    def generar_estadisticas(self, archivo_salida):
        """Genera estadísticas de los datos válidos"""
        archivo = Path(archivo_salida)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.filas_validas:
            return
        
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("       ESTADÍSTICAS DE DATOS VÁLIDOS\n")
            f.write("=" * 60 + "\n\n")
            
            # Estadísticas de precios
            precios = [fila['precio'] for fila in self.filas_validas]
            f.write("--- Precios ---\n")
            f.write(f"Precio promedio: ${sum(precios)/len(precios):.2f}\n")
            f.write(f"Precio mínimo: ${min(precios):.2f}\n")
            f.write(f"Precio máximo: ${max(precios):.2f}\n\n")
            
            # Estadísticas de stock
            stocks = [fila['stock'] for fila in self.filas_validas]
            f.write("--- Stock ---\n")
            f.write(f"Stock promedio: {sum(stocks)/len(stocks):.1f} unidades\n")
            f.write(f"Stock total: {sum(stocks)} unidades\n")
            f.write(f"Productos sin stock: {sum(1 for s in stocks if s == 0)}\n")
        
        print(f"📊 Estadísticas generadas: {archivo}")


def main():
    """Función principal"""
    print("🔍 VALIDADOR DE DATOS CSV\n")
    
    # Crear validador
    validador = ValidadorCSV('data/productos_dirty.csv')
    
    # Procesar archivo
    print("⚙️  Procesando y validando datos...")
    validador.procesar_archivo()
    
    # Generar salidas
    print("\n📝 Generando reportes...")
    validador.generar_csv_limpio('output/productos_limpios.csv')
    validador.generar_reporte_errores('output/reporte_errores_validacion.txt')
    validador.generar_estadisticas('output/estadisticas_productos.txt')
    
    # Resumen en consola
    total = len(validador.filas_validas) + len(validador.filas_invalidas)
    print(f"\n📊 Resumen:")
    print(f"   Total procesado: {total} filas")
    print(f"   ✅ Válidas: {len(validador.filas_validas)}")
    print(f"   ❌ Inválidas: {len(validador.filas_invalidas)}")
    
    if validador.filas_invalidas:
        print(f"\n⚠️  Se encontraron {len(validador.filas_invalidas)} filas con errores")
        print(f"   Ver detalle en: output/reporte_errores_validacion.txt")
    
    print(f"\n✨ Validación completada!\n")


if __name__ == '__main__':
    main()
