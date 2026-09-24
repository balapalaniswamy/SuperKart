FROM python:3.11-slim

WORKDIR /app

# Copying the dependency file first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying the rest of the backend code (main.py + the serialized model)
COPY . .

# The Flask app listens on this port
EXPOSE 7860

CMD ["python", "main.py"]
