# 📋 Cheatsheet: Archivos + POO en Python

> Referencia rápida de una página para manejo de archivos (txt, csv, json) y patrones POO comunes

---

## 📄 Archivos de Texto

```python
# Leer todo
with open('archivo.txt', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Leer líneas
with open('archivo.txt', 'r', encoding='utf-8') as f:
    lineas = f.readlines()  # ['linea1\n', 'linea2\n', ...]

# Iterar líneas (eficiente)
with open('archivo.txt', 'r', encoding='utf-8') as f:
    for linea in f:
        print(linea.strip())

# Escribir
with open('salida.txt', 'w', encoding='utf-8') as f:
    f.write('Línea 1\n')
    f.writelines(['Línea 2\n', 'Línea 3\n'])

# Anexar
with open('log.txt', 'a', encoding='utf-8') as f:
    f.write('Nueva entrada\n')
```

---

## 🗂️ CSV

```python
import csv

# Leer con DictReader (recomendado)
with open('datos.csv', 'r', encoding='utf-8', newline='') as f:
    lector = csv.DictReader(f)
    for fila in lector:
        print(fila['columna'])  # Acceso por nombre

# Leer con reader (listas)
with open('datos.csv', 'r', encoding='utf-8', newline='') as f:
    lector = csv.reader(f)
    encabezado = next(lector)
    for fila in lector:
        print(fila[0])  # Acceso por índice

# Escribir con DictWriter (recomendado)
with open('salida.csv', 'w', encoding='utf-8', newline='') as f:
    columnas = ['nombre', 'edad', 'nota']
    escritor = csv.DictWriter(f, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerow({'nombre': 'Ana', 'edad': 22, 'nota': 9.5})

# Escribir con writer (listas)
with open('salida.csv', 'w', encoding='utf-8', newline='') as f:
    escritor = csv.writer(f)
    escritor.writerow(['nombre', 'edad', 'nota'])
    escritor.writerow(['Ana', 22, 9.5])

# Delimitador personalizado
lector = csv.DictReader(f, delimiter=';')
escritor = csv.writer(f, delimiter='\t')
```

---

## 🔤 JSON

```python
import json

# Leer
with open('datos.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)  # dict o list

# Escribir
with open('salida.json', 'w', encoding='utf-8') as f:
    json.dump(datos, f, indent=4, ensure_ascii=False)

# Desde/a string
texto = json.dumps(datos, indent=2, ensure_ascii=False)
datos = json.loads(texto)

# Estructura anidada
datos = {
    'usuario': 'Ana',
    'cursos': [
        {'nombre': 'Python', 'nota': 9.5},
        {'nombre': 'Java', 'nota': 8.7}
    ]
}
print(datos['cursos'][0]['nota'])  # 9.5
```

---

## 🛣️ Pathlib

```python
from pathlib import Path

# Crear rutas
ruta = Path('data/archivo.csv')
ruta = Path.cwd() / 'data' / 'archivo.csv'  # Multiplataforma

# Propiedades
ruta.exists()          # True/False
ruta.is_file()         # True/False
ruta.is_dir()          # True/False
ruta.name              # 'archivo.csv'
ruta.stem              # 'archivo'
ruta.suffix            # '.csv'
ruta.parent            # Path('data')

# Crear directorios
Path('output').mkdir(exist_ok=True)
Path('output/reportes').mkdir(parents=True, exist_ok=True)

# Listar
for archivo in Path('data').iterdir():
    print(archivo)

for csv in Path('data').glob('*.csv'):
    print(csv)

# Leer/escribir
contenido = Path('archivo.txt').read_text(encoding='utf-8')
Path('salida.txt').write_text('Hola\n', encoding='utf-8')
```

---

## ⚠️ Excepciones

```python
try:
    with open('archivo.csv', 'r') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            edad = int(fila['edad'])
            nota = float(fila['nota'])
except FileNotFoundError:
    print('Archivo no encontrado')
except KeyError as e:
    print(f'Columna faltante: {e}')
except ValueError as e:
    print(f'Error de conversión: {e}')
except json.JSONDecodeError as e:
    print(f'JSON inválido: {e}')
```

---

## 🏗️ POO: Patrones Básicos

### Clase con to_dict / from_dict

```python
import json

class Estudiante:
    def __init__(self, nombre, edad, carrera):
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
    
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'edad': self.edad,
            'carrera': self.carrera
        }
    
    @classmethod
    def from_dict(cls, datos):
        return cls(
            nombre=datos['nombre'],
            edad=datos['edad'],
            carrera=datos['carrera']
        )
    
    def __str__(self):
        return f'{self.nombre} - {self.carrera}'
    
    def __repr__(self):
        return f'Estudiante({self.nombre!r}, {self.edad}, {self.carrera!r})'

# Uso
est = Estudiante('Ana', 22, 'Ingeniería')
datos = est.to_dict()

with open('estudiante.json', 'w', encoding='utf-8') as f:
    json.dump(datos, f, indent=4, ensure_ascii=False)

with open('estudiante.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)
    est2 = Estudiante.from_dict(datos)
```

