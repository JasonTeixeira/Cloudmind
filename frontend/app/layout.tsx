import type { Metadata } from 'next'
import { Inter, JetBrains_Mono } from 'next/font/google'
import './globals.css'

import { GlobalCommandPalette } from '@/components/ui/GlobalCommandPalette'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const jetbrainsMono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-jetbrains-mono' })

export const metadata: Metadata = {
  title: 'CloudMind - World-Class Cloud Management Platform',
  description: 'Enterprise-grade cloud management with AI-powered insights, cost optimization, and security monitoring',
  keywords: 'cloud management, cost optimization, security monitoring, AI insights, infrastructure',
  authors: [{ name: 'CloudMind Team' }],
  creator: 'CloudMind',
  publisher: 'CloudMind',
  robots: 'index, follow',
  manifest: '/manifest.json',
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
  openGraph: {
    title: 'CloudMind - World-Class Cloud Management Platform',
    description: 'Enterprise-grade cloud management with AI-powered insights, cost optimization, and security monitoring',
    type: 'website',
    locale: 'en_US',
    siteName: 'CloudMind',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'CloudMind - World-Class Cloud Management Platform',
    description: 'Enterprise-grade cloud management with AI-powered insights, cost optimization, and security monitoring',
  },
}

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: '#00f5ff',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <head>
        {/* Security Headers */}
        <meta httpEquiv="X-Content-Type-Options" content="nosniff" />
        <meta httpEquiv="X-Frame-Options" content="DENY" />
        <meta httpEquiv="X-XSS-Protection" content="1; mode=block" />
        <meta httpEquiv="Referrer-Policy" content="strict-origin-when-cross-origin" />
        <meta httpEquiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=()" />
        
        {/* CSRF Protection */}
        <meta name="csrf-token" content="" />
        
        {/* Content Security Policy */}
        <meta httpEquiv="Content-Security-Policy" content="
          default-src 'self';
          script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net;
          style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
          font-src 'self' https://fonts.gstatic.com;
          img-src 'self' data: https:;
          connect-src 'self' http://localhost:8000 https://localhost:8000 https://api.cloudmind.com;
          frame-ancestors 'none';
          base-uri 'self';
          form-action 'self';
        " />
      </head>
      <body className={`${inter.variable} ${jetbrainsMono.variable} h-full bg-cyber-black text-cyber-cyan font-sans antialiased`}>
        {children}
        <GlobalCommandPalette />
        
        {/* Service Worker Registration */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                window.addEventListener('load', function() {
                  navigator.serviceWorker.register('/sw.js')
                    .then(function(registration) {
                      console.log('SW registered: ', registration);
                    })
                    .catch(function(registrationError) {
                      console.log('SW registration failed: ', registrationError);
                    });
                });
              }
            `,
          }}
        />
      </body>
    </html>
  )
} 