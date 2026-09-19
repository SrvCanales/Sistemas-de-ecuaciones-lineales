from google import genai
from google.genai import types
import urllib.parse
import requests
from fractions import Fraction
import sympy as sp

PLANTILLAS_TEORICAS = {
    "gauss": r"""
\section*{Fundamentos: Método de Gauss-Jordan}
El objetivo de este método es transformar la matriz ampliada del sistema en su forma escalonada reducida. Esto permite leer la solución directamente de la matriz resultante.

\begin{tcolorbox}[colback=blue!5,colframe=blue!60!black,title=Operaciones Elementales de Fila válidas]
1. \textbf{Intercambio:} $F_i \leftrightarrow F_j$ (Intercambiar la posición de dos filas).\\
2. \textbf{Escalado:} $F_i \rightarrow kF_i$ con $k \neq 0$ (Multiplicar una fila por una constante no nula).\\
3. \textbf{Sustitución:} $F_i \rightarrow F_i + kF_j$ (Sumar a una fila un múltiplo de otra).
\end{tcolorbox}

\vspace{0.5cm}
\textbf{Validez y Aplicación:} Este es el método más universal. A diferencia de otros enfoques, Gauss-Jordan no exige que la matriz sea cuadrada (puede haber más variables que ecuaciones o viceversa) ni que el determinante sea distinto de cero. Es el único método capaz de identificar claramente si un sistema tiene infinitas soluciones o si es incompatible.
\newpage
\section*{Resolución Paso a Paso}
""",

    "cramer": r"""
\section*{Fundamentos: Regla de Cramer}
Este método clásico utiliza determinantes para resolver sistemas de ecuaciones lineales de forma explícita y directa, aislando el cálculo de cada variable.

\begin{tcolorbox}[colback=green!5,colframe=green!50!black,title=Teorema de Cramer]
Si un sistema de $n \times n$ tiene una matriz de coeficientes $A$ con $\det(A) \neq 0$, la solución única está dada por:
\[ x_i = \frac{\det(A_i)}{\det(A)} \]
donde $A_i$ es la matriz que resulta de reemplazar la $i$-ésima columna de $A$ por el vector de términos independientes $B$.
\end{tcolorbox}

\vspace{0.5cm}
\textbf{Validez y Aplicación:} La Regla de Cramer tiene dos requisitos estrictos: el sistema debe ser cuadrado (mismo número de ecuaciones que de incógnitas) y el determinante de la matriz principal debe ser estrictamente distinto de cero ($\det(A) \neq 0$). Si $\det(A) = 0$, el método colapsa por división por cero, indicando que se debe usar Gauss para determinar si hay infinitas soluciones o ninguna.
\newpage
\section*{Resolución Paso a Paso}
""",

    "inversa_gauss": r"""
\section*{Fundamentos: Inversión por Operaciones Elementales}
Todo sistema cuadrado puede representarse como $AX = B$. Si la matriz $A$ es invertible, la solución directa es $X = A^{-1}B$. Este método halla $A^{-1}$ usando el algoritmo de Gauss.

\begin{tcolorbox}[colback=purple!5,colframe=purple!50!black,title=Algoritmo de Inversión por Matriz Aumentada]
Construimos una matriz super-aumentada colocando la matriz identidad $I$ a la derecha de $A$. Aplicamos operaciones elementales de fila hasta transformar el lado izquierdo en la identidad:
\[ [A | I] \quad \xrightarrow{\text{Operaciones Elementales}} \quad [I | A^{-1}] \]
\end{tcolorbox}

\vspace{0.5cm}
\textbf{Validez y Aplicación:} Exige que el sistema sea cuadrado y que $\det(A) \neq 0$. Es computacionalmente más eficiente que la matriz adjunta para dimensiones grandes. Si durante el escalonamiento una fila del lado izquierdo se vuelve completamente cero, se concluye matemáticamente que la matriz es singular (no invertible).
\newpage
\section*{Resolución Paso a Paso}
""",

    "inversa_adjunta": r"""
\section*{Fundamentos: Inversión por Matriz Adjunta}
Este enfoque algebraico permite encontrar la inversa de una matriz $A$ utilizando sus determinantes menores, sin necesidad de realizar operaciones elementales entre filas.

\begin{tcolorbox}[colback=orange!5,colframe=orange!60!black,title=Fórmulas Clave]
\textbf{1. Cofactor:} $C_{ij} = (-1)^{i+j} \det(M_{ij})$ \\
\textbf{2. Matriz Adjunta:} $\text{Adj}(A) = C^T$ (Transpuesta de la matriz de cofactores) \\
\textbf{3. Inversa:} $A^{-1} = \frac{1}{\det(A)} \text{Adj}(A)$
\end{tcolorbox}

\vspace{0.5cm}
\textbf{Validez y Aplicación:} Al igual que la regla de Cramer, requiere un sistema cuadrado con $\det(A) \neq 0$. Aunque computacionalmente es pesado para matrices grandes (por la cantidad de determinantes a calcular), ofrece una fórmula analítica directa e infalible, ideal para demostraciones y sistemas de orden $2 \times 2$ o $3 \times 3$.
\newpage
\section*{Resolución Paso a Paso}
"""
}

