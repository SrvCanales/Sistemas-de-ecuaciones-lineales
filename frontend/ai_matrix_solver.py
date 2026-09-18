from google import genai
from google.genai import types
import subprocess
import os
from fractions import Fraction

def calcular_historial_cramer(matriz_entrada):
    # Separar matriz de coeficientes (A) y términos independientes (B)
    A = sp.Matrix([fila[:-1] for fila in matriz_entrada])
    B = sp.Matrix([fila[-1] for fila in matriz_entrada])
    
    det_A = A.det()
    historial = [f"Calculamos el determinante de la matriz de coeficientes $A$:\n\\det(A) = {det_A}"]
    
    if det_A == 0:
        return "El determinante es 0. El sistema no se puede resolver por la Regla de Cramer."
    
    variables = ['x', 'y', 'z', 'w'] # Adaptar según tamaño
    
    for i in range(A.shape[1]):
        # Crear matriz modificada reemplazando la columna i con B
        A_mod = A.copy()
        A_mod.col_op(i, lambda v, j: B[j])
        det_mod = A_mod.det()
        valor_var = det_mod / det_A
        
        paso = (f"Para la variable ${variables[i]}$, reemplazamos la columna {i+1} de $A$ con el vector $B$:\n"
                f"\\det(A_{variables[i]}) = {det_mod}\n"
                f"${variables[i]} = \\frac{{{det_mod}}}{{{det_A}}} = {valor_var}$")
        historial.append(paso)
        
    return "\n\n".join(historial)

def calcular_historial_inversa_adjunta(matriz_entrada):
    A = sp.Matrix([fila[:-1] for fila in matriz_entrada])
    B = sp.Matrix([fila[-1] for fila in matriz_entrada])
    det_A = A.det()
    
    if det_A == 0: return "Determinante 0. No es invertible."
    
    # SymPy calcula la adjunta directamente con .adjugate()
    adj_A = A.adjugate()
    A_inv = adj_A / det_A
    X = A_inv * B
    
    historial = [
        f"Calculamos el determinante:\n\\det(A) = {det_A}",
        f"Calculamos la matriz de cofactores transpuesta (Adjunta):\n\\text{{Adj}}(A) = {sp.latex(adj_A)}",
        f"Aplicamos $A^{{-1}} = \\frac{{1}}{{\\det(A)}} \\text{{Adj}}(A)$:\n$A^{{-1}} = {sp.latex(A_inv)}$",
        f"Multiplicamos $X = A^{{-1}} B$:\n$X = {sp.latex(X)}$"
    ]
    return "\n\n".join(historial)

def calcular_historial_inversa_gauss(matriz_entrada):
    A = sp.Matrix([fila[:-1] for fila in matriz_entrada])
    B = sp.Matrix([fila[-1] for fila in matriz_entrada])
    n = A.shape[0]
    
    if A.det() == 0: return "Determinante 0. No es invertible."
    
    # Creamos la matriz aumentada [A | I]
    I = sp.eye(n)
    A_aumentada = A.row_join(I)
    
    # SymPy hace Gauss-Jordan y devuelve la matriz reducida
    A_reducida, _ = A_aumentada.rref()
    
    # Extraemos la mitad derecha, que ahora es A^-1
    A_inv = A_reducida[:, n:]
    X = A_inv * B
    
    historial = [
        f"Construimos la matriz aumentada con la Identidad $[A | I]$:\n{sp.latex(A_aumentada)}",
        f"Aplicamos operaciones elementales de fila (Gauss-Jordan) hasta obtener $[I | A^{{-1}}]$:\n{sp.latex(A_reducida)}",
        f"Extraemos la matriz inversa $A^{{-1}}$:\n$A^{{-1}} = {sp.latex(A_inv)}$",
        f"Multiplicamos $X = A^{{-1}} B$:\n$X = {sp.latex(X)}$"
    ]
    return "\n\n".join(historial)

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

def generar_pdf_con_gemini(matriz, metodo, solucion, api_key):
    try:
        # 1. Proveedor: Inicializamos el cliente pasando la VARIABLE api_key

        client = genai.Client(api_key=api_key)

        if metodo == "gauss":
            historial = calcular_historial_gauss(matriz)
        elif metodo == "cramer":
            historial = calcular_historial_cramer(matriz)
        elif metodo == "inversa_gauss":
            historial = calcular_historial_inversa_gauss(matriz)
        elif metodo == "inversa_adjunta":
            historial = calcular_historial_inversa_adjunta(matriz)

        # 2. Prompt LATEX
        prompt = f"""
    Eres un tipógrafo matemático experto en LaTeX. Debes maquetar la resolución paso a paso de un sistema de ecuaciones utilizando el método de: {metodo.upper()}
    A continuación, te entrego el historial EXACTO paso a paso de la resolución de un sistema de ecuaciones:
    
    {historial}
    
    REGLAS ESTRICTAS:
    1. Tu tarea es convertir este texto crudo en código LaTeX válido y elegante.
    2. NO alteres ningún número ni fracción. Usa exactamente las matrices y determinantes exactamente como se muestran. 
    3. Escribe una frase explicativa pequeña entre cada matriz usando las operaciones indicadas (ej. Aplicamos $F_2 \\rightarrow F_2 - 2F_1$).
    4. Responde ÚNICAMENTE con el contenido LaTeX (sin \\documentclass ni preámbulos)
    5. Encasilla el resultado para cada incógnita, e interpreta la solución (sistema compatible determinado/indeterminado o incompatible y por qué es así) """

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

        # 5. Enviar el código a la API externa de compilación LaTeX
        import urllib.parse
        import requests
        
        codigo_url = urllib.parse.quote(documento_completo)
        url_compilador = f"https://latexonline.cc/compile?text={codigo_url}"
        
        respuesta_pdf = requests.get(url_compilador)
        
        if respuesta_pdf.status_code == 200:
            return respuesta_pdf.content, None # Devuelve los bytes del PDF
        else:
            return None, "Error en el servidor externo al compilar el documento LaTeX."

    except Exception as e:
        return None, str(e)

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
