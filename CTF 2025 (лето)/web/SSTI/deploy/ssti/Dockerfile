# build stage
FROM python:3.9-bullseye as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt
COPY . .

# final stage
FROM gcr.io/distroless/python3-debian12
WORKDIR /app
ENV PYTHONPATH=/install/lib/python3.9/site-packages
COPY --from=builder /app /app
COPY --from=builder /install /install
CMD ["app.py"]