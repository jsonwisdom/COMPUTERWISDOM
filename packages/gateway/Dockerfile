FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY src/ ./src/

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Start the development server
CMD ["npm", "run", "dev", "--", "--port", "3000", "--host", "0.0.0.0"]