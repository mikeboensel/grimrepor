FROM node:lts
EXPOSE 3000

WORKDIR /app

COPY website /app

RUN npm install

ENV PATH=./node_modules/.bin:$PATH

RUN npm run build

# CMD ["sleep", "infinity"]
CMD ["npm", "run", "start"]