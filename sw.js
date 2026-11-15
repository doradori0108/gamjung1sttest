/* 오프라인용: 앱 파일과 문제 데이터를 저장해 두고, 인터넷이 되면 뒤에서 새 버전으로 갱신한다 */
const CACHE = "dora-exam-v1.5.2";
const CORE = ["./", "index.html", "style.css", "app.js", "manifest.json", "icons/icon-192.png", "icons/icon-512.png",
  "data/subjects.json", "data/acct/units.json", "data/acct/exam.json", "data/acct/ox.json", "data/econ/units.json", "data/econ/exam.json", "data/econ/ox.json", "notes/econ.html", "notes/acct.html"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())) });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())) });
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;      // GitHub 동기화 요청은 건드리지 않음
  e.respondWith(caches.open(CACHE).then(async c => {
    const hit = await c.match(e.request, { ignoreSearch: true });
    const net = fetch(e.request, { cache: "no-cache" }).then(r => { if (r.ok) c.put(e.request, r.clone()); return r }).catch(() => hit);
    /* 화면 파일(html·css·js)은 인터넷이 되면 새 파일을 먼저 쓰고(최대 2.5초 대기), 안 되면 저장본 */
    if (e.request.mode === "navigate" || /\.(css|js|html)$|\/$/.test(u.pathname)) return hit ? Promise.race([net, new Promise(r => setTimeout(() => r(hit), 2500))]) : net;
    return hit || net;
  }));
});
