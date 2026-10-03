const CACHE_NAME = "enal-ai-os-v1";
const STATIC_CACHE = "enal-ai-os-static-v1";
const DYNAMIC_CACHE = "enal-ai-os-dynamic-v1";

const STATIC_ASSETS = [
  "/",
  "/dashboard",
  "/manifest.json",
  "/icons/icon-192x192.png",
  "/icons/icon-512x512.png",
];

const DYNAMIC_ASSETS = [
  "/api/v1/chat",
  "/api/v1/conversations",
  "/api/v1/workspaces",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys
          .filter((key) => key !== STATIC_CACHE && key !== DYNAMIC_CACHE)
          .map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  if (request.method !== "GET") {
    return;
  }

  if (STATIC_ASSETS.some((asset) => url.pathname === asset || url.pathname.startsWith("/_next"))) {
    event.respondWith(
      caches.match(request).then((cached) => {
        const fetchPromise = fetch(request).then((networkResponse) => {
          if (networkResponse.ok) {
            const clone = networkResponse.clone();
            caches.open(STATIC_CACHE).then((cache) => {
              cache.put(request, clone);
            });
          }
          return networkResponse;
        }).catch(() => {
          return cached || new Response("Offline", { status: 503 });
        });
        return cached || fetchPromise;
      })
    );
    return;
  }

  if (url.pathname.startsWith("/api/")) {
    event.respondWith(
      fetch(request).catch(() => {
        return new Response(
          JSON.stringify({ detail: "Offline - API not available" }),
          {
            status: 503,
            headers: { "Content-Type": "application/json" },
          }
        );
      })
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((cached) => {
      const fetchPromise = fetch(request).then((networkResponse) => {
        if (networkResponse.ok && url.origin === self.location.origin) {
          const clone = networkResponse.clone();
          caches.open(DYNAMIC_CACHE).then((cache) => {
            cache.put(request, clone);
          });
        }
        return networkResponse;
      }).catch(() => {
        return cached || new Response("Offline", { status: 503 });
      });
      return cached || fetchPromise;
    })
  );
});

self.addEventListener("push", (event) => {
  if (!event.data) {
    return;
  }

  const data = event.data.json();
  const options = {
    body: data.body || "New notification from Enal AI OS",
    icon: "/icons/icon-192x192.png",
    badge: "/icons/icon-72x72.png",
    data: data.url || "/",
    actions: [
      { action: "open", title: "Open" },
      { action: "dismiss", title: "Dismiss" },
    ],
  };

  event.waitUntil(
    self.registration.showNotification(data.title || "Enal AI OS", options)
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  if (event.action === "dismiss") {
    return;
  }
  const url = event.notification.data || "/";
  event.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if (client.url === url && "focus" in client) {
          return client.focus();
        }
      }
      if ("navigate" in clients) {
        return clients.navigate(url);
      }
      return clients.openWindow(url);
    })
  );
});
