const filesToCache = [
    	'./',
      './index.html',
      './js/Dejavu.js',
      './js/Matrix.js',
      './js/nn.json',
      './js/words_vector_plus1.js',
      './js/main.js',
      './css/main.css',
      './favicon.png',
      './manifest.json'
 ];

const staticCacheName = 'hntitlenator-v1';

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(staticCacheName)
    .then(cache => {
      return cache.addAll(filesToCache);
    })
  );
});

self.addEventListener('fetch', event => {
  console.log('Fetch event for ', event.request.url);
  event.respondWith(
    caches.match(event.request)
    .then(response => {
      if (response) {
        console.log('Found ', event.request.url, ' in cache');
        return response;
      }
      console.log('Network request for ', event.request.url);
      return fetch(event.request)

			.then(response => {
				return caches.open(staticCacheName).then(cache => {
					cache.put(event.request.url, response.clone());
					return response;
				});
			});

    }).catch(e => console.log(e) )
  );
});

self.addEventListener('activate', event => {

  const cacheWhitelist = [staticCacheName];

  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
