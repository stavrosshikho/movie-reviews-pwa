const CACHE_NAME = "reviewvault-v1";

// Things to cache immediately (core shell)
const CORE_ASSETS = [
  "/",
  "/offline",
  "/static/style.css",
  "/static/script.js",
  "/manifest.webmanifest",
  "/static/icon-192.svg",
  "/static/icon-512.svg"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((key) => (key !== CACHE_NAME ? caches.delete(key) : null))
      )
    )
  );
  self.clients.claim();
});

// Helper: cache-first for static assets
async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  const fresh = await fetch(request);
  const cache = await caches.open(CACHE_NAME);
  cache.put(request, fresh.clone());
  return fresh;
}

// Helper: network-first for page navigation
async function networkFirst(request) {
  const cache = await caches.open(CACHE_NAME);
  try {
    const fresh = await fetch(request);
    cache.put(request, fresh.clone());
    return fresh;
  } catch (err) {
    const cached = await caches.match(request);
    if (cached) return cached;
    return caches.match("/offline");
  }
}

self.addEventListener("fetch", (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Only handle same-origin requests
  if (url.origin !== self.location.origin) return;

  // If it's a navigation (page load), do network-first with offline fallback
  if (req.mode === "navigate") {
    event.respondWith(networkFirst(req));
    return;
  }

  // Cache-first for static files
  if (url.pathname.startsWith("/static/")) {
    event.respondWith(cacheFirst(req));
    return;
  }

  // For everything else, try network-first but still allow cache fallback
  event.respondWith(networkFirst(req));
});
