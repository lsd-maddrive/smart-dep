FROM node:12 as nodebuild

COPY ./app /app
WORKDIR /app
RUN npm install
RUN npm run build

RUN ls /app/dist

# Create new image with files from "nodebuild" image
FROM nginx:1.17.9-alpine

COPY --from=nodebuild /app/dist /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/nginx.conf
