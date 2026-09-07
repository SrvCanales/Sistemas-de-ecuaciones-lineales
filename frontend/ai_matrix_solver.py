from google import genai
from google.genai import types
import subprocess
import os

def generar_pdf_con_gemini(matriz, solucion, api_key):
    try:
        # 1. Proveedor: Inicializamos el cliente pasando la VARIABLE api_key (sin comillas)
        client = genai.Client(api_key=api_key)

        # 2. Prompt LATEX
        prompt = f"""
        Resuelve ordenadamente el siguiente sistema de ecuaciones representado por esta matriz ampliada:
        {matriz}

         REGLAS ESTRICTAS DE FORMATO:
        1. Tu respuesta debe ser ÚNICAMENTE código LaTeX válido. Cero comentarios fuera del código.
        2. NO uses bloques de código markdown (```latex ... ```). Escribe el código directamente.
        3. NO incluyas \\documentclass, ni \\usepackage, ni \\begin{{document}} ni \\end{{document}}.
        4. Utiliza únicamente los paquetes estándar de amsmath y amssymb (ej. pmatrix, bmatrix, align*).
        5. NO uses comandos que requieran otros paquetes extras (como \\cancel, \\color, \\systeme).
        6. Asegúrate de cerrar correctamente todas las llaves y entornos.
        7. Tu respuesta debe ser de izquierda a derecha, de arriba a abajo, respetando los márgenes de la página

        REQUISITO CLAVE = Tu desarrollo debe ser coherente con la solución {solucion}. No aproximes.

        REGLA ESTRICTA: Obtén la forma escalonada a partir de la forma aumentada de la matriz. Luego resuelve cada ecuación resultante. Tu respuesta debe estar escrita ÚNICAMENTE en código LaTeX válido. 
        No uses bloques de código (```latex). Escribe directamente el texto y las fórmulas usando entornos como \\begin{{pmatrix}} y \\begin{{align*}}.
        No incluyas el preámbulo (\\documentclass), solo el contenido del documento.
        """

        # 3. Llamar a la API usando la SINTAXIS NUEVA
        # El modelo se indica directamente dentro de generate_content
        respuesta = client.models.generate_content(
            model='gemini-3.5-flash-lite', # Puedes usar gemini-1.5-flash o gemini-pro
            contents=prompt
        )
        
        # Doble limpieza por si la IA ignora la regla 2
        contenido_latex = respuesta.text.replace("```latex", "").replace("```", "").strip()

        # 4. Ensamblar el documento LaTeX completo
        documento_completo = r"""
\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{amsmath, amssymb}
\usepackage[margin=2.5cm]{geometry}
\begin{document}
\section*{Resolución del Sistema}
""" + contenido_latex + r"""
\end{document}
"""

        # 5. Guardar el archivo .tex temporal
        with open("temp_resolucion.tex", "w", encoding="utf-8") as f:
            f.write(documento_completo)

        # 6. Compilar el PDF llamando al sistema operativo (pdflatex)
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "temp_resolucion.tex"],
            stdout=subprocess.DEVNULL, # Oculta los logs de compilación en la consola
            check=True
        )

        # 7. Leer el PDF generado en formato binario
        with open("temp_resolucion.pdf", "rb") as pdf_file:
            pdf_bytes = pdf_file.read()

        # 8. Limpieza de archivos temporales (.tex, .aux, .log, .pdf)
        for ext in [".tex", ".aux", ".log", ".pdf"]:
            if os.path.exists(f"temp_resolucion{ext}"):
                os.remove(f"temp_resolucion{ext}")

        return pdf_bytes, None # Si todo sale bien, devuelve el PDF y "Ningún error"

    except Exception as e:
        # Si algo falla, devuelve None para el PDF y el mensaje del error
        return None, str(e)
