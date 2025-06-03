FROM oven/bun:1-slim

WORKDIR /app

# Copy package files
COPY package.json bun.lockb ./

# Install dependencies
RUN bun install --frozen-lockfile

# Copy all source files
COPY . .

# Build the application
RUN bun run build

# Expose port
EXPOSE 3000

# Start command  
CMD ["bun", "start"] 