FROM node:slim
EXPOSE 8080
WORKDIR /app
COPY frontend/package.json /app/
RUN npm install
COPY frontend/server.js /app/
CMD node /app/server.js