FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-lang-spanish
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