# Funciones auxiliares

def latex_matriz_aumentada(M, cols_izq=None):
    """Convierte una matriz SymPy en LaTeX con una línea vertical divisoria."""
    filas, cols = M.shape
    if cols_izq is None: 
        cols_izq = cols - 1 # Por defecto, la última columna es el lado derecho
        
    formato = "c" * cols_izq + "|" + "c" * (cols - cols_izq) if cols_izq < cols else "c" * cols
    res = r"\left[\begin{array}{" + formato + "}\n"
    for i in range(filas):
        res += " & ".join([sp.latex(M[i, j]) for j in range(cols)]) + r" \\" + "\n"
    res += r"\end{array}\right]"
    return res

def latex_determinante(M):
    """Dibuja una matriz con barras verticales de determinante |A|."""
    filas, cols = M.shape
    res = r"\begin{vmatrix}" + "\n"
    for i in range(filas):
        res += " & ".join([sp.latex(M[i, j]) for j in range(cols)]) + r" \\" + "\n"
    res += r"\end{vmatrix}"
    return res

# Funciones principales para generar LATEX

def calcular_latex_gauss(matriz_entrada):
    M = sp.Matrix(matriz_entrada).applyfunc(sp.Rational)
    filas, cols = M.shape
    
    pasos = ["Iniciamos con la matriz aumentada del sistema:\n", f"\\[ {latex_matriz_aumentada(M)} \\]\n"]
    
    lead = 0
    for r in range(filas):
        if lead >= cols - 1: break
        
        # 1. Buscar pivote y hacer intercambio si es necesario
        i = r
        while M[i, lead] == 0:
            i += 1
            if i == filas:
                i, lead = r, lead + 1
                if lead == cols - 1: break
        if lead >= cols - 1: break
        
        if i != r:
            M.row_swap(i, r)
            pasos.append(rf"Intercambiamos la fila {r+1} con la fila {i+1} ($F_{r+1} \leftrightarrow F_{i+1}$):")
            pasos.append(rf"\[ {latex_matriz_aumentada(M)} \]")
            
        # 2. Hacer el pivote igual a 1
        pivote = M[r, lead]
        if pivote != 1 and pivote != 0:
            M[r, :] = M[r, :] / pivote
            pasos.append(rf"Escalamos la fila {r+1} multiplicando por el inverso del pivote ($F_{r+1} \rightarrow \frac{{1}}{{{sp.latex(pivote)}}} F_{r+1}$):")
            pasos.append(rf"\[ {latex_matriz_aumentada(M)} \]")
            
        # 3. Eliminar los elementos de la columna en las demás filas
        for k in range(filas):
            if k != r:
                factor = M[k, lead]
                if factor != 0:
                    M[k, :] = M[k, :] - factor * M[r, :]
                    signo = "-" if factor > 0 else "+"
                    factor_abs = sp.Abs(factor)
                    termino = f"F_{r+1}" if factor_abs == 1 else f"{sp.latex(factor_abs)}F_{r+1}"
                    pasos.append(rf"Eliminamos el elemento en $F_{k+1}$ ($F_{k+1} \rightarrow F_{k+1} {signo} {termino}$):")
                    pasos.append(rf"\[ {latex_matriz_aumentada(M)} \]")
        lead += 1
        
    pasos_latex = "\n\n".join(pasos)
    solucion_texto = f"La matriz escalonada reducida final obtenida es: {str(M.tolist())}"
    return pasos_latex, solucion_texto


