from google import genai
import subprocess
import os

def generar_pdf_con_gemini(matriz, api_key):
    try:
        # 1. Proveedor: Inicializamos el cliente pasando la VARIABLE api_key (sin comillas)
        client = genai.Client(api_key=api_key)

        # 2. Prompt LATEX
        prompt = f"""
        Actúa como un profesor de álgebra lineal. 
        Resuelve paso a paso el siguiente sistema de ecuaciones representado por esta matriz ampliada:
        {matriz}
        
        REGLA ESTRICTA: Tu respuesta debe estar escrita ÚNICAMENTE en código LaTeX válido. 
        No uses bloques de código (```latex). Escribe directamente el texto y las fórmulas usando entornos como \\begin{{pmatrix}} y \\begin{{align*}}.
        No incluyas el preámbulo (\\documentclass), solo el contenido del documento.
        """

        # 3. Llamar a la API usando la SINTAXIS NUEVA
        # El modelo se indica directamente dentro de generate_content
        respuesta = client.models.generate_content(
            model='gemini-2.5-flash', # Puedes usar gemini-1.5-flash o gemini-pro
            contents=prompt
        )
        
        contenido_latex = respuesta.text.replace("```latex", "").replace("```", "") # Limpieza por seguridad

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