### Clase con from_csv_row

```python
import csv

class Producto:
    def __init__(self, codigo, nombre, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
    
    @classmethod
    def from_csv_row(cls, fila):
        return cls(
            codigo=fila['codigo'],
            nombre=fila['nombre'],
            precio=float(fila['precio']),
            stock=int(fila['stock'])
        )
    
    def __str__(self):
        return f'{self.codigo}: {self.nombre} - ${self.precio:.2f} ({self.stock} unid.)'

# Uso
with open('productos.csv', 'r', encoding='utf-8', newline='') as f:
    lector = csv.DictReader(f)
    productos = [Producto.from_csv_row(fila) for fila in lector]
```

---

## 🏛️ POO: Patrón Repositorio/Gestor

```python
import json
from pathlib import Path

class RepositorioJSON:
    def __init__(self, archivo):
        self.archivo = Path(archivo)
        self.archivo.parent.mkdir(parents=True, exist_ok=True)
    
    def cargar(self):
        if not self.archivo.exists():
            return []
        with open(self.archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def guardar(self, datos):
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    
    def agregar(self, item):
        datos = self.cargar()
        datos.append(item)
        self.guardar(datos)
    
    def leer_todos(self):
        return self.cargar()

# Uso
repo = RepositorioJSON('data/estudiantes.json')
repo.agregar({'nombre': 'Ana', 'edad': 22})
todos = repo.leer_todos()
```

### Gestor con Clase de Dominio

```python
import csv
from pathlib import Path

class Estudiante:
    def __init__(self, nombre, edad, nota):
        self.nombre = nombre
        self.edad = edad
        self.nota = nota
    
    @classmethod
    def from_csv_row(cls, fila):
        return cls(fila['nombre'], int(fila['edad']), float(fila['nota']))
    
    def to_csv_row(self):
        return {'nombre': self.nombre, 'edad': self.edad, 'nota': self.nota}
    
    def __str__(self):
        return f'{self.nombre}: {self.nota}'

class GestorEstudiantes:
    def __init__(self, archivo):
        self.archivo = Path(archivo)
        self.estudiantes = []
    
    def cargar(self):
        with open(self.archivo, 'r', encoding='utf-8', newline='') as f:
            lector = csv.DictReader(f)
            self.estudiantes = [Estudiante.from_csv_row(fila) for fila in lector]
    
    def guardar(self, archivo_salida=None):
        archivo = archivo_salida or self.archivo
        with open(archivo, 'w', encoding='utf-8', newline='') as f:
            columnas = ['nombre', 'edad', 'nota']
            escritor = csv.DictWriter(f, fieldnames=columnas)
            escritor.writeheader()
            for est in self.estudiantes:
                escritor.writerow(est.to_csv_row())
    
    def agregar(self, estudiante):
        self.estudiantes.append(estudiante)
    
    def obtener_promedio(self):
        return sum(e.nota for e in self.estudiantes) / len(self.estudiantes)

# Uso
gestor = GestorEstudiantes('estudiantes.csv')
gestor.cargar()
gestor.agregar(Estudiante('Luis', 23, 9.0))
print(f'Promedio: {gestor.obtener_promedio():.2f}')
gestor.guardar('estudiantes_actualizado.csv')
```

---

## 🎨 POO: Dataclasses (Python 3.7+)

```python
from dataclasses import dataclass, asdict
import json

@dataclass
class Libro:
    titulo: str
    autor: str
    anio: int
    precio: float
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, datos):
        return cls(**datos)

# Uso
libro = Libro('Cien Años de Soledad', 'García Márquez', 1967, 25.99)
datos = libro.to_dict()

with open('libro.json', 'w', encoding='utf-8') as f:
    json.dump(datos, f, indent=4, ensure_ascii=False)
```

---

## 🧬 POO: Herencia

