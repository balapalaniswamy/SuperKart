FROM python:3.11-slim

WORKDIR /app

# Copying the dependency file first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying the rest of the frontend code
COPY . .

# Streamlit's default port
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
