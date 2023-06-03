const urlsToCache = ["/", "/static/index.js", "/static/files.css", "static/icons/folder.webp", "static/icons/unknown.webp"]
const CACHE_NAME = "v1";

const putInCache = async (request, response) => {
    const cache = await caches.open(CACHE_NAME);
    await cache.put(request, response);
};

const networkFirst = async (request) => {
    const response = await fetch(request).catch(() => caches.match(request));

    if (response) {
        putInCache(request, response.clone()).then();

        return response;
    }

    return caches.match(request.url);
};

const cacheFirst = async (request) => {
    const network = fetch(request)
        .then((res) => {
            putInCache(request, res.clone());
            return res;
        })
        .catch(() => undefined);
    const cacheResponse = await caches.match(request);

    if (cacheResponse)
        return cacheResponse;

    return network;
};

self.addEventListener("install", (event) => {
    event.waitUntil(caches.open(CACHE_NAME)
        .then(cache => cache.addAll(urlsToCache)));

    return self.skipWaiting()
});

self.addEventListener("activate", (event) => {
    if ("navigationPreload" in self.registration)
        event.waitUntil(self.registration.navigationPreload.enable());

    // Tell the active service worker to take control of the page immediately.
    return self.clients.claim();
});

self.addEventListener("fetch", (event) => {
    // We only want to call event.respondWith() if this is a navigation request
    // for an HTML page.
    event.respondWith(
        (async () => {
            // First, try to use the navigation preload response if it's supported.
            const preloadResponse = await event.preloadResponse.catch(() => undefined);

            if (preloadResponse) {
                return preloadResponse;
            }

            if (["script", "style", "image"].indexOf(event.request.destination) !== -1)
                return cacheFirst(event.request)

            // Always try the network first.
            return await networkFirst(event.request);
        })()
    );
});
