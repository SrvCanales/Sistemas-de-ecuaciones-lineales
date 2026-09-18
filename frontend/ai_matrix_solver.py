from google import genai
from google.genai import types
import urllib.parse
import requests
from fractions import Fraction
import sympy as sp

def calcular_historial_cramer(matriz_entrada):
    A = sp.Matrix([fila[:-1] for fila in matriz_entrada])
    B = sp.Matrix([fila[-1] for fila in matriz_entrada])
    n = A.shape[0]
    det_A = A.det()
    
    if det_A == 0:
        return "El determinante es 0. El sistema no se puede resolver por la Regla de Cramer."
    
    historial = [f"Calculamos el determinante de la matriz de coeficientes $A$:\n$A = {sp.latex(A)}$"]
    
    # Detallar el cálculo del determinante expandiendo por la primera fila (para 3x3 o mayor)
    if n >= 3:
        expansion = "\\det(A) = "
        for j in range(n):
            M_0j = A.copy()
            M_0j.row_del(0)
            M_0j.col_del(j)
            signo = "+" if j % 2 == 0 else "-"
            expansion += f"{signo} ({A[0,j]}) \\det({sp.latex(M_0j)}) "
        historial.append(expansion + f" = {det_A}")
    else:
        historial.append(f"\\det(A) = {det_A}")
    
    variables = ['x', 'y', 'z', 'w'][:n]
    
    for i in range(n):
        A_mod = A.copy()
        A_mod.col_op(i, lambda v, j: B[j])
        det_mod = A_mod.det()
        valor_var = det_mod / det_A
        
        paso = f"Para la variable ${variables[i]}$, reemplazamos la columna {i+1} de $A$ con el vector $B$:\n$A_{variables[i]} = {sp.latex(A_mod)}$\n"
        
        # Expandir también el cálculo del determinante modificado
        if n >= 3:
            paso += f"\\det(A_{variables[i]}) = "
            for j in range(n):
                M_0j = A_mod.copy()
                M_0j.row_del(0)
                M_0j.col_del(j)
                signo = "+" if j % 2 == 0 else "-"
                paso += f"{signo} ({A_mod[0,j]}) \\det({sp.latex(M_0j)}) "
            paso += f" = {det_mod}\n"
        else:
            paso += f"\\det(A_{variables[i]}) = {det_mod}\n"

        paso += f"${variables[i]} = \\frac{{\\det(A_{variables[i]})}}{{\\det(A)}} = \\frac{{{det_mod}}}{{{det_A}}} = {valor_var}$"
        historial.append(paso)
        
    return "\n\n".join(historial)

def calcular_historial_inversa_adjunta(matriz_entrada):
    A = sp.Matrix([fila[:-1] for fila in matriz_entrada])
    B = sp.Matrix([fila[-1] for fila in matriz_entrada])
    n = A.shape[0]
    det_A = A.det()
    
    if det_A == 0: return "Determinante 0. No es invertible."
    
    historial = [
        f"1. Calculamos el determinante de la matriz $A$:\n\\det(A) = {det_A}",
        "2. Calculamos la matriz de cofactores $C$. Para cada elemento, el cofactor es $C_{ij} = (-1)^{i+j} \\det(M_{ij})$:"
    ]
    
    C = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            M_ij = A.copy()
            M_ij.row_del(i)
            M_ij.col_del(j)
            det_Mij = M_ij.det()
            cofactor = ((-1)**(i+j)) * det_Mij
            C[i,j] = cofactor
            # Mostrar explícitamente de dónde sale cada número
            historial.append(f"C_{{{i+1}{j+1}}} = (-1)^{{{i+1}+{j+1}}} \\det({sp.latex(M_ij)}) = ({-1 if (i+j)%2!=0 else 1})({det_Mij}) = {cofactor}")
    
    adj_A = C.T
    A_inv = adj_A / det_A
    X = A_inv * B
    
    historial.append(f"Matriz de cofactores $C$:\n$C = {sp.latex(C)}$")
    historial.append(f"3. Transponemos $C$ para obtener la Matriz Adjunta:\n\\text{{Adj}}(A) = C^T = {sp.latex(adj_A)}")
    historial.append(f"4. Aplicamos $A^{{-1}} = \\frac{{1}}{{\\det(A)}} \\text{{Adj}}(A)$:\n$A^{{-1}} = {sp.latex(A_inv)}$")
    historial.append(f"5. Multiplicamos $X = A^{{-1}} B$ para obtener la solución final:\n$X = {sp.latex(X)}$")
    
    return "\n\n".join(historial)

