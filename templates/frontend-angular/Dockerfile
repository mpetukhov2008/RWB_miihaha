# Stage 1: build Angular
FROM node:22-alpine AS build
WORKDIR /src
COPY package.json ./
RUN npm install --legacy-peer-deps
COPY . .
RUN npm run build

# Stage 2: nginx
FROM nginx:1.27-alpine
COPY --from=build /src/dist/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
