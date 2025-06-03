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

# Set environment variables for Next.js deployment
ENV NODE_ENV=production
ENV HOSTNAME="0.0.0.0"

# Expose port (Railway will override this)
EXPOSE 3000

# Start command - Next.js will use HOSTNAME and PORT env vars
CMD ["sh", "-c", "PORT=${PORT:-3000} HOSTNAME=0.0.0.0 bun start"] 