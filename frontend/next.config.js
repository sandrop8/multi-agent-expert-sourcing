const path = require('path')

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable TypeScript strict mode
  typescript: {
    ignoreBuildErrors: false,
  },
  // Configure webpack for path aliases
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Get the absolute path to the project root
    const projectRoot = path.resolve(__dirname)

    config.resolve.alias = {
      ...config.resolve.alias,
      '@': projectRoot,
      '@/lib': path.join(projectRoot, 'lib'),
      '@/lib/utils': path.join(projectRoot, 'lib', 'utils'),
      '@/components': path.join(projectRoot, 'components'),
      '@/app': path.join(projectRoot, 'app'),
    }

    // Debug: uncomment the line below to see path resolution in build logs
    // console.log('Webpack alias configuration:', config.resolve.alias)

    return config
  },
}

module.exports = nextConfig 