def calcular_latex_cramer(matriz_entrada):
    A = sp.Matrix([fila[:-1] for fila in matriz_entrada]).applyfunc(sp.Rational)
    B = sp.Matrix([fila[-1] for fila in matriz_entrada]).applyfunc(sp.Rational)
    n = A.shape[0]
    
    det_A = A.det()
    pasos = [
        r"\textbf{Paso 1: Determinante del Sistema (\(\det(A)\))}",
        "Calculamos el determinante de la matriz de coeficientes. Evaluamos la expansión por cofactores de la primera fila:",
        rf"\[ \det(A) = {latex_determinante(A)} \]"
    ]
    
    # Mostrar la expansión paso a paso para determinantes 3x3 o mayores
    if n >= 3:
        expansion = r"\[ \det(A) = "
        for j in range(n):
            M_sub = A.copy()
            M_sub.row_del(0)
            M_sub.col_del(j)
            signo = "+" if j % 2 == 0 else "-"
            val = A[0, j]
            if val != 0:
                expansion += rf" {signo} \left({sp.latex(val)}\right) {latex_determinante(M_sub)} "
        expansion += rf" = {sp.latex(det_A)} \]"
        pasos.append(expansion)
    
    if det_A == 0:
        pasos.append(r"\vspace{0.5cm}\textbf{\color{red} ¡Atención!} El determinante es 0. La Regla de Cramer colapsa. El sistema no tiene solución única.")
        return "\n\n".join(pasos), "El determinante es cero. El sistema es Incompatible o Compatible Indeterminado."
        
    pasos.append(r"\vspace{0.5cm}\textbf{Paso 2: Determinantes de las Variables}")
    variables = ['x', 'y', 'z', 'w'][:n]
    resultados_finales = []
    
    for i in range(n):
        A_mod = A.copy()
        A_mod.col_op(i, lambda v, j: B[j])
        det_mod = A_mod.det()
        valor_var = det_mod / det_A
        resultados_finales.append(f"{variables[i]} = {valor_var}")
        
        pasos.append(rf"\noindent Sustituimos la columna {i+1} por el vector de términos independientes para hallar $\det(A_{variables[i]})$:")
        pasos.append(rf"\[ \det(A_{variables[i]}) = {latex_determinante(A_mod)} = {sp.latex(det_mod)} \]")
        pasos.append(rf"\[ {variables[i]} = \frac{{\det(A_{variables[i]})}}{{\det(A)}} = \frac{{{sp.latex(det_mod)}}}{{{sp.latex(det_A)}}} = {sp.latex(valor_var)} \]")
        pasos.append(r"\vspace{0.3cm}\hrule\vspace{0.3cm}")

    solucion_texto = f"El sistema tiene solución única: {', '.join(resultados_finales)}"
    return "\n\n".join(pasos), solucion_texto


