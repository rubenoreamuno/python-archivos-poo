#!/usr/bin/env python3
"""
Ejercicio 7: Analizador de Frecuencia de Palabras
Análisis lingüístico de texto con estadísticas y visualización
"""

import string
from pathlib import Path
from collections import Counter


class AnalizadorTexto:
    """Analizador de frecuencia y estadísticas de texto"""
    
    # Stopwords comunes en español (palabras vacías)
    STOPWORDS = {
        'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'haber',
        'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'lo', 'todo',
        'pero', 'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir', 'otro', 'ese',
        'la', 'si', 'me', 'ya', 'ver', 'porque', 'dar', 'cuando', 'él', 'muy',
        'sin', 'vez', 'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo',
        'yo', 'también', 'hasta', 'año', 'dos', 'querer', 'entre', 'así', 'primero',
        'desde', 'grande', 'eso', 'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella',
        'sí', 'día', 'uno', 'bien', 'poco', 'deber', 'entonces', 'poner', 'cosa',
        'tanto', 'hombre', 'parecer', 'nuestro', 'tan', 'donde', 'ahora', 'parte',
        'después', 'vida', 'quedar', 'siempre', 'creer', 'hablar', 'llevar', 'dejar',
        'nada', 'cada', 'seguir', 'menos', 'nuevo', 'encontrar', 'algo', 'solo',
        'decir', 'salir', 'volver', 'tomar', 'conocer', 'vivir', 'sentir', 'tratar',
        'mirar', 'contar', 'empezar', 'esperar', 'buscar', 'existir', 'entrar',
        'trabajar', 'escribir', 'perder', 'producir', 'ocurrir', 'entender', 'pedir',
        'recibir', 'recordar', 'terminar', 'permitir', 'aparecer', 'conseguir', 'comenzar',
        'servir', 'sacar', 'necesitar', 'mantener', 'resultar', 'leer', 'caer', 'cambiar',
        'presentar', 'crear', 'abrir', 'considerar', 'oír', 'acabar', 'mil', 'evitar',
    }
    
    def __init__(self, archivo_texto):
        self.archivo = Path(archivo_texto)
        self.texto_original = ""
        self.texto_limpio = ""
        self.palabras = []
        self.palabras_filtradas = []
    
    def cargar_texto(self):
        """Carga el archivo de texto"""
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                self.texto_original = f.read()
            print(f"✅ Texto cargado: {len(self.texto_original)} caracteres")
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {self.archivo}")
            raise
    
    def limpiar_texto(self):
        """Limpia el texto: minúsculas y elimina puntuación"""
        # Convertir a minúsculas
        texto = self.texto_original.lower()
        
        # Eliminar puntuación
        translator = str.maketrans('', '', string.punctuation + '¡¿')
        texto = texto.translate(translator)
        
        self.texto_limpio = texto
    
    def tokenizar(self):
        """Separa el texto en palabras (tokens)"""
        self.palabras = self.texto_limpio.split()
    
    def filtrar_stopwords(self):
        """Filtra palabras vacías comunes"""
        self.palabras_filtradas = [
            palabra for palabra in self.palabras
            if palabra not in self.STOPWORDS and len(palabra) > 2
        ]
    
    def procesar(self):
        """Ejecuta el pipeline completo de procesamiento"""
        self.cargar_texto()
        self.limpiar_texto()
        self.tokenizar()
        self.filtrar_stopwords()
    
    def contar_frecuencias(self, filtradas=True):
        """Cuenta la frecuencia de cada palabra"""
        palabras = self.palabras_filtradas if filtradas else self.palabras
        return Counter(palabras)
    
    def top_palabras(self, n=10, filtradas=True):
        """Retorna las N palabras más frecuentes"""
        frecuencias = self.contar_frecuencias(filtradas)
        return frecuencias.most_common(n)
    
    def palabras_unicas(self):
        """Retorna palabras que aparecen solo una vez"""
        frecuencias = self.contar_frecuencias(filtradas=True)
        return [palabra for palabra, freq in frecuencias.items() if freq == 1]
    
    def longitud_promedio_palabras(self):
        """Calcula la longitud promedio de las palabras"""
        if not self.palabras_filtradas:
            return 0
        return sum(len(p) for p in self.palabras_filtradas) / len(self.palabras_filtradas)
    
    def total_palabras(self):
        """Total de palabras (sin filtrar)"""
        return len(self.palabras)
    
    def palabras_unicas_count(self):
        """Cantidad de palabras únicas (filtradas)"""
        return len(set(self.palabras_filtradas))
    
    def generar_histograma_ascii(self, frecuencias, max_barras=20, ancho_barra=40):
        """
        Genera un histograma ASCII
        
        Args:
            frecuencias: Lista de tuplas (palabra, frecuencia)
            max_barras: Número máximo de barras a mostrar
            ancho_barra: Ancho máximo de la barra en caracteres
        """
        if not frecuencias:
            return "No hay datos para mostrar"
        
        # Limitar cantidad de barras
        frecuencias = frecuencias[:max_barras]
        
        # Encontrar el valor máximo para escalar
        max_freq = max(freq for _, freq in frecuencias)
        
        histograma = []
        for i, (palabra, freq) in enumerate(frecuencias, 1):
            # Calcular longitud de barra proporcional
            longitud_barra = int((freq / max_freq) * ancho_barra)
            barra = '█' * longitud_barra
            
            # Formatear línea
            linea = f"{i:2}. {palabra:20} {barra} {freq}"
            histograma.append(linea)
        
        return '\n'.join(histograma)
    
    def generar_reporte(self, archivo_salida):
        """Genera un reporte completo de análisis"""
        archivo_salida = Path(archivo_salida)
        archivo_salida.parent.mkdir(parents=True, exist_ok=True)
        
        # Obtener datos
        top_10 = self.top_palabras(10, filtradas=True)
        unicas = self.palabras_unicas()
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("=" * 60 + "\n")
            f.write("       ANÁLISIS DE FRECUENCIA DE PALABRAS\n")
            f.write("=" * 60 + "\n\n")
            
            # Estadísticas generales
            f.write(f"Archivo analizado: {self.archivo.name}\n")
            f.write(f"Total de caracteres: {len(self.texto_original):,}\n")
            f.write(f"Total de palabras: {self.total_palabras()}\n")
            f.write(f"Palabras únicas (significativas): {self.palabras_unicas_count()}\n")
            f.write(f"Longitud promedio: {self.longitud_promedio_palabras():.1f} caracteres\n")
            f.write("\n")
            
            # Top palabras con histograma
            f.write("--- Top 10 Palabras Más Frecuentes ---\n\n")
            f.write(self.generar_histograma_ascii(top_10, ancho_barra=30))
            f.write("\n\n")
            
            # Palabras únicas
            f.write("--- Palabras Únicas (1 aparición) ---\n")
            f.write(f"Total: {len(unicas)} palabras\n\n")
            if unicas:
                # Mostrar las primeras 20
                f.write("Ejemplos (primeras 20):\n")
                for i, palabra in enumerate(unicas[:20], 1):
                    f.write(f"{i}. {palabra}\n")
            
            # Estadísticas adicionales
            f.write("\n--- Estadísticas Adicionales ---\n")
            frecuencias = self.contar_frecuencias(filtradas=True)
            f.write(f"Palabra más larga: {max(self.palabras_filtradas, key=len)}\n")
            f.write(f"Palabra más corta: {min(self.palabras_filtradas, key=len)}\n")
            f.write(f"Palabra más frecuente: {top_10[0][0]} ({top_10[0][1]} veces)\n")
        
        print(f"📊 Reporte generado: {archivo_salida}")


def main():
    """Función principal"""
    print("📝 ANALIZADOR DE FRECUENCIA DE PALABRAS\n")
    
    # Crear analizador
    analizador = AnalizadorTexto('data/texto_analisis.txt')
    
    # Procesar texto
    print("⚙️  Procesando texto...")
    analizador.procesar()
    
    # Mostrar estadísticas en consola
    print(f"\n📊 Estadísticas:")
    print(f"   Total de palabras: {analizador.total_palabras()}")
    print(f"   Palabras únicas: {analizador.palabras_unicas_count()}")
    print(f"   Longitud promedio: {analizador.longitud_promedio_palabras():.1f} caracteres")
    
    print(f"\n🔝 Top 5 palabras:")
    for i, (palabra, freq) in enumerate(analizador.top_palabras(5), 1):
        print(f"   {i}. {palabra}: {freq} veces")
    
    # Generar reporte completo
    analizador.generar_reporte('output/analisis_frecuencias.txt')
    
    print(f"\n✨ Análisis completado!\n")


if __name__ == '__main__':
    main()
