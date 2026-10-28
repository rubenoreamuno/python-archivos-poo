# Databricks notebook source
# Listas []
# Se pueden iterar --> recorrer

lista = [1,2,3,4,5]

# COMMAND ----------

lista[2] = 4

# COMMAND ----------

lista

# COMMAND ----------

for i in lista:
  print(i)

# COMMAND ----------

# Tuplas ()
# Inmutables --> no se pueden alterar
tupla = (('nombre', 'Juan'), ('apellido', 'Perez'))

# COMMAND ----------

tupla[1][0]

# COMMAND ----------

tupla[0][1] = "Ruben"

# COMMAND ----------

for i in tupla:
    print(i)

# COMMAND ----------

# Diccionarios {}
# 

orden = {
    'nombre': 'Juan',
    'apellido': 'Perez',
    'edad': 20,
    'direccion': 'Calle 123',
    'telefono': '1234567890',
    'email': 'juan.perez@gmail.com',
    'ciudad': 'Bogota',
    'pais': 'Colombia',
    'codigo_postal': '12345',
    'productos' : ['producto1', 'producto2', 'producto3']
}

# COMMAND ----------

orden['total'] = 12500

# COMMAND ----------

orden

# COMMAND ----------

orden.items()

# COMMAND ----------

for i in orden.keys():
    print(i)

# COMMAND ----------

for i in orden.values():
    print(i)

# COMMAND ----------

orden['productos']