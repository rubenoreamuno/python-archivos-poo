# Ejercicio 5: Sistema Bancario con Excepciones Personalizadas

## 📋 Descripción

Desarrollar un sistema bancario que procese transacciones desde CSV y use excepciones personalizadas para manejar casos de error de negocio.

## 🎯 Objetivos de Aprendizaje

- Crear excepciones personalizadas
- Implementar validaciones robustas
- Manejar transacciones con verificaciones
- Usar `@property` para encapsulación
- Registrar errores en archivo de log

## 📝 Requisitos Funcionales

1. Leer `data/transacciones.csv`
2. Crear cuentas bancarias y procesar transacciones
3. Validar cada transacción:
   - Retiros no pueden exceder saldo
   - Montos deben ser positivos
   - Cuentas deben existir
4. Registrar errores en `output/errores_transacciones.log`
5. Generar reporte final de saldos

## 🏗️ Diseño Sugerido

### Excepciones Personalizadas

```python
class ErrorBancario(Exception):
    """Excepción base para errores bancarios"""
    pass

class ErrorSaldoInsuficiente(ErrorBancario):
    """Saldo insuficiente para la operación"""
    pass

class ErrorMontoInvalido(ErrorBancario):
    """Monto negativo o cero"""
    pass

class ErrorCuentaNoExiste(ErrorBancario):
    """Cuenta no encontrada"""
    pass
```

### Clases

```python
class CuentaBancaria:
    def __init__(self, numero_cuenta, saldo_inicial=0):
        self._saldo = saldo_inicial
    
    @property
    def saldo(self):
        return self._saldo
    
    def depositar(self, monto):
        if monto <= 0:
            raise ErrorMontoInvalido(...)
        self._saldo += monto
    
    def retirar(self, monto):
        if monto <= 0:
            raise ErrorMontoInvalido(...)
        if monto > self._saldo:
            raise ErrorSaldoInsuficiente(...)
        self._saldo -= monto

class Transaccion:
    def __init__(self, id_transaccion, fecha, tipo, monto, cuenta, descripcion):
        # Atributos

class GestorBancario:
    def __init__(self):
        self.cuentas = {}  # {numero: CuentaBancaria}
        self.transacciones_exitosas = []
        self.transacciones_fallidas = []
    
    def procesar_transaccion(self, transaccion):
        try:
            cuenta = self.obtener_cuenta(transaccion.cuenta)
            if transaccion.tipo == 'deposito':
                cuenta.depositar(transaccion.monto)
            elif transaccion.tipo == 'retiro':
                cuenta.retirar(transaccion.monto)
            self.transacciones_exitosas.append(transaccion)
        except ErrorBancario as e:
            self.transacciones_fallidas.append((transaccion, str(e)))
```

## 📤 Salida Esperada

```
========================================
    REPORTE BANCARIO
========================================

Transacciones procesadas: 15
Exitosas: 13
Fallidas: 2

--- Saldos Finales ---
CTA-1001: $1,400.00
CTA-1002: $1,200.00
CTA-1003: $1,450.00

--- Transacciones Fallidas ---
TXN008: Error - Saldo insuficiente
TXN012: Error - Monto inválido
```

## 💡 Tips

- Usa `try-except` específico para cada tipo de error
- Log de errores debe incluir timestamp y detalles
- Valida datos antes de crear objetos

## ✅ Criterios de Evaluación

- [x] Excepciones personalizadas bien diseñadas
- [x] Validaciones correctas en cada operación
- [x] Log de errores detallado
- [x] Cálculos de saldo correctos
- [x] Código robusto ante datos inválidos
