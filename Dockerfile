FROM python:3.12.4

WORKDIR /api-movies

COPY requirements.txt .
COPY . /api-movies

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]