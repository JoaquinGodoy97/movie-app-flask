FROM python:3.12.4

WORKDIR /api-movies

COPY requirements.txt .
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]