From node:slim

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install prettier -g

RUN npm install

COPY . .

RUN npm run build 

EXPOSE 3011

CMD ["node", "build/server.js"]