def calcular_latex_inversa_gauss(matriz_entrada):
    A = sp.Matrix([fila[:-1] for fila in matriz_entrada]).applyfunc(sp.Rational)
    B = sp.Matrix([fila[-1] for fila in matriz_entrada]).applyfunc(sp.Rational)
    n = A.shape[0]
    
    if A.det() == 0:
        return r"\textbf{Error:} El determinante de la matriz principal es 0. La matriz no es invertible.", "Determinante cero, matriz singular."
        
    # Construir [A | I]
    I = sp.eye(n)
    M = A.row_join(I)
    
    pasos = [
        r"\textbf{Paso 1: Construcción de la matriz aumentada $[A | I]$}",
        rf"\[ {latex_matriz_aumentada(M, cols_izq=n)} \]",
        r"\vspace{0.5cm}\textbf{Paso 2: Reducción por Operaciones Elementales}"
    ]
    
    # Algoritmo de Gauss-Jordan sobre [A | I]
    for r in range(n):
        if M[r, r] == 0:
            for i in range(r + 1, n):
                if M[i, r] != 0:
                    M.row_swap(i, r)
                    pasos.append(rf"Intercambio: $F_{r+1} \leftrightarrow F_{i+1}$")
                    pasos.append(rf"\[ {latex_matriz_aumentada(M, cols_izq=n)} \]")
                    break
                    
        pivote = M[r, r]
        if pivote != 1:
            M[r, :] = M[r, :] / pivote
            pasos.append(rf"Pivote a 1: $F_{r+1} \rightarrow \frac{{1}}{{{sp.latex(pivote)}}} F_{r+1}$")
            pasos.append(rf"\[ {latex_matriz_aumentada(M, cols_izq=n)} \]")
            
        for k in range(n):
            if k != r and M[k, r] != 0:
                factor = M[k, r]
                M[k, :] = M[k, :] - factor * M[r, :]
                signo = "-" if factor > 0 else "+"
                factor_abs = sp.Abs(factor)
                termino = f"F_{r+1}" if factor_abs == 1 else f"{sp.latex(factor_abs)}F_{r+1}"
                pasos.append(rf"Eliminación: $F_{k+1} \rightarrow F_{k+1} {signo} {termino}$")
                pasos.append(rf"\[ {latex_matriz_aumentada(M, cols_izq=n)} \]")

    A_inv = M[:, n:]
    X = A_inv * B
    
    pasos.append(r"\vspace{0.5cm}\textbf{Paso 3: Extracción de la Inversa y Solución}")
    pasos.append(rf"La matriz ha sido transformada a $[I | A^{{-1}}]$. Extraemos la inversa:")
    pasos.append(rf"\[ A^{{-1}} = {latex_matriz_aumentada(A_inv, cols_izq=n)} \]")
    pasos.append(r"Finalmente, multiplicamos por el vector de términos independientes ($X = A^{-1}B$):")
    pasos.append(rf"\[ X = {latex_matriz_aumentada(A_inv, cols_izq=n)} {latex_matriz_aumentada(B, cols_izq=1)} = {latex_matriz_aumentada(X, cols_izq=1)} \]")

    return "\n\n".join(pasos), f"Solución calculada mediante A_inv * B = {str(X.tolist())}"


def calcular_latex_inversa_adjunta(matriz_entrada):
    A = sp.Matrix([fila[:-1] for fila in matriz_entrada]).applyfunc(sp.Rational)
    B = sp.Matrix([fila[-1] for fila in matriz_entrada]).applyfunc(sp.Rational)
    n = A.shape[0]
    
    det_A = A.det()
    pasos = [
        r"\textbf{Paso 1: Determinante del Sistema}",
        rf"\[ \det(A) = {sp.latex(det_A)} \]"
    ]
    if det_A == 0:
        pasos.append(r"El determinante es 0. La matriz no tiene inversa.")
        return "\n\n".join(pasos), "Determinante cero."

    pasos.append(r"\vspace{0.5cm}\textbf{Paso 2: Matriz de Cofactores ($C$)}")
    pasos.append(r"Calculamos explícitamente cada cofactor usando la fórmula $C_{ij} = (-1)^{i+j} \det(M_{ij})$:")
    
    C = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            M_sub = A.copy()
            M_sub.row_del(i)
            M_sub.col_del(j)
            det_sub = M_sub.det()
            cofactor = ((-1)**(i+j)) * det_sub
            C[i, j] = cofactor
            
            signo_base = "-" if (i+j)%2 != 0 else "+"
            # Muestra la submatriz y el cálculo del signo
            pasos.append(rf"\[ C_{{{i+1}{j+1}}} = {signo_base} {latex_determinante(M_sub)} = {signo_base}({sp.latex(det_sub)}) = {sp.latex(cofactor)} \]")

    adj_A = C.T
    A_inv = adj_A / det_A
    X = A_inv * B

    pasos.append(r"\vspace{0.5cm}\textbf{Paso 3: Matriz Adjunta ($\text{Adj}(A)$)}")
    pasos.append(r"Agrupamos los cofactores y transponemos la matriz ($C^T$):")
    pasos.append(rf"\[ C = {latex_matriz_aumentada(C, cols_izq=n)} \quad \Rightarrow \quad \text{{Adj}}(A) = {latex_matriz_aumentada(adj_A, cols_izq=n)} \]")
    
    pasos.append(r"\vspace{0.5cm}\textbf{Paso 4: Matriz Inversa y Solución Final}")
    pasos.append(rf"\[ A^{{-1}} = \frac{{1}}{{\det(A)}} \text{{Adj}}(A) = \frac{{1}}{{{sp.latex(det_A)}}} {latex_matriz_aumentada(adj_A, cols_izq=n)} = {latex_matriz_aumentada(A_inv, cols_izq=n)} \]")
    pasos.append(r"Multiplicamos $X = A^{-1}B$:")
    pasos.append(rf"\[ X = {latex_matriz_aumentada(A_inv, cols_izq=n)} {latex_matriz_aumentada(B, cols_izq=1)} = {latex_matriz_aumentada(X, cols_izq=1)} \]")

    return "\n\n".join(pasos), f"Solución calculada mediante Adjunta X = {str(X.tolist())}"

