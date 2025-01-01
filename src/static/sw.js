const CACHE_STATIC = "pwabuilder-static-v1";
const CACHE_DYNAMIC = "pwabuilder-dynamic-v1";

// Importa bibliotecas externas para o Service Worker
importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.1.2/workbox-sw.js');

// Demais códigos do Service Worker...
self.addEventListener("activate", (event) => {
    console.log("Service Worker ativado");
});
