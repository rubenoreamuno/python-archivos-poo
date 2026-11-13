
# Datos de prueba: simulan self.notas (lista de dicts con id_estudiante y nota)
import types

self = types.SimpleNamespace(notas=[
    {'id_estudiante': '1001', 'nota': 80},
    {'id_estudiante': '1001', 'nota': 65.7},
    {'id_estudiante': '1001', 'nota': 89},
    {'id_estudiante': '1002', 'nota': 80},
    {'id_estudiante': '1002', 'nota': 65.7},
    {'id_estudiante': '1002', 'nota': 89},
    {'id_estudiante': '1003', 'nota': 80},
    {'id_estudiante': '1003', 'nota': 65.7},
    {'id_estudiante': '1003', 'nota': 89},
])




result = {
    '1001' : [80, 65.7, 89],
    '1002' : [80, 65.7, 89],
    '1003' : [80, 65.7, 89]
}

result = {}


for i in self.notas:
    try:
        result[i['id_estudiante']] = i['id_estudiante'].append(i['nota'])
    