FROM node:18-alpine

WORKDIR /app

# Add the following to reduce potential npm issues
ENV NODE_OPTIONS=--max_old_space_size=4096

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8080

CMD ["npm", "run", "dev"]