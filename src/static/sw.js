const CACHE_STATIC = "pwabuilder-static-v1";
const CACHE_DYNAMIC = "pwabuilder-dynamic-v1";
const CACHE_OTHER = "pwabuilder-other-v1";

// Importa Workbox no contexto do Service Worker
importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

// Listener para ativar o novo Service Worker assim que for atualizado
self.addEventListener("install", (event) => {
  self.skipWaiting(); // Ativa o novo SW imediatamente
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          return caches.delete(cacheName); // Apaga todos os caches antigos
        })
      );
    })
  );
  return self.clients.claim();
});


// Listener para limpar caches antigos
self.addEventListener("activate", (event) => {
  const currentCaches = [CACHE_STATIC, CACHE_DYNAMIC, CACHE_OTHER];
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (!currentCaches.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  return self.clients.claim();
});

// Rotas dinâmicas usando NetworkFirst
workbox.routing.registerRoute(
  new RegExp('/(login|logout|treino|alunos)'),
  new workbox.strategies.NetworkFirst({
    cacheName: CACHE_DYNAMIC,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 7 * 24 * 60 * 60,
      }),
    ],
  })
);

// Cache de arquivos estáticos
workbox.routing.registerRoute(
  /\.(?:js|css|html|png|jpg|jpeg|svg|gif)$/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: CACHE_STATIC,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 30 * 24 * 60 * 60,
      }),
    ],
  })
);


// Rotas com StaleWhileRevalidate
workbox.routing.registerRoute(
  new RegExp('/.*'),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: CACHE_OTHER,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 7 * 24 * 60 * 60,
      }),
    ],
  })
);
