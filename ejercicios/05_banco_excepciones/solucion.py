#!/usr/bin/env python3
"""
Ejercicio 5: Sistema Bancario con Excepciones Personalizadas
Procesamiento de transacciones con validación y manejo de errores robusto
"""

import csv
from pathlib import Path
from datetime import datetime


# ========== Excepciones Personalizadas ==========

class ErrorBancario(Exception):
    """Excepción base para todos los errores bancarios"""
    pass


class ErrorSaldoInsuficiente(ErrorBancario):
    """Se lanza cuando no hay saldo suficiente para un retiro"""
    pass


class ErrorMontoInvalido(ErrorBancario):
    """Se lanza cuando el monto es negativo o cero"""
    pass


class ErrorCuentaNoExiste(ErrorBancario):
    """Se lanza cuando se intenta operar con una cuenta inexistente"""
    pass


class ErrorTipoTransaccionInvalida(ErrorBancario):
    """Se lanza cuando el tipo de transacción no es válido"""
    pass


# ========== Clases del Dominio ==========

class CuentaBancaria:
    """Representa una cuenta bancaria con operaciones validadas"""
    
    def __init__(self, numero_cuenta, saldo_inicial=0):
        self.numero_cuenta = numero_cuenta
        self._saldo = float(saldo_inicial)
    
    @property
    def saldo(self):
        """Obtiene el saldo actual (solo lectura desde fuera)"""
        return self._saldo
    
    def depositar(self, monto):
        """Deposita dinero en la cuenta"""
        if monto <= 0:
            raise ErrorMontoInvalido(
                f"El monto del depósito debe ser positivo: {monto}"
            )
        self._saldo += monto
    
    def retirar(self, monto):
        """Retira dinero de la cuenta"""
        if monto <= 0:
            raise ErrorMontoInvalido(
                f"El monto del retiro debe ser positivo: {monto}"
            )
        if monto > self._saldo:
            raise ErrorSaldoInsuficiente(
                f"Saldo insuficiente. Saldo: ${self._saldo:.2f}, Intento: ${monto:.2f}"
            )
        self._saldo -= monto
    
    def __str__(self):
        return f"{self.numero_cuenta}: ${self._saldo:.2f}"


class Transaccion:
    """Representa una transacción bancaria"""
    
    def __init__(self, id_transaccion, fecha, tipo, monto, cuenta, descripcion):
        self.id_transaccion = id_transaccion
        self.fecha = fecha
        self.tipo = tipo.lower()
        self.monto = float(monto)
        self.cuenta = cuenta
        self.descripcion = descripcion
    
    @classmethod
    def from_csv_row(cls, fila):
        """Crea una transacción desde una fila CSV"""
        return cls(
            id_transaccion=fila['id_transaccion'],
            fecha=fila['fecha'],
            tipo=fila['tipo'],
            monto=fila['monto'],
            cuenta=fila['cuenta'],
            descripcion=fila['descripcion']
        )
    
    def __str__(self):
        return f"{self.id_transaccion}: {self.tipo} ${self.monto:.2f} - {self.cuenta}"