```python
import json
from abc import ABC, abstractmethod

class Publicacion(ABC):
    def __init__(self, titulo, anio):
        self.titulo = titulo
        self.anio = anio
    
    @abstractmethod
    def to_dict(self):
        pass
    
    def __str__(self):
        return f'{self.titulo} ({self.anio})'

class Libro(Publicacion):
    def __init__(self, titulo, anio, autor, isbn):
        super().__init__(titulo, anio)
        self.autor = autor
        self.isbn = isbn
    
    def to_dict(self):
        return {
            'tipo': 'libro',
            'titulo': self.titulo,
            'anio': self.anio,
            'autor': self.autor,
            'isbn': self.isbn
        }

class Revista(Publicacion):
    def __init__(self, titulo, anio, numero, editorial):
        super().__init__(titulo, anio)
        self.numero = numero
        self.editorial = editorial
    
    def to_dict(self):
        return {
            'tipo': 'revista',
            'titulo': self.titulo,
            'anio': self.anio,
            'numero': self.numero,
            'editorial': self.editorial
        }

# Factory
def cargar_publicacion(datos):
    if datos['tipo'] == 'libro':
        return Libro(datos['titulo'], datos['anio'], datos['autor'], datos['isbn'])
    elif datos['tipo'] == 'revista':
        return Revista(datos['titulo'], datos['anio'], datos['numero'], datos['editorial'])

# Uso
publicaciones = [
    Libro('Don Quijote', 1605, 'Cervantes', '978-1234567890'),
    Revista('National Geographic', 2024, 123, 'Nat Geo')
]

with open('publicaciones.json', 'w', encoding='utf-8') as f:
    json.dump([p.to_dict() for p in publicaciones], f, indent=4, ensure_ascii=False)

with open('publicaciones.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)
    publicaciones = [cargar_publicacion(d) for d in datos]
```

---

## 🛡️ POO: @property y Validación

```python
class Producto:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self._precio = 0
        self._stock = 0
        self.precio = precio  # Usa el setter
        self.stock = stock
    
    @property
    def precio(self):
        return self._precio
    
    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError('El precio no puede ser negativo')
        self._precio = valor
    
    @property
    def stock(self):
        return self._stock
    
    @stock.setter
    def stock(self, valor):
        if valor < 0:
            raise ValueError('El stock no puede ser negativo')
        self._stock = valor
    
    @property
    def valor_inventario(self):
        return self._precio * self._stock

# Uso
prod = Producto('Laptop', 1500.0, 10)
print(prod.valor_inventario)  # 15000.0
# prod.precio = -100  # Raise ValueError
```

---

## 🚨 Excepciones Personalizadas

```python
class ErrorValidacion(Exception):
    """Excepción base para errores de validación"""
    pass

class ErrorSaldoInsuficiente(ErrorValidacion):
    """Se lanza cuando no hay saldo suficiente"""
    pass

class ErrorDatoInvalido(ErrorValidacion):
    """Se lanza cuando un dato es inválido"""
    pass

class CuentaBancaria:
    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular
        self._saldo = saldo_inicial
    
    def retirar(self, monto):
        if monto <= 0:
            raise ErrorDatoInvalido('El monto debe ser positivo')
        if monto > self._saldo:
            raise ErrorSaldoInsuficiente(
                f'Saldo insuficiente: tienes ${self._saldo:.2f}, intentas retirar ${monto:.2f}'
            )
        self._saldo -= monto
    
    @property
    def saldo(self):
        return self._saldo

# Uso
try:
    cuenta = CuentaBancaria('Ana', 1000)
    cuenta.retirar(1500)
except ErrorSaldoInsuficiente as e:
    print(f'❌ {e}')
except ErrorDatoInvalido as e:
    print(f'❌ {e}')
```

---

## 📊 Patrón: Leer → Procesar → Escribir

```python
import csv
from pathlib import Path

# Leer CSV
with open('ventas.csv', 'r', encoding='utf-8', newline='') as f:
    lector = csv.DictReader(f)
    ventas = list(lector)

# Procesar
for venta in ventas:
    venta['total'] = float(venta['cantidad']) * float(venta['precio'])

# Escribir resultado
Path('output').mkdir(exist_ok=True)
with open('output/ventas_procesadas.csv', 'w', encoding='utf-8', newline='') as f:
    columnas = ['producto', 'cantidad', 'precio', 'total']
    escritor = csv.DictWriter(f, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(ventas)
```

---

## 🎯 Tips Finales

- ✅ **Siempre** usa `encoding='utf-8'`
- ✅ **Siempre** usa `newline=''` con CSV
- ✅ Usa `with` para cerrar archivos automáticamente
- ✅ Usa `pathlib.Path` en lugar de `os.path`
- ✅ Usa `ensure_ascii=False` en JSON para acentos
- ✅ Usa `indent=4` en JSON para formato legible
- ✅ Maneja excepciones específicas (`FileNotFoundError`, `JSONDecodeError`, `ValueError`)
- ✅ Usa `@classmethod` para constructores alternativos (`from_dict`, `from_csv_row`)
- ✅ Implementa `__str__` para representación legible
- ✅ Implementa `__repr__` para representación técnica
- ✅ Valida datos con `@property` setters
- ✅ Crea excepciones personalizadas para casos de negocio

---

**📖 Ver [README.md](README.md) para guía completa y [ejercicios/](ejercicios/) para práctica**
