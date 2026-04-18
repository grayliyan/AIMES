FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy application
COPY . .

# Expose port
EXPOSE 5173

CMD ["npm", "run", "dev"]