/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  },
  swcMinify: true,
  eslint: {
    ignoreDuringBuilds: true,
  },
  async redirects() {
    return [
      {
        source: '/workspace/:path*',
        destination: '/console/:path*',
        permanent: true,
      },
      {
        source: '/dashboard',
        destination: '/console',
        permanent: true,
      },
      {
        source: '/workspace',
        destination: '/console/trading',
        permanent: true,
      },
      {
        source: '/workspace/trading',
        destination: '/console/trading',
        permanent: true,
      },
    ];
  },
}

module.exports = nextConfig
