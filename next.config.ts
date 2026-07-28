import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  async redirects() {
    return [
      {
        source: '/typhlosion',
        destination: '/typhlosion.html',
        permanent: false,
      },
      {
        source: '/basebloom',
        destination: '/basebloom/index.html',
        permanent: false,
      },
    ];
  },
};

export default nextConfig;
