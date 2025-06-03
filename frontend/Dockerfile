FROM oven/bun:1-slim

WORKDIR /app

# Copy dependency files
COPY package.json bun.lockb ./

# Install dependencies
RUN bun install --frozen-lockfile

# Copy configuration files
COPY next.config.js tsconfig.json postcss.config.js components.json ./

# Copy source code
COPY app/ ./app/
COPY components/ ./components/
COPY lib/ ./lib/

# Copy any other necessary files
COPY public/ ./public/ 2>/dev/null || true

# Build the application
RUN bun run build

# Expose port
EXPOSE 3000

# Start command
CMD ["bun", "start"] 