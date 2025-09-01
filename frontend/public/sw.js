// CloudMind Service Worker - Advanced PWA Features
const CACHE_NAME = 'cloudmind-v1.0.0';
const STATIC_CACHE = 'cloudmind-static-v1.0.0';
const DYNAMIC_CACHE = 'cloudmind-dynamic-v1.0.0';
const API_CACHE = 'cloudmind-api-v1.0.0';

// Cache configuration
const STATIC_ASSETS = [
  '/',
  '/manifest.json',
  '/offline.html',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

const API_ENDPOINTS = [
  '/api/v1/health',
  '/api/v1/auth/status',
  '/api/v1/projects',
  '/api/v1/cost',
  '/api/v1/security',
  '/api/v1/ai',
  '/api/v1/infrastructure',
  '/api/v1/monitoring',
  '/api/v1/reports'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('🔄 Service Worker installing...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('📦 Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('✅ Static assets cached successfully');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('❌ Failed to cache static assets:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('🚀 Service Worker activating...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && 
                cacheName !== DYNAMIC_CACHE && 
                cacheName !== API_CACHE) {
              console.log('🗑️ Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('✅ Service Worker activated successfully');
        return self.clients.claim();
      })
  );
});

// Fetch event - handle requests with advanced caching strategies
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Handle different types of requests
  if (request.method === 'GET') {
    if (isStaticAsset(request)) {
      event.respondWith(cacheFirst(request, STATIC_CACHE));
    } else if (isAPIRequest(request)) {
      event.respondWith(networkFirst(request, API_CACHE));
    } else {
      event.respondWith(networkFirst(request, DYNAMIC_CACHE));
    }
  } else {
    // For non-GET requests, try network first
    event.respondWith(networkFirst(request));
  }
});

// Push event - handle push notifications
self.addEventListener('push', (event) => {
  console.log('📱 Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'New notification from CloudMind',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-192x192.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'View Details',
        icon: '/icons/icon-192x192.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/icons/icon-192x192.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('CloudMind', options)
  );
});

// Notification click event
self.addEventListener('notificationclick', (event) => {
  console.log('🔔 Notification clicked');
  
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/dashboard')
    );
  } else if (event.action === 'close') {
    // Just close the notification
    return;
  } else {
    // Default action - open dashboard
    event.waitUntil(
      clients.openWindow('/dashboard')
    );
  }
});

// Background sync event
self.addEventListener('sync', (event) => {
  console.log('🔄 Background sync triggered:', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(performBackgroundSync());
  }
});

// Cache-first strategy for static assets
async function cacheFirst(request, cacheName) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.error('❌ Cache first strategy failed:', error);
    return new Response('Offline content not available', { status: 503 });
  }
}

// Network-first strategy for dynamic content
async function networkFirst(request, cacheName) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('🌐 Network failed, trying cache...');
    
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline page for navigation requests
    if (request.destination === 'document') {
      return caches.match('/offline.html');
    }
    
    return new Response('Offline content not available', { status: 503 });
  }
}

// Check if request is for static assets
function isStaticAsset(request) {
  return request.destination === 'style' ||
         request.destination === 'script' ||
         request.destination === 'image' ||
         request.destination === 'font' ||
         request.url.includes('/static/') ||
         request.url.includes('/_next/');
}

// Check if request is for API
function isAPIRequest(request) {
  return request.url.includes('/api/') ||
         request.url.includes('/graphql') ||
         request.url.includes('/websocket');
}

// Perform background sync
async function performBackgroundSync() {
  try {
    console.log('🔄 Performing background sync...');
    
    // Sync offline data
    const offlineData = await getOfflineData();
    if (offlineData.length > 0) {
      await syncOfflineData(offlineData);
    }
    
    // Update cached data
    await updateCachedData();
    
    console.log('✅ Background sync completed');
  } catch (error) {
    console.error('❌ Background sync failed:', error);
  }
}

// Get offline data from IndexedDB
async function getOfflineData() {
  // This would integrate with your IndexedDB implementation
  return [];
}

// Sync offline data with server
async function syncOfflineData(data) {
  // This would sync offline changes with the server
  console.log('📤 Syncing offline data:', data.length, 'items');
}

// Update cached data
async function updateCachedData() {
  try {
    const cache = await caches.open(API_CACHE);
    const requests = await cache.keys();
    
    for (const request of requests) {
      try {
        const response = await fetch(request);
        if (response.ok) {
          cache.put(request, response);
        }
      } catch (error) {
        console.log('⚠️ Failed to update cached request:', request.url);
      }
    }
  } catch (error) {
    console.error('❌ Failed to update cached data:', error);
  }
}

// Message event - handle messages from main thread
self.addEventListener('message', (event) => {
  console.log('📨 Message received in service worker:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_CACHE_STATUS') {
    event.ports[0].postMessage({
      type: 'CACHE_STATUS',
      data: {
        staticCache: STATIC_CACHE,
        dynamicCache: DYNAMIC_CACHE,
        apiCache: API_CACHE
      }
    });
  }
});

// Error event
self.addEventListener('error', (event) => {
  console.error('❌ Service Worker error:', event.error);
});

// Unhandled rejection event
self.addEventListener('unhandledrejection', (event) => {
  console.error('❌ Service Worker unhandled rejection:', event.reason);
});

console.log('🚀 CloudMind Service Worker loaded successfully'); 