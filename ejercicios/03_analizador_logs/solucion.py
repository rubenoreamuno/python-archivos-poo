#!/usr/bin/env python3
"""
Ejercicio 3: Analizador de Logs de Servidor
Procesa logs, extrae estadísticas y genera reportes
"""

from pathlib import Path
from collections import Counter


class EntradaLog:
    """Representa una entrada individual del log"""
    
    def __init__(self, fecha, hora, nivel, mensaje):
        self.fecha = fecha
        self.hora = hora
        self.nivel = nivel
        self.mensaje = mensaje
    
    @classmethod
    def parsear_linea(cls, linea):
        """
        Parsea una línea de log
        Formato: "2024-01-20 08:15:23 INFO Server started on port 8080"
        """
        partes = linea.strip().split(' ', 3)
        if len(partes) < 4:
            return None
        
        fecha = partes[0]
        hora = partes[1]
        nivel = partes[2]
        mensaje = partes[3]
        
        return cls(fecha, hora, nivel, mensaje)
    
    @property
    def es_error(self):
        """Verifica si es un error"""
        return self.nivel == 'ERROR'
    
    @property
    def es_warning(self):
        """Verifica si es una advertencia"""
        return self.nivel == 'WARNING'
    
    @property
    def hora_del_dia(self):
        """Extrae la hora (formato HH:MM:SS -> HH)"""
        return self.hora.split(':')[0]
    
    def __str__(self):
        return f"{self.fecha} {self.hora} [{self.nivel}] {self.mensaje}"


class AnalizadorLogs:
    """Analizador de logs con estadísticas y reportes"""
    
    def __init__(self, archivo_log):
        self.archivo_log = Path(archivo_log)
        self.entradas = []
    
    def cargar_log(self):
        """Carga y parsea el archivo de log línea por línea"""
        try:
            with open(self.archivo_log, 'r', encoding='utf-8') as f:
                for linea in f:
                    entrada = EntradaLog.parsear_linea(linea)
                    if entrada:
                        self.entradas.append(entrada)
            print(f"✅ Cargadas {len(self.entradas)} entradas de log")
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {self.archivo_log}")
            raise
    
    def contar_por_nivel(self):
        """Cuenta eventos por nivel (INFO, WARNING, ERROR)"""
        conteo = Counter(entrada.nivel for entrada in self.entradas)
        return dict(conteo)
    
    def contar_por_hora(self):
        """Cuenta eventos por hora del día"""
        conteo = Counter(entrada.hora_del_dia for entrada in self.entradas)
        return dict(sorted(conteo.items()))
    
    def mensajes_frecuentes(self, top_n=5):
        """Retorna los N mensajes más frecuentes"""
        mensajes = [entrada.mensaje for entrada in self.entradas]
        conteo = Counter(mensajes)
        return conteo.most_common(top_n)
    
    def porcentaje_errores(self):
        """Calcula el porcentaje de errores sobre el total"""
        if not self.entradas:
            return 0.0
        errores = sum(1 for e in self.entradas if e.es_error)
        return (errores / len(self.entradas)) * 100
    
    def obtener_errores(self):
        """Retorna lista de todas las entradas de error"""
        return [e for e in self.entradas if e.es_error]
    
    def obtener_warnings(self):
        """Retorna lista de todas las advertencias"""
        return [e for e in self.entradas if e.es_warning]
    
    def buscar_patron(self, patron):
        """Busca un patrón en los mensajes"""
        return [
            e for e in self.entradas
            if patron.lower() in e.mensaje.lower()
        ]
    
    def generar_reporte(self, archivo_salida):
        """Genera un reporte completo de análisis"""
        archivo_salida = Path(archivo_salida)
        archivo_salida.parent.mkdir(parents=True, exist_ok=True)
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("=" * 50 + "\n")
            f.write("      ANÁLISIS DE LOGS DE SERVIDOR\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total de eventos: {len(self.entradas)}\n\n")
            
            # Eventos por nivel
            f.write("--- Eventos por Nivel ---\n")
            conteo_nivel = self.contar_por_nivel()
            total = len(self.entradas)
            for nivel in ['INFO', 'WARNING', 'ERROR']:
                cantidad = conteo_nivel.get(nivel, 0)
                porcentaje = (cantidad / total * 100) if total > 0 else 0
                f.write(f"{nivel}: {cantidad} ({porcentaje:.1f}%)\n")
            f.write("\n")
            
            # Eventos por hora
            f.write("--- Eventos por Hora ---\n")
            conteo_hora = self.contar_por_hora()
            for hora, cantidad in conteo_hora.items():
                f.write(f"{hora}:00 - {cantidad} eventos\n")
            f.write("\n")
            
            # Top 5 mensajes
            f.write("--- Top 5 Mensajes Más Frecuentes ---\n")
            top_mensajes = self.mensajes_frecuentes(5)
            for i, (mensaje, cantidad) in enumerate(top_mensajes, 1):
                # Truncar mensajes muy largos
                msg_corto = mensaje[:60] + '...' if len(mensaje) > 60 else mensaje
                f.write(f"{i}. {msg_corto} ({cantidad} veces)\n")
            f.write("\n")
            
            # Alertas y patrones críticos
            f.write("--- ALERTAS Y PATRONES CRÍTICOS ---\n")
            
            errores = self.obtener_errores()
            if errores:
                f.write(f"🔴 {len(errores)} errores detectados ({self.porcentaje_errores():.1f}% del total)\n")
                f.write("   Errores:\n")
                for error in errores[:5]:  # Mostrar máximo 5
                    f.write(f"   - {error.fecha} {error.hora}: {error.mensaje}\n")
            
            # Patrones específicos
            db_failures = self.buscar_patron('database')
            auth_failures = self.buscar_patron('authentication failed')
            
            if db_failures:
                f.write(f"⚠️  {len(db_failures)} eventos relacionados con base de datos\n")
            
            if auth_failures:
                f.write(f"⚠️  {len(auth_failures)} fallos de autenticación\n")
            
            if not errores and not db_failures and not auth_failures:
                f.write("✅ No se detectaron patrones críticos\n")
        
        print(f"📊 Reporte generado en: {archivo_salida}")


def main():
    """Función principal"""
    # Rutas
    archivo_log = Path('data/server.log')
    archivo_reporte = Path('output/analisis_logs.txt')
    
    # Crear analizador
    analizador = AnalizadorLogs(archivo_log)
    analizador.cargar_log()
    
    # Mostrar estadísticas en consola
    print(f"\n📊 Estadísticas rápidas:")
    print(f"   Total eventos: {len(analizador.entradas)}")
    
    conteo = analizador.contar_por_nivel()
    print(f"   INFO: {conteo.get('INFO', 0)}")
    print(f"   WARNING: {conteo.get('WARNING', 0)}")
    print(f"   ERROR: {conteo.get('ERROR', 0)}")
    print(f"   Porcentaje de errores: {analizador.porcentaje_errores():.1f}%")
    
    # Generar reporte completo
    analizador.generar_reporte(archivo_reporte)
    
    print(f"\n✨ Análisis completado!\n")


if __name__ == '__main__':
    main()
