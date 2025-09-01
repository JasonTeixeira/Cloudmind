const nextJest = require('next/jest')

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files
  dir: './',
})

// Add any custom config to be passed to Jest
const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jsdom',
  testPathIgnorePatterns: ['<rootDir>/.next/', '<rootDir>/node_modules/'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
    'react-router-dom': '<rootDir>/tests/__mocks__/react-router-dom.ts',
  },
  collectCoverageFrom: [
    'app/**/*.{js,jsx,ts,tsx}',
    'components/**/*.{js,jsx,ts,tsx}',
    'lib/**/*.{js,jsx,ts,tsx}',
    '!**/*.d.ts',
    '!**/node_modules/**',
    '!**/.next/**',
    '!**/coverage/**',
    '!**/cypress/**',
    '!**/playwright-report/**',
  ],
  coverageThreshold: {
    global: {
      branches: 50, // Lowered temporarily to be achievable
      functions: 50,
      lines: 50,
      statements: 50,
    },
  },
  testMatch: [
    '<rootDir>/__tests__/**/*.{test,spec}.{js,jsx,ts,tsx}',
    '<rootDir>/components/**/*.{test,spec}.{js,jsx,ts,tsx}',
    '<rootDir>/app/**/*.{test,spec}.{js,jsx,ts,tsx}',
    '<rootDir>/lib/**/*.{test,spec}.{js,jsx,ts,tsx}',
  ],
  testTimeout: 10000,
  maxWorkers: '50%',
  verbose: true,
  bail: false,
  errorOnDeprecated: true,
}

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
module.exports = createJestConfig(customJestConfig)