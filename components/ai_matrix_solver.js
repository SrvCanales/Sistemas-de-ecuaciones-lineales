/**
 * ai_matrix_solver.js
 * * Este archivo contiene la lógica para:
 * 1. Leer una matriz M.
 * 2. Enviar la matriz y un prompt especificado a una API de Inteligencia Artificial.
 * 3. Procesar la respuesta y generar un PDF usando jsPDF.
 * 4. Mostrar el PDF en la página y permitir su descarga.
 */

class AIMatrixSolver {
    constructor(matrix, apiKey, provider = 'gemini') {
        this.matrix = matrix;
        this.apiKey = apiKey;
        this.provider = provider;
        this.pdfUrl = null;
    }

    async solveMatrix(userPrompt) {
        // Convertimos la matriz a texto estructurado para la IA
        const matrixString = JSON.stringify(this.matrix);
        const fullPrompt = `${userPrompt}\n\nMatriz M:\n${matrixString}`;
        
        let aiResponse = "";
        
        try {
            if (!this.apiKey || this.apiKey === 'TU_CLAVE_API_AQUI') {
                return "AVISO: No se ha configurado una API KEY real. Para que funcione la inteligencia artificial, debes insertar tu clave API en el código.\n\nSimulación de respuesta para la matriz proporcionada:\nEl cálculo se ha realizado con éxito. (Reemplaza la API KEY para ver resultados reales generados por IA).";
            }

            if (this.provider === 'gemini') {
                aiResponse = await this._callGemini(fullPrompt);
            } else if (this.provider === 'openai') {
                aiResponse = await this._callOpenAI(fullPrompt);
            }
            return aiResponse;
        } catch (error) {
            console.error("Error al consultar la IA:", error);
            return "Ocurrió un error al procesar con IA: " + error.message;
        }
    }

    async _callGemini(prompt) {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${this.apiKey}`;
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
        });
        const data = await response.json();
        if (data.error) throw new Error(data.error.message);
        return data.candidates[0].content.parts[0].text;
    }

    async _callOpenAI(prompt) {
        const url = 'https://api.openai.com/v1/chat/completions';
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify({
                model: "gpt-3.5-turbo",
                messages: [{ role: "user", content: prompt }]
            })
        });
        const data = await response.json();
        if (data.error) throw new Error(data.error.message);
        return data.choices[0].message.content;
    }

    generatePDF(aiResult, promptUsed) {
        // Obtenemos jsPDF globalmente
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        doc.setFontSize(16);
        doc.text("Resolución de Matriz mediante Inteligencia Artificial", 10, 20);
        
        doc.setFontSize(11);
        doc.setTextColor(100);
        doc.text(`Prompt utilizado: ${promptUsed}`, 10, 30, { maxWidth: 190 });
        
        doc.setTextColor(0);
        doc.setFontSize(12);
        doc.text("Matriz Original:", 10, 45);
        
        let yOffset = 52;
        doc.setFont("courier", "normal");
        this.matrix.forEach(row => {
            doc.text(JSON.stringify(row), 10, yOffset);
            yOffset += 6;
        });

        yOffset += 10;
        doc.setFont("helvetica", "bold");
        doc.text("Resolución / Análisis de la IA:", 10, yOffset);
        
        yOffset += 8;
        doc.setFont("helvetica", "normal");
        doc.setFontSize(11);
        
        // Manejo automático de múltiples páginas
        const splitResponse = doc.splitTextToSize(aiResult, 190);
        for (let i = 0; i < splitResponse.length; i++) {
            if (yOffset > 280) { // Nueva página si nos acercamos al final
                doc.addPage();
                yOffset = 20;
            }
            doc.text(splitResponse[i], 10, yOffset);
            yOffset += 6.5;
        }
        
        // Generar Blob
        const pdfBlob = doc.output('blob');
        this.pdfUrl = URL.createObjectURL(pdfBlob);
        
        return this.pdfUrl;
    }

    renderPDFAndDownloadUI(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = "";
        
        const downloadBtn = document.createElement("a");
        downloadBtn.href = this.pdfUrl;
        downloadBtn.download = "Resolucion_IA_Matriz.pdf";
        downloadBtn.textContent = "📥 Descargar PDF";
        downloadBtn.style = "display: block; width: max-content; margin-bottom: 15px; padding: 12px 24px; background-color: #2563eb; color: white; text-decoration: none; border-radius: 6px; font-family: sans-serif; font-weight: bold;";
        
        const iframe = document.createElement("iframe");
        iframe.src = this.pdfUrl;
        iframe.width = "100%";
        iframe.height = "700px";
        iframe.style.border = "1px solid #d1d5db";
        iframe.style.borderRadius = "6px";
        
        container.appendChild(downloadBtn);
        container.appendChild(iframe);
    }
}
