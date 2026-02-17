/** @type {import('next').NextConfig} */
const nextConfig = {
    async redirects() {
      return [
        {
          source: '/',
          has: [
            {
              type: 'host',
              value: 'rivue.ai',
            },
          ],
          destination: 'https://try.rivue.ai',
          permanent: true,
        },
      ]
    },
  }
  
  module.exports = nextConfig
  