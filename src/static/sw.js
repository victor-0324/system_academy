const CACHE_STATIC = "pwabuilder-static-v1";
const CACHE_DYNAMIC = "pwabuilder-dynamic-v1";
const CACHE_OTHER = "pwabuilder-other-v1";

importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

// Listener para ativar o novo Service Worker assim que for atualizado
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
  }
});

// Listener para gerenciar ativação e limpeza de caches antigos
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
  // Garantir que o SW ative e controle todas as abas imediatamente
  return self.clients.claim();
});

// Rotas dinâmicas (ex: login, logout, treino, alunos) usando NetworkFirst
workbox.routing.registerRoute(
  new RegExp('/(login|logout|treino|alunos)'),
  new workbox.strategies.NetworkFirst({
    cacheName: CACHE_DYNAMIC,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50, // Limita o número de entradas no cache
        maxAgeSeconds: 7 * 24 * 60 * 60, // 1 semana
      }),
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [0, 200], // Cacheia apenas respostas com status 0 ou 200
      }),
    ],
  })
);

// Arquivos estáticos (CSS, JS, imagens) usando CacheFirst
workbox.routing.registerRoute(
  /\.(?:js|css|html|png|jpg|jpeg|svg|gif)$/,
  new workbox.strategies.CacheFirst({
    cacheName: CACHE_STATIC,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 100, // Limita o número de arquivos estáticos no cache
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 dias
      }),
      new workbox.cacheableResponse.CacheableResponsePlugin({
        statuses: [0, 200], // Cacheia apenas respostas com status 0 ou 200
      }),
    ],
  })
);

// Outras rotas usando StaleWhileRevalidate
workbox.routing.registerRoute(
  new RegExp('/.*'),
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: CACHE_OTHER,
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxEntries: 50, // Limita o cache para rotas variadas
        maxAgeSeconds: 7 * 24 * 60 * 60, // 1 semana
      }),
    ],
  })
);

// Registrar o Service Worker uma única vez e monitorar atualização
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js').then((registration) => {
    console.log('Service Worker registrado com sucesso:', registration);

    // Verificar se há um SW novo em espera
    if (registration.waiting) {
      // Informar a todos os clientes sobre o novo SW e pular a espera
      registration.waiting.postMessage({ type: 'SKIP_WAITING' });
    }

    // Monitora atualizações do SW
    registration.addEventListener('updatefound', () => {
      const newWorker = registration.installing;
      if (newWorker) {
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            console.log('Novo SW instalado, esperando para ativar.');
          }
        });
      }
    });
  }).catch((error) => {
    console.error('Falha ao registrar o Service Worker:', error);
  });

  // Monitora mensagens do Service Worker
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    console.log('Novo SW ativo, recarregando página.');
    window.location.reload();
  });
}
