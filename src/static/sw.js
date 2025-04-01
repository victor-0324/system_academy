const CACHE_STATIC = "pwabuilder-static-v2";  // Mudando a versão do cache para atualizar corretamente
const CACHE_DYNAMIC = "pwabuilder-dynamic-v2";
const CACHE_OTHER = "pwabuilder-other-v2";

// Importa Workbox no contexto do Service Worker
importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

// 🔹 Força a ativação imediata do novo Service Worker
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

// 🔹 Limpa TODOS os caches antigos ao ativar o novo Service Worker
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(cacheNames.map((cacheName) => caches.delete(cacheName)));
    })
  );
  return self.clients.claim();
});

// 🔹 Atualiza o Service Worker e recarrega a página automaticamente
self.addEventListener("install", (event) => {
  self.skipWaiting(); // Força a atualização imediata
});

// 🔹 Rotas dinâmicas usando NetworkFirst (para páginas que precisam estar sempre atualizadas)
workbox.routing.registerRoute(
  new RegExp('/(login|logout|treino|alunos)'),
  new workbox.strategies.NetworkFirst({
    cacheName: CACHE_DYNAMIC,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 7 * 24 * 60 * 60, // Expira em 7 dias
      }),
    ],
  })
);

// 🔹 Cache de arquivos estáticos (JS, CSS, imagens, etc.) com StaleWhileRevalidate para sempre atualizar
workbox.routing.registerRoute(
  /\.(?:js|css|html|png|jpg|jpeg|svg|gif)$/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: CACHE_STATIC,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 100,
        maxAgeSeconds: 30 * 24 * 60 * 60, // Expira em 30 dias
      }),
    ],
  })
);

// 🔹 Estratégia para outras rotas (garante que a versão mais recente seja carregada)
workbox.routing.registerRoute(
  new RegExp('/.*'),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: CACHE_OTHER,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 7 * 24 * 60 * 60, // Expira em 7 dias
      }),
    ],
  })
);