def calcular_historial_inversa_gauss(matriz_entrada):
    n = len(matriz_entrada)
    # 1. Construir matriz aumentada [A | I] con fracciones exactas
    M = []
    for i, fila in enumerate(matriz_entrada):
        fila_frac = [Fraction(val) for val in fila[:-1]]
        identidad = [Fraction(1) if i == j else Fraction(0) for j in range(n)]
        M.append(fila_frac + identidad)
        
    filas, cols = n, 2*n
    historial = ["Matriz aumentada inicial $[A | I]$:\n" + str([[str(c) for c in f] for f in M])]
    
    # 2. Replicar el algoritmo paso a paso
    lead = 0
    for r in range(filas):
        if lead >= n: break
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
        
    # 3. Extraer matriz inversa final y multiplicar por B (usando SymPy para la limpieza visual final)
    A = sp.Matrix([fila[:-1] for fila in matriz_entrada])
    B = sp.Matrix([fila[-1] for fila in matriz_entrada])
    A_inv = A.inv()
    X = A_inv * B
    
    historial.append(f"La mitad derecha es ahora nuestra matriz inversa $A^{{-1}}$:\n$A^{{-1}} = {sp.latex(A_inv)}$")
    historial.append(f"Finalmente, resolvemos el sistema multiplicando $X = A^{{-1}} B$:\n$X = {sp.latex(X)}$")
    
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

def generar_pdf_con_gemini(matriz, metodo, api_key):
    try:
        client = genai.Client(api_key=api_key)

        if metodo == "gauss":
            historial = calcular_historial_gauss(matriz)
        elif metodo == "cramer":
            historial = calcular_historial_cramer(matriz)
        elif metodo == "inversa_gauss":
            historial = calcular_historial_inversa_gauss(matriz)
        elif metodo == "inversa_adjunta":
            historial = calcular_historial_inversa_adjunta(matriz)
        else:
            historial = calcular_historial_gauss(matriz)

        # Modificamos el prompt para asegurar que Gemini muestre estos nuevos pasos claramente
        prompt = f"""
    Eres un tipógrafo matemático experto en LaTeX. Debes maquetar la resolución paso a paso de un sistema de ecuaciones utilizando el método de: {metodo.upper()}
    A continuación, te entrego el historial EXACTO paso a paso generado por un motor algebraico:
    
    {historial}
    
    REGLAS ESTRICTAS:
    1. Convierte este texto crudo en código LaTeX válido y elegante.
    2. NO alteres ningún número ni fracción. Usa exactamente los cálculos matemáticos provistos.
    3. Si el método involucra operaciones de fila (Gauss), escribe la matriz completa y la operación realizada al lado (ej. $F_2 \\rightarrow F_2 - 2F_1$).
    4. Si el método involucra determinantes o cofactores, muestra la expansión de los cálculos intermedios tal como se proveen en el historial. Muestra cada cofactor por separado si se proveen.
    5. Responde ÚNICAMENTE con el contenido LaTeX (sin \\documentclass ni preámbulos).
    6. Al final de la resolución, encasilla claramente el vector de solución final. """

        respuesta = client.models.generate_content(
            model='gemini-3.5-flash-lite', 
            contents=prompt
        )
        
        contenido_latex = respuesta.text.replace("```latex", "").replace("```", "").strip()

        documento_completo = r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{amsmath, amssymb}
\usepackage[margin=2.5cm]{geometry}
\begin{document}
\section*{Resolución del Sistema}
""" + contenido_latex + r"""
\end{document}
"""

        codigo_url = urllib.parse.quote(documento_completo)
        url_compilador = f"https://latexonline.cc/compile?text={codigo_url}"
        
        respuesta_pdf = requests.get(url_compilador)
        
        if respuesta_pdf.status_code == 200:
            return respuesta_pdf.content, None 
        else:
            return None, "Error en el servidor externo al compilar el documento LaTeX."

    except Exception as e:
        return None, str(e)