def generar_pdf_con_gemini(matriz, metodo, api_key):
    try:
        # 1. Ejecutar el motor matemático puro (cero IA involucrada en los números)
        if metodo == "gauss":
            pasos_latex, solucion_texto = calcular_latex_gauss(matriz)
        elif metodo == "cramer":
            pasos_latex, solucion_texto = calcular_latex_cramer(matriz)
        elif metodo == "inversa_gauss":
            pasos_latex, solucion_texto = calcular_latex_inversa_gauss(matriz)
        elif metodo == "inversa_adjunta":
            pasos_latex, solucion_texto = calcular_latex_inversa_adjunta(matriz)
        else:
            pasos_latex, solucion_texto = calcular_latex_gauss(matriz)

        # 2. Llamada mínima a la IA: Solo para la interpretación final
        client = genai.Client(api_key=api_key)
        prompt_ia = f"""
        Actúa como un profesor de álgebra lineal. 
        Un estudiante acaba de resolver un sistema de ecuaciones y obtuvo el siguiente resultado numérico: {solucion_texto}.
        Redacta una interpretación final de máximo 5 líneas. Indica claramente si el sistema es Compatible Determinado, Indeterminado o Incompatible, qué significa esto geométricamente (corte de planos/rectas) y una palabra de aliento. 
        Devuelve SOLO el código LaTeX para este párrafo de texto (sin entornos begin/end de documento).
        """
        respuesta_ia = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt_ia
        )
        interpretacion_latex = respuesta_ia.text.strip()

        # 3. Ensamblar el documento LaTeX maestro
        documento_completo = r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{amsmath, amssymb}
\usepackage[margin=2.5cm]{geometry}
\usepackage[most]{tcolorbox} % Paquete esencial para las plantillas

\begin{document}
""" + PLANTILLAS_TEORICAS.get(metodo, PLANTILLAS_TEORICAS["gauss"]) + r"""

% --- INICIO DE CÁLCULOS MATEMÁTICOS ---
""" + pasos_latex + r"""

\newpage
\section*{Conclusión e Interpretación}
\begin{tcolorbox}[colback=gray!5,colframe=gray!60!black,title=Análisis del Resultado]
""" + interpretacion_latex + r"""
\end{tcolorbox}

\end{document}
"""

        url_compilador = "https://texlive.net/cgi-bin/latexcgi"
        
        # Texlive.net requiere que estructuremos el envío como un formulario web
        datos = {
            'filename[]': 'document.tex',
            'return': 'pdf'
        }
        archivos = {
            'filecontents[]': ('document.tex', documento_completo)
        }
        
        respuesta_pdf = requests.post(url_compilador, data=datos, files=archivos)
        
        # Comprobación de seguridad: Un PDF legítimo siempre inicia con los bytes '%PDF'
        if respuesta_pdf.status_code == 200 and respuesta_pdf.content.startswith(b'%PDF'):
            return respuesta_pdf.content, None 
        else:
            # Si LaTeX encuentra un error matemático/sintáctico, texlive devuelve el log completo
            log_error = respuesta_pdf.text
            
            if "!" in log_error:
                # Extraemos exactamente la línea donde LaTeX detectó el fallo
                mensaje_util = "!" + log_error.split("!")[-1][:300]
            else:
                mensaje_util = log_error[:300]
                
            return None, f"Fallo en el formato LaTeX: {mensaje_util}"
            
    except Exception as e:
        return None, str(e)
