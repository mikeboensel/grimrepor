FROM ubuntu:22.04 AS dev

EXPOSE 3000

WORKDIR /app

RUN apt-get -y update &&\
 apt-get -y upgrade

COPY website /app

ENV PATH=./node_modules/.bin:$PATH

RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -

# Remove conflicting package
RUN apt-get remove -y libnode-dev

RUN apt-get install -y nodejs

RUN npm install

RUN npm run build

# CMD ["sleep", "infinity"]
CMD ["npm", "run", "start"]
    

FROM node:lts AS prod
EXPOSE 3000

WORKDIR /app

COPY website /app

RUN npm install

ENV PATH=./node_modules/.bin:$PATH

RUN npm run build

# CMD ["sleep", "infinity"]
CMD ["npm", "run", "start"]