# syntax=docker/dockerfile:1

FROM golang:1.24-alpine as builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o backend .

FROM debian:bullseye-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/backend .
COPY --from=builder /app/templates ./templates
COPY .env .

# Опционально: добавляем dummy файл secret.txt для /secret ручки (либо вшиваем свой флаг)
RUN echo "FECTF{v3ry_1mp0r74n7_1nf0rm4710n_f0r_r3p0r7_63n3r470r}" > secret.txt

EXPOSE 8080

CMD ["./backend"]
