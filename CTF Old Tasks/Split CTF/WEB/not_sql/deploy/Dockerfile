FROM node:20-alpine

WORKDIR /app
COPY app/package.json /app/package.json
RUN npm install --omit=dev
COPY app/ /app/

ENV PORT=3000
EXPOSE 3000

CMD ["node", "index.js"]
