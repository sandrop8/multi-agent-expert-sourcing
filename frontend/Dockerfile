FROM oven/bun:1-slim

WORKDIR /app

# Copy package files
COPY package.json bun.lockb ./

# Install dependencies
RUN bun install --frozen-lockfile

# Copy all source files
COPY . .

# Debug: Verify directory structure and lib/utils.ts
RUN echo "=== App directory structure ===" && ls -la /app
RUN echo "=== Lib directory ===" && ls -la /app/lib
RUN echo "=== Utils file ===" && cat /app/lib/utils.ts

# Build the application
RUN bun run build

# Expose port
EXPOSE 3000

# Start command  
CMD ["bun", "start"] 