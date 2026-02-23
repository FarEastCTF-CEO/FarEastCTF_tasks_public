FROM python:3.11-slim

WORKDIR /app
COPY app/ /app/

RUN pip install --no-cache-dir flask==3.0.3

EXPOSE 80
ENV PORT=80

CMD ["python", "run.py"]
