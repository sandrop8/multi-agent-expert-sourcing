const path = require('path')

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable TypeScript strict mode
  typescript: {
    ignoreBuildErrors: false,
  },
  // Configure webpack for path aliases - simplified for Docker compatibility
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname),
    }

    // Enable debug logging for Docker builds
    console.log('Docker build - Project root:', path.resolve(__dirname))
    console.log('Docker build - @ alias:', config.resolve.alias['@'])

    return config
  },
}

module.exports = nextConfig 