class GestorBancario:
    """Gestor principal del sistema bancario"""
    
    def __init__(self):
        self.cuentas = {}  # {numero_cuenta: CuentaBancaria}
        self.transacciones_exitosas = []
        self.transacciones_fallidas = []
    
    def obtener_o_crear_cuenta(self, numero_cuenta):
        """Obtiene una cuenta existente o crea una nueva"""
        if numero_cuenta not in self.cuentas:
            self.cuentas[numero_cuenta] = CuentaBancaria(numero_cuenta)
        return self.cuentas[numero_cuenta]
    
    def obtener_cuenta(self, numero_cuenta):
        """Obtiene una cuenta existente (lanza excepción si no existe)"""
        if numero_cuenta not in self.cuentas:
            raise ErrorCuentaNoExiste(f"La cuenta {numero_cuenta} no existe")
        return self.cuentas[numero_cuenta]
    
    def procesar_transaccion(self, transaccion):
        """
        Procesa una transacción individual
        Retorna: (exito: bool, error_mensaje: str o None)
        """
        try:
            # Obtener o crear cuenta
            cuenta = self.obtener_o_crear_cuenta(transaccion.cuenta)
            
            # Procesar según tipo
            if transaccion.tipo == 'deposito':
                cuenta.depositar(transaccion.monto)
            elif transaccion.tipo == 'retiro':
                cuenta.retirar(transaccion.monto)
            else:
                raise ErrorTipoTransaccionInvalida(
                    f"Tipo de transacción inválido: {transaccion.tipo}"
                )
            
            # Registrar éxito
            self.transacciones_exitosas.append(transaccion)
            return True, None
            
        except ErrorBancario as e:
            # Registrar fallo
            self.transacciones_fallidas.append((transaccion, str(e)))
            return False, str(e)
    
    def cargar_transacciones(self, archivo_csv):
        """Carga y procesa transacciones desde CSV"""
        archivo = Path(archivo_csv)
        transacciones_cargadas = 0
        
        try:
            with open(archivo, 'r', encoding='utf-8', newline='') as f:
                lector = csv.DictReader(f)
                for fila in lector:
                    try:
                        transaccion = Transaccion.from_csv_row(fila)
                        self.procesar_transaccion(transaccion)
                        transacciones_cargadas += 1
                    except ValueError as e:
                        print(f"⚠️  Error al parsear fila: {e}")
            
            print(f"✅ Transacciones procesadas: {transacciones_cargadas}")
            print(f"   Exitosas: {len(self.transacciones_exitosas)}")
            print(f"   Fallidas: {len(self.transacciones_fallidas)}")
            
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {archivo}")
            raise
    
    def generar_log_errores(self, archivo_log):
        """Genera un archivo de log con los errores de transacciones"""
        archivo = Path(archivo_log)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("    LOG DE ERRORES - SISTEMA BANCARIO\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total de errores: {len(self.transacciones_fallidas)}\n\n")
            
            if self.transacciones_fallidas:
                for transaccion, error in self.transacciones_fallidas:
                    f.write(f"--- {transaccion.id_transaccion} ---\n")
                    f.write(f"Fecha: {transaccion.fecha}\n")
                    f.write(f"Tipo: {transaccion.tipo}\n")
                    f.write(f"Monto: ${transaccion.monto:.2f}\n")
                    f.write(f"Cuenta: {transaccion.cuenta}\n")
                    f.write(f"ERROR: {error}\n\n")
            else:
                f.write("✅ No se registraron errores\n")
        
        print(f"📝 Log de errores generado: {archivo}")
    
    def generar_reporte(self, archivo_salida):
        """Genera un reporte completo del estado bancario"""
        archivo = Path(archivo_salida)
        archivo.parent.mkdir(parents=True, exist_ok=True)
        
        with open(archivo, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("=" * 50 + "\n")
            f.write("          REPORTE BANCARIO\n")
            f.write("=" * 50 + "\n\n")
            
            total_trans = len(self.transacciones_exitosas) + len(self.transacciones_fallidas)
            f.write(f"Transacciones procesadas: {total_trans}\n")
            f.write(f"Exitosas: {len(self.transacciones_exitosas)}\n")
            f.write(f"Fallidas: {len(self.transacciones_fallidas)}\n\n")
            
            # Saldos finales
            f.write("--- Saldos Finales de Cuentas ---\n")
            for numero in sorted(self.cuentas.keys()):
                cuenta = self.cuentas[numero]
                f.write(f"{cuenta.numero_cuenta}: ${cuenta.saldo:,.2f}\n")
            f.write("\n")
            
            # Total en el sistema
            total_sistema = sum(c.saldo for c in self.cuentas.values())
            f.write(f"💰 Total en el sistema: ${total_sistema:,.2f}\n\n")
            
            # Transacciones fallidas
            if self.transacciones_fallidas:
                f.write("--- Transacciones Fallidas ---\n")
                for transaccion, error in self.transacciones_fallidas:
                    f.write(f"❌ {transaccion.id_transaccion} ({transaccion.cuenta}): ")
                    f.write(f"{transaccion.tipo} ${transaccion.monto:.2f}\n")
                    f.write(f"   Error: {error}\n\n")
            else:
                f.write("✅ Todas las transacciones fueron exitosas\n")
        
        print(f"📊 Reporte generado: {archivo}")


def main():
    """Función principal"""
    # Crear gestor
    gestor = GestorBancario()
    
    # Cargar y procesar transacciones
    print("💳 Procesando transacciones bancarias...\n")
    gestor.cargar_transacciones('data/transacciones.csv')
    
    # Mostrar resumen en consola
    print(f"\n💰 Resumen:")
    for numero, cuenta in sorted(gestor.cuentas.items()):
        print(f"   {cuenta}")
    
    total = sum(c.saldo for c in gestor.cuentas.values())
    print(f"\n💵 Total en el sistema: ${total:,.2f}")
    
    # Generar reportes
    gestor.generar_log_errores('output/errores_transacciones.log')
    gestor.generar_reporte('output/reporte_bancario.txt')
    
    print(f"\n✨ Proceso completado!\n")


if __name__ == '__main__':
    main()
