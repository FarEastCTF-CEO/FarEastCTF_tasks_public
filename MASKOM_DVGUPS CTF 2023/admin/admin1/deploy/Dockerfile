FROM golang:1.21-alpine AS build
WORKDIR /app
COPY ../src/ ./
RUN go build -o /admin1 admin1.go

FROM alpine:3.19
RUN apk add --no-cache socat
WORKDIR /srv
COPY --from=build /admin1 ./admin1
COPY config.json ./config.json
EXPOSE 8080
CMD ["sh","./start.sh"]
