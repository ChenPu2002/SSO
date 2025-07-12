FROM node:16-alpine

WORKDIR /app

# 复制 package.json 并安装依赖
COPY package*.json ./
RUN npm install

# 复制项目代码
COPY . .

EXPOSE 8080

CMD ["npm", "run", "serve"]