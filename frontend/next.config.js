/** @type {import('next').NextConfig} */
const nextConfig = {
  // Output configuration for Docker
  output: 'standalone',

  // Image optimization
  images: {
    domains: [
      'localhost',
      'cloudmind.local',
      'avatars.githubusercontent.com',
      'lh3.googleusercontent.com',
    ],
    formats: ['image/webp', 'image/avif'],
  },

  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME || 'CloudMind',
    NEXT_PUBLIC_APP_VERSION: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
  },

  // Webpack configuration
  webpack: (config, { isServer }) => {
    // Handle Three.js
    config.module.rules.push({
      test: /\.(glsl|vs|fs|vert|frag)$/,
      exclude: /node_modules/,
      use: ['raw-loader', 'glslify-loader'],
    });

    // Handle WASM files
    config.experiments = {
      ...config.experiments,
      asyncWebAssembly: true,
    };

    // Handle Node.js modules in browser
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
        crypto: false,
      };
    }

    return config;
  },

  // PWA configuration
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ];
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/docs',
        destination: '/api/docs',
        permanent: true,
      },
    ];
  },

  // Rewrites for API proxy
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/:path*`,
      },
    ];
  },

  // Bundle analyzer
  ...(process.env.ANALYZE === 'true' && {
    webpack: (config) => {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'static',
          openAnalyzer: false,
        })
      );
      return config;
    },
  }),

  // TypeScript configuration
  typescript: {
    // !! WARN !!
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    // !! WARN !!
    ignoreBuildErrors: false,
  },

  // ESLint configuration
  eslint: {
    // Warning: This allows production builds to successfully complete even if
    // your project has ESLint errors.
    ignoreDuringBuilds: false,
  },

  // Compiler configuration
  compiler: {
    // Remove console logs in production
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // Trailing slash configuration
  trailingSlash: false,

  // Base path configuration
  basePath: '',

  // Asset prefix configuration
  assetPrefix: '',

  // Powered by header
  poweredByHeader: false,

  // React strict mode
  reactStrictMode: true,

  // Swc minification
  swcMinify: true,

  // Experimental features
  experimental: {
    // Enable typed routes
    typedRoutes: true,
    
    // Enable turbo
    turbo: {
      rules: {
        '*.svg': {
          loaders: ['@svgr/webpack'],
          as: '*.js',
        },
      },
    },
  },

  // Transpile packages (only used ones)
  transpilePackages: [
    '@radix-ui/react-dialog',
    '@radix-ui/react-dropdown-menu',
    '@radix-ui/react-label',
    '@radix-ui/react-popover',
    '@radix-ui/react-progress',
    '@radix-ui/react-select',
    '@radix-ui/react-tabs',
    '@radix-ui/react-toast',
    '@radix-ui/react-tooltip',
    'recharts',
  ],
};

module.exports = nextConfig; 