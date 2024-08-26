FROM node:alpine

WORKDIR /app

COPY front/package*.json ./

RUN npm install

COPY front/dist ./dist

EXPOSE 3000
