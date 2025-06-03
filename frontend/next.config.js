const path = require('path')

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable TypeScript strict mode
  typescript: {
    ignoreBuildErrors: false,
  },
  // Configure runtime environment variables (available at runtime, not build time)
  publicRuntimeConfig: {
    API_URL: process.env.API_URL || 'http://localhost:8000',
  },
  // Configure webpack for path aliases
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname),
    }

    return config
  },
}

module.exports = nextConfig 