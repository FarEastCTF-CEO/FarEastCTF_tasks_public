FROM debian:bookworm-slim

RUN apt-get update  && apt-get install -y --no-install-recommends socat ca-certificates  && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf
WORKDIR /home/ctf

COPY ret /home/ctf/chal
COPY flag.txt /home/ctf/flag.txt

RUN chown -R root:root /home/ctf  && chmod 0755 /home/ctf/chal  && chmod 0444 /home/ctf/flag.txt

USER ctf
ENV PORT=12340
EXPOSE 12340

CMD ["sh", "-c", "socat TCP-LISTEN:,reuseaddr,fork EXEC:./chal,stderr"]
