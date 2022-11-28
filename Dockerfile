FROM node:18-alpine

WORKDIR /code/

COPY package.json .
RUN yarn install

COPY . .

ENTRYPOINT [ "yarn" ]
CMD [ "start:dev" ]