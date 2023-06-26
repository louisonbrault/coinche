# Étape 1: Build de l'application Angular
FROM node:16-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build --configuration=production

# Étape 2: Création de l'image Docker
FROM nginx:alpine

# Copie des fichiers de build de l'application
COPY --from=builder /app/dist/coinche/ /usr/share/nginx/html

# Changement de la conf nginx
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

CMD envsubst < /usr/share/nginx/html/assets/env.template.js > /usr/share/nginx/html/assets/env.js && nginx -g "daemon off;"
