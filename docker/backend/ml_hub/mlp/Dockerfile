FROM python:3.6.9
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
CMD ["python", "mlp.py"]