FROM python:3.11-slim
WORKDIR /app
COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/prod.txt
COPY . .
EXPOSE 8010
CMD ["gunicorn", "--bind", "0.0.0.0:8010", "StockSeeker.wsgi:application"]
