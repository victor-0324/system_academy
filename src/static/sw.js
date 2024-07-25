const CACHE_NAME = "pwabuilder-offline";
const PRECACHE_URLS = [
  '/', // Add more URLs of your critical assets
  '/static/css/style.css',
  '/static/js/main.js'
];

importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

// Precache critical assets
workbox.precaching.precacheAndRoute(PRECACHE_URLS);

// Cache First strategy for CSS and JS files with background update
workbox.routing.registerRoute(
  /\.(?:css|js)$/,
  new workbox.strategies.CacheFirst({
    cacheName: `${CACHE_NAME}-assets`,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 7 * 24 * 60 * 60, // 1 week
      }),
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [0, 200],
      }),
    ],
  })
);

// Network First strategy for HTML pages
workbox.routing.registerRoute(
  new RegExp('/.*'),
  new workbox.strategies.NetworkFirst({
    cacheName: `${CACHE_NAME}-pages`,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 7 * 24 * 60 * 60, // 1 week
      }),
    ],
  })
);

// Preload important resources
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(PRECACHE_URLS);
    })
  );
});

// Prefetch next likely navigation pages
self.addEventListener('fetch', event => {
  if (event.request.mode === 'navigate') {
    event.waitUntil(
      fetch(event.request).then(response => {
        return caches.open(CACHE_NAME).then(cache => {
          return cache.put(event.request, response.clone());
        });
      })
    );
  }
});
