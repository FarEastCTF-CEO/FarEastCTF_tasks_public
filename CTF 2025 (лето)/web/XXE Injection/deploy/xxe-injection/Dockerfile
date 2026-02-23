FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd flag && usermod -s /usr/sbin/nologin flag && usermod -c "/flag" flag

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]