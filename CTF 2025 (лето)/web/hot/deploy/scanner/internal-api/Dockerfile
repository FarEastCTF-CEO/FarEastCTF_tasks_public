# syntax=docker/dockerfile:1


# Сборка Go-бинарника
FROM golang:1.24-alpine AS builder

WORKDIR /app

# Копируем go.mod/go.sum отдельно для кэширования зависимостей
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o internal-api

# Финальный образ
FROM alpine:latest

WORKDIR /app
COPY --from=builder /app/internal-api .

COPY .env .
CMD ["./internal-api"]
