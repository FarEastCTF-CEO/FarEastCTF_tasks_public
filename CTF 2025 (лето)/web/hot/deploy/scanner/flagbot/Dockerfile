FROM alpine:latest


RUN apk add --no-cache curl

WORKDIR /app

COPY entrypoint.sh index.html ./
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]