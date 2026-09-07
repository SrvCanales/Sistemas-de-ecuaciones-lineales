from google import genai
from google.genai import types
import subprocess
import os
from fractions import Fraction

def calcular_historial_gauss(matriz_entrada):
    M = [[Fraction(val) for val in fila] for fila in matriz_entrada]
    filas, cols = len(M), len(M[0])
    historial = ["Matriz inicial:\n" + str([[str(c) for c in f] for f in M])]
    
    lead = 0
    for r in range(filas):
        if lead >= cols - 1: break
        if M[r][lead] == 0:
            for i in range(r + 1, filas):
                if M[i][lead] != 0:
                    M[r], M[i] = M[i], M[r]
                    historial.append(f"Intercambio $F_{r+1} \\leftrightarrow F_{i+1}$:\n" + str([[str(c) for c in f] for f in M]))
                    break
        
        pivote = M[r][lead]
        if pivote != 0:
            if pivote != 1:
                M[r] = [x / pivote for x in M[r]]
                historial.append(f"$F_{r+1} \\rightarrow \\frac{{1}}{{{pivote}}} F_{r+1}$:\n" + str([[str(c) for c in f] for f in M]))
            
            for k in range(filas):
                if k != r and M[k][lead] != 0:
                    factor = M[k][lead]
                    M[k] = [M[k][j] - factor * M[r][j] for j in range(cols)]
                    historial.append(f"$F_{k+1} \\rightarrow F_{k+1} - ({factor})F_{r+1}$:\n" + str([[str(c) for c in f] for f in M]))
        lead += 1
    return "\n\n".join(historial)

def generar_pdf_con_gemini(matriz, solucion, api_key):
    try:
        # 1. Proveedor: Inicializamos el cliente pasando la VARIABLE api_key (sin comillas)

        client = genai.Client(api_key=api_key)

        historial_exacto = calcular_historial_gauss(matriz)

        # 2. Prompt LATEX
        prompt = f"""
    Eres un tipógrafo matemático experto en LaTeX.
    A continuación, te entrego el historial EXACTO paso a paso de la resolución de un sistema de ecuaciones:
    
    {historial_exacto}
    
    REGLAS ESTRICTAS:
    1. Tu tarea es convertir este texto crudo en código LaTeX válido y elegante.
    2. NO alteres ningún número ni fracción. Usa exactamente las matrices provistas.
    3. Escribe una frase explicativa esclarecedora entre cada matriz usando las operaciones indicadas (ej. Aplicamos $F_2 \\rightarrow F_2 - 2F_1$).
    4. Responde ÚNICAMENTE con el contenido LaTeX (sin \\documentclass ni preámbulos)
    5. Encasilla el resultado para cada incógnita, e interpreta la solución (sistema compatible determinado/indeterminado o incompatible y por qué es así)
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
