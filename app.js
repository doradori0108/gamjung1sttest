/* 감평 1차 문제풀이 (PWA)
   - 문제: data/<과목>/units.json · exam.json · ox.json
   - 기록: 이 기기(localStorage)에 바로 저장 → 설정에서 연결하면 GitHub 비공개 저장소 progress.json과 동기화
   - 문항 ID: "<과목>:<회차-번호>" (기출·보충), "<과목>:ox<번호>" (개념 O·X) */
"use strict";
const APP_VER = "1.9.19";
const DAILY_N = 10;               // 오늘의 문제 수 (과목별, 기출만)
const SEC_PER_Q = 60;             // 문제당 제한시간(초) → 10문제 = 10분
const LS_STATE = "dora-exam-v1", LS_SYNC = "dora-exam-sync", LS_THEME = "dora-exam-theme";
const N5 = "①②③④⑤";
const $ = s => document.querySelector(s);
const plain = s => String(s || "").replace(/<[^>]+>/g, "").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
const today = () => new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10);
const lvOf = n => n >= 15 ? "상" : n >= 8 ? "중" : "하";

/* ───────── 데이터 ───────── */
let SUBJ = [], D = {};
async function getJSON(p) { const r = await fetch(p, { cache: "no-cache" }); if (!r.ok) throw new Error(p + " " + r.status); return r.json() }
async function loadData() {
  SUBJ = await getJSON("data/subjects.json");
  await Promise.all(SUBJ.map(async s => {
    const [meta, exam, ox, sent] = await Promise.all([getJSON(`data/${s.id}/units.json`), getJSON(`data/${s.id}/exam.json`), getJSON(`data/${s.id}/ox.json`).catch(() => []), getJSON(`data/${s.id}/sent.json`).catch(() => [])]);
    D[s.id] = { meta, exam, ox, sent, ex: Object.fromEntries(exam.map(x => [x.k, x])), oxBy: Object.fromEntries(ox.map(b => [b.id, b])), ub: Object.fromEntries(meta.units.map(u => [u.u, u])) };
  }));
}

/* ───────── 기록 ───────── */
let S = null;
function blank() { return { v: 1, subjects: {}, hist: {}, days: {}, daily: {}, book: {}, sent: {} } }
function loadLocal() { try { return JSON.parse(localStorage.getItem(LS_STATE)) } catch (e) { return null } }
function saveLocal() { try { localStorage.setItem(LS_STATE, JSON.stringify(S)) } catch (e) { } }
function touch() { saveLocal(); schedulePush() }
const lecOf = sub => (S.subjects[sub] && S.subjects[sub].lec) || D[sub].meta.defaultLec;
function setLec(sub, lec) { S.subjects[sub] = { lec, t: Date.now() } }

/* 두 기록 합치기: 문항 기록은 더 나중 것, 하루 요약은 더 많이 푼 것, 오늘 세트는 더 많이 푼 쪽 */
function merge(A, B) {
  const M = blank();
  for (const k of new Set([...Object.keys(A.subjects || {}), ...Object.keys(B.subjects || {})])) {
    const a = (A.subjects || {})[k], b = (B.subjects || {})[k];
    M.subjects[k] = !a ? b : !b ? a : (b.t || 0) > (a.t || 0) ? b : a;
  }
  M.hist = Object.assign({}, A.hist);
  /* 합격노트: 문항마다 더 나중에 고친 쪽 (뺀 것도 on:false로 남겨 두어 다른 기기에도 빠짐이 전달됨) */
  M.book = Object.assign({}, A.book);
  for (const [k, b] of Object.entries(B.book || {})) { const a = M.book[k]; if (!a || (b.t || 0) > (a.t || 0)) M.book[k] = b }
  /* 문장 훈련: 문장마다 더 나중 기록 (문제풀이 기록 hist와 따로) */
  M.sent = Object.assign({}, A.sent);
  for (const [k, b] of Object.entries(B.sent || {})) { const a = M.sent[k]; if (!a || (b.t || 0) > (a.t || 0)) M.sent[k] = b }
  for (const [k, h] of Object.entries(B.hist || {})) { const a = M.hist[k]; if (!a || (h.t || 0) > (a.t || 0)) M.hist[k] = h }
  for (const src of [A.days || {}, B.days || {}]) for (const [d, v] of Object.entries(src)) {
    M.days[d] = M.days[d] || {};
    for (const [s, x] of Object.entries(v)) { const c = M.days[d][s]; if (!c || x.done > c.done || (x.done === c.done && x.ok > c.ok)) M.days[d][s] = x }
  }
  const keepDays = Object.keys(Object.assign({}, A.daily, B.daily)).sort().slice(-3);
  for (const d of keepDays) {
    M.daily[d] = {};
    const a = (A.daily || {})[d] || {}, b = (B.daily || {})[d] || {};
    for (const s of new Set([...Object.keys(a), ...Object.keys(b)])) {
      const x = a[s], y = b[s];
      if (!x || !y) { M.daily[d][s] = x || y; continue }
      const nx = (x.res || []).filter(Boolean).length, ny = (y.res || []).filter(Boolean).length;
      const same = JSON.stringify(x.set) === JSON.stringify(y.set), ux = (x.tm || {}).used || 0, uy = (y.tm || {}).used || 0;
      let pick;
      if (nx !== ny) pick = nx > ny ? x : y;
      else if (!same) pick = ux !== uy ? (ux > uy ? x : y) : (x.c || 0) <= (y.c || 0) ? x : y;   // 둘 다 안 풀었으면 시간을 더 쓴(먼저 시작한) 쪽
      else pick = (x.t || 0) >= (y.t || 0) ? x : y;
      /* 같은 세트면 쓴 시간은 줄어들지 않는다: 두 기기 중 더 긴 시간을 남긴다 (예전엔 다른 기기의 짧은 시간으로 덮여 '리셋'처럼 보였음) */
      if (same && ((pick.tm || {}).used || 0) < Math.max(ux, uy)) pick = Object.assign({}, pick, { tm: Object.assign({}, pick.tm, { used: Math.max(ux, uy) }) });
      M.daily[d][s] = pick;
    }
  }
  return M;
}
const stable = o => JSON.stringify(o, (k, v) => v && typeof v === "object" && !Array.isArray(v) ? Object.fromEntries(Object.keys(v).sort().map(x => [x, v[x]])) : v);
const norm = o => { const m = merge(o, blank()); delete m.updated; delete m.app; return m };
function exportState() { const M = merge(S, blank()); M.v = 1; M.updated = new Date().toISOString(); M.app = APP_VER; return M }

/* ───────── 동기화 (GitHub 비공개 저장소) ───────── */
let SY = {}; try { SY = JSON.parse(localStorage.getItem(LS_SYNC)) || {} } catch (e) { }
const saveSY = () => { try { localStorage.setItem(LS_SYNC, JSON.stringify(SY)) } catch (e) { } };
const syncOn = () => !!(SY.owner && SY.repo && SY.token);
let syncState = { busy: false, again: false, status: "", msg: "", at: 0 }, pushTimer = null;
const b64e = s => btoa(unescape(encodeURIComponent(s)));
const b64d = s => decodeURIComponent(escape(atob(s.replace(/\s/g, ""))));
function ghFetch(path, opt = {}) {
  return fetch(`https://api.github.com/repos/${encodeURIComponent(SY.owner)}/${encodeURIComponent(SY.repo)}${path}`, {
    method: opt.method || "GET", cache: "no-store",
    headers: Object.assign({ Authorization: `Bearer ${SY.token}`, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28" }, opt.body ? { "Content-Type": "application/json" } : {}),
    body: opt.body ? JSON.stringify(opt.body) : undefined
  });
}
function ghMsg(st) {
  return st === 401 ? "토큰이 맞지 않거나 기한이 지났어요. 설정에서 토큰을 다시 넣어 주세요."
    : st === 403 ? "토큰에 이 저장소의 읽기·쓰기 권한이 없어요(Contents: Read and write)."
      : st === 404 ? "저장소를 찾을 수 없어요. GitHub 아이디·저장소 이름과 토큰의 저장소 선택을 확인해 주세요."
        : "GitHub 응답 오류(" + st + ")";
}
function schedulePush(ms = 6000) { if (!syncOn()) return; clearTimeout(pushTimer); pushTimer = setTimeout(syncNow, ms) }
async function syncNow() {
  if (!syncOn()) { drawSync(); return }
  clearTimeout(pushTimer);
  if (syncState.busy) { syncState.again = true; return }
  syncState.busy = true; syncState.status = "busy"; drawSync();
  try {
    for (let tries = 0; tries < 3; tries++) {
      const g = await ghFetch("/contents/progress.json");
      let sha = null, remote = null;
      if (g.status === 200) { const j = await g.json(); sha = j.sha; remote = JSON.parse(b64d(j.content)) }
      else if (g.status !== 404) throw { st: g.status };
      else { const rr = await ghFetch(""); if (rr.status !== 200) throw { st: rr.status } }
      const before = JSON.stringify(exportState().daily);
      if (remote) { S = merge(S, remote); saveLocal() }
      const body = exportState();
      const same = remote && stable(norm(remote)) === stable(norm(body));
      if (!same) {
        const p = await ghFetch("/contents/progress.json", { method: "PUT", body: { message: `기록 ${today()} (${navigator.userAgent.includes("Mobile") ? "휴대폰" : "PC"})`, content: b64e(JSON.stringify(body)), ...(sha ? { sha } : {}) } });
        if (p.status === 409 || p.status === 422) continue;   // 그 사이 다른 기기가 저장 → 다시 받아서 합치기
        if (!p.ok) throw { st: p.status };
      }
      syncState.status = "ok"; syncState.msg = ""; syncState.at = Date.now();
      if (JSON.stringify(exportState().daily) !== before) onRemoteChange();
      break;
    }
  } catch (e) {
    syncState.status = navigator.onLine === false ? "offline" : "err";
    syncState.msg = e && e.st ? ghMsg(e.st) : navigator.onLine === false ? "인터넷 연결이 없어요. 연결되면 자동으로 맞춥니다." : "동기화 실패: " + (e && e.message || e);
  } finally {
    syncState.busy = false; drawSync(); refreshHomeIfShown();
    if (syncState.again) { syncState.again = false; schedulePush(1000) }
  }
}
function drawSync() {
  const el = $("#syncPill"); if (!el) return;
  const t = syncState.at ? new Date(syncState.at).toTimeString().slice(0, 5) : "";
  const [cls, txt] = !syncOn() ? ["", "☁️ 동기화 꺼짐"] : syncState.status === "busy" ? ["", "🔄 동기화 중…"] : syncState.status === "ok" ? ["ok", `✅ 동기화 ${t}`] : syncState.status === "offline" ? ["", "📴 오프라인"] : syncState.status === "err" ? ["err", "⚠️ 동기화 오류"] : ["", "☁️ 동기화 대기"];
  el.className = "pill " + cls; el.textContent = txt;
}

/* ───────── 출제 ───────── */
function rng(seed) {
  let h = 1779033703; for (const c of seed) h = Math.imul(h ^ c.charCodeAt(0), 3432918353), h = h << 13 | h >>> 19;
  return function () { h = Math.imul(h ^ h >>> 16, 2246822507); h = Math.imul(h ^ h >>> 13, 3266489909); h ^= h >>> 16; return (h >>> 0) / 4294967296 }
}
function shuffle(a, r) { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1));[a[i], a[j]] = [a[j], a[i]] } return a }
/* 출제 가중치: 안 푼 문제 4 · 틀린 문제 3 · 맞힌 문제 1, 최근에 본 문제는 낮추고 오래 안 본 문제는 높인다 */
function weight(id, day) {
  const h = S.hist[id]; if (!h) return 4;
  let w = h.ok ? 1 : 3;
  if (h.last) { const g = (Date.parse(day) - Date.parse(h.last)) / 864e5; w *= g < 2 ? .2 : g < 7 ? .7 : 1.5 }
  return w;
}
function wpick(list, wf, r) { let t = list.reduce((s, x) => s + wf(x), 0) * r(), i = 0; for (; i < list.length - 1; i++) { t -= wf(list[i]); if (t <= 0) break } return i }
const exOfU = (sub, u) => D[sub].exam.filter(x => x.u === u && !x.skip && !x.gen);   // 문제풀이 = 기출만(보충 문제 제외)
const oxOfU = (sub, u) => D[sub].ox.filter(b => b.u === u);
function openUnits(sub) { const m = D[sub].meta, L = Math.min(lecOf(sub), m.dataThrough); return m.units.filter(u => u.lec <= L) }
/* 단원별 몫: 수강한 단원 중 문제가 있는 단원에 10년 출제 문항 수 비율로 나눈다 */
function quotas(sub, r) {
  const U = openUnits(sub).map(x => ({ u: x.u, w: x.n || 0.5, ex: exOfU(sub, x.u).length, ox: oxOfU(sub, x.u).length })).filter(x => x.ex + x.ox > 0);
  const cap = x => x.ox > 0 ? DAILY_N : x.ex;
  const total = Math.min(DAILY_N, U.reduce((s, x) => s + cap(x), 0));
  const q = Object.fromEntries(U.map(x => [x.u, 0]));
  let left = total, act = U.slice();
  while (left > 0 && act.length) {
    const tot = act.reduce((s, x) => s + x.w, 0), raw = act.map(x => left * x.w / tot);
    let given = 0; act.forEach((x, i) => { const f = Math.floor(raw[i]); q[x.u] += f; given += f });
    let rem = left - given; const fr = act.map((x, i) => ({ x, w: raw[i] - Math.floor(raw[i]) }));
    while (rem > 0 && fr.some(f => f.w > 0)) { const i = wpick(fr, f => f.w, r); if (fr[i].w <= 0) continue; q[fr[i].x.u]++; fr[i].w = 0; rem-- }
    left = 0; act.forEach(x => { if (q[x.u] > cap(x)) { left += q[x.u] - cap(x); q[x.u] = cap(x) } });
    act = act.filter(x => q[x.u] < cap(x));
    if (rem > 0) left += rem;
  }
  return { q, U };
}
function buildSet(sub, seed, day) {
  const r = rng(seed), { q, U } = quotas(sub, r), out = [], usedEx = new Set(), usedOx = new Set();
  const oxw = b => weight(`${sub}:ox${b.id}`, day);
  for (const x of U) {
    const exs = exOfU(sub, x.u), oxs = oxOfU(sub, x.u);
    for (let s = 0; s < q[x.u]; s++) {
      const exLeft = exs.filter(e => !usedEx.has(e.k));
      // O·X가 있는 단원: 35%는 기출, 나머지는 O·X(80%) 또는 O·X로 만든 5지선다(20%)
      if (exLeft.length && (!oxs.length || r() < 0.35)) { const e = exLeft[wpick(exLeft, e => weight(`${sub}:${e.k}`, day), r)]; usedEx.add(e.k); out.push({ t: "ex", k: e.k }); continue }
      if (r() < 0.2) { const it = mcItem(sub, x.u, r() < 0.6, r, usedOx, oxw); if (it) { out.push(it); continue } }
      const pool = oxs.filter(b => !usedOx.has(b.id)), from = pool.length ? pool : oxs, b = from[wpick(from, oxw, r)]; usedOx.add(b.id); out.push({ t: "ox", id: b.id });
    }
  }
  shuffle(out, r);
  // 방금 나온 O·X 지문과 연결된 기출이 세트에 있으면 그 바로 뒤로
  const ox = D[sub].oxBy;
  for (const e of out.filter(z => z.t === "ex")) {
    const linked = z => z.t === "ox" && (ox[z.id].links || []).some(l => l.split(" ")[0] === e.k);
    if (out.some(linked)) { out.splice(out.indexOf(e), 1); e.after = true; out.splice(out.findIndex(linked) + 1, 0, e) }
  }
  return out;
}
/* O·X 지문 5개로 5지선다 만들기. neg(옳지 않은 것 고르기)면 정답 1개는 X 지문, 나머지 4개는 O 지문 */
function mcItem(sub, u, neg, r, usedOx, oxw) {
  const oxs = oxOfU(sub, u), keyPool = oxs.filter(b => b.a === !neg), others = oxs.filter(b => b.a === neg);
  if (!keyPool.length || others.length < 4) return null;
  const fresh = keyPool.filter(b => !usedOx.has(b.id)), from = fresh.length ? fresh : keyPool, key = from[wpick(from, oxw, r)];
  usedOx.add(key.id);
  return { t: "mc", neg, u, opts: shuffle([key, ...shuffle(others.slice(), r).slice(0, 4)], r).map(b => b.id), key: key.id };
}

/* ───────── 화면 상태 ───────── */
let day = today();
let V = { route: "home", sub: null, tab: null, mode: null, unit: null, Q: [], res: [], idx: 0, key: "" };
let T = { used: 0, run: 0, paused: false };
const qid = (sub, q) => q.t === "ex" ? `${sub}:${q.k}` : `${sub}:ox${q.t === "mc" ? q.key : q.id}`;
const answered = () => V.res.filter(Boolean).length;
function nextUn(from) { for (let k = 1; k <= V.Q.length; k++) { const i = (from + k) % V.Q.length; if (!V.res[i]) return i } return -1 }
const timed = () => V.route === "subject" && (V.mode === "daily" || V.mode === "extra");
const entry = sub => ((S.daily[day] || {})[sub || V.sub]);

function dailyEntry(sub, create) {
  let e = entry(sub);
  const L = Math.min(lecOf(sub), D[sub].meta.dataThrough);
  const valid = e && e.set && e.set.every(q => q.t === "ex" ? D[sub].ex[q.k] : q.t === "ox" ? D[sub].oxBy[q.id] : D[sub].oxBy[q.key]);
  const none = (e && (e.res || []).filter(Boolean).length) === 0;
  if (e && valid && !(none && (e.lec !== L || e.set.length !== DAILY_N))) return e;
  if (!create) return null;
  S.daily[day] = S.daily[day] || {};
  e = S.daily[day][sub] = { set: buildSet(sub, `${day}|${sub}|${L}`, day), res: [], tm: { used: 0, paused: false }, lec: L, c: Date.now(), t: Date.now() };
  for (const d of Object.keys(S.daily).sort().slice(0, -3)) delete S.daily[d];
  touch();
  return e;
}
function summary(sub) {
  const e = dailyEntry(sub, false), d = ((S.days[day] || {})[sub]);
  const total = e ? e.set.length : DAILY_N, done = e ? (e.res || []).filter(Boolean).length : 0, ok = e ? (e.res || []).filter(r => r && r.ok).length : 0;
  return { total, done, ok, started: !!e, d };
}
function streak(sub) {
  let n = 0;
  for (let i = 0; i < 400; i++) {
    const k = new Date(Date.parse(day) - i * 864e5).toISOString().slice(0, 10), v = (S.days[k] || {})[sub];
    if (v && v.done >= v.total) n++; else if (i === 0) continue; else break;
  }
  return n;
}
function wrongList(sub) {
  const out = [];
  for (const [id, h] of Object.entries(S.hist)) {
    if (h.ok !== false || !id.startsWith(sub + ":")) continue;
    const k = id.slice(sub.length + 1);
    if (k.startsWith("ox")) { const b = D[sub].oxBy[+k.slice(2)]; if (b) out.push({ q: { t: "ox", id: b.id }, h }) }
    else if (D[sub].ex[k] && !D[sub].ex[k].skip) out.push({ q: { t: "ex", k }, h });
  }
  return out.sort((a, b) => (b.h.wrong || 0) - (a.h.wrong || 0) || String(a.h.last).localeCompare(String(b.h.last)));
}

/* ───────── 합격노트 ───────── */
const BK_TAGS = [["mix", "🔁", "헷갈림"], ["key", "⭐", "중요"], ["mem", "🧠", "암기"]];
function qOfId(sub, id) {
  if (!id.startsWith(sub + ":")) return null; const k = id.slice(sub.length + 1);
  if (k.startsWith("ox")) { const b = D[sub].oxBy[+k.slice(2)]; return b ? { t: "ox", id: b.id } : null }
  return D[sub].ex[k] ? { t: "ex", k } : null;
}
function bookList(sub, tag) {
  const out = [];
  for (const [id, b] of Object.entries(S.book || {})) {
    if (!b.on || !id.startsWith(sub + ":") || (tag && !(b.tags || []).includes(tag))) continue;
    const q = qOfId(sub, id); if (q) out.push({ id, q, b });
  }
  /* 같은 문제가 다른 번호로 두 번 들어간 경우(앞으로 문제를 추가하다 생길 수 있음)도 한 번만: 내용이 같으면 최근 것만 */
  const seen = new Set();
  return out.sort((a, b) => (b.b.t || 0) - (a.b.t || 0)).filter(x => { const g = sigOf(sub, x.q); if (seen.has(g)) return false; seen.add(g); return true });
}
function sigOf(sub, q) {
  const n = t => plain(t).replace(/\s+/g, "");
  if (q.t === "ex") { const x = D[sub].ex[q.k]; return "ex|" + n(x.q) + "|" + x.o.map(n).join("|") }
  return "ox|" + n(D[sub].oxBy[q.id].s);
}
function bookSet(id, patch) {
  const b = Object.assign({ tags: [], memo: "", on: true }, S.book[id], patch, { t: Date.now() });
  b.tags = BK_TAGS.map(x => x[0]).filter(t => b.tags.includes(t)); S.book[id] = b; touch();
}
/* 문제·해설 화면의 '📒 합격노트' 막대. wrong=true면 저장할 때 '헷갈림'을 먼저 골라 둔다 */
function bookBar(id, q, wrong) {
  const b = S.book[id], on = !!(b && b.on), tags = (b && b.tags) || [];
  return `<div class="bk ${on ? "on" : ""}" data-id="${esc2(id)}" data-w="${wrong ? 1 : ""}">
    <button class="bkbtn" aria-pressed="${on}">${on ? "📒 합격노트에 저장됨 ✓" : "📒 합격노트에 저장"}</button>
    <div class="bkpanel" ${on ? "" : "hidden"}><div class="bktags" role="group" aria-label="분류">${BK_TAGS.map(([k, e, n]) => `<button aria-pressed="${tags.includes(k)}" data-k="${k}">${e} ${n}</button>`).join("")}<button class="bkdel" data-del="1">빼기</button></div>
    <input class="bkmemo" maxlength="120" placeholder="✍️ 한 줄 메모 (예: 재평가는 감가상각 먼저)" value="${esc2((b && b.memo) || "").replace(/"/g, "&quot;")}"></div></div>`;
}
function bindBook(root) {
  root.querySelectorAll(".bk").forEach(el => {
    const id = el.dataset.id, redraw = () => { const n = document.createElement("div"); n.innerHTML = bookBar(id, null, el.dataset.w); const ne = n.firstElementChild; el.replaceWith(ne); bindBook(ne.parentNode) };
    el.querySelector(".bkbtn").onclick = () => {
      const b = S.book[id];
      if (b && b.on) bookSet(id, { on: false }); else { bookSet(id, { on: true, tags: b && b.tags && b.tags.length ? b.tags : el.dataset.w ? ["mix"] : [] }); toast("📒 합격노트에 저장했어요") }
      redraw();
    };
    el.querySelectorAll(".bktags button[data-k]").forEach(t => t.onclick = () => { const b = S.book[id], tg = new Set(b.tags || []); tg.has(t.dataset.k) ? tg.delete(t.dataset.k) : tg.add(t.dataset.k); bookSet(id, { tags: [...tg] }); redraw() });
    const del = el.querySelector(".bkdel"); if (del) del.onclick = () => { bookSet(id, { on: false }); redraw() };
    const memo = el.querySelector(".bkmemo"); let tm = 0;
    if (memo) memo.oninput = () => { clearTimeout(tm); tm = setTimeout(() => bookSet(id, { memo: memo.value.trim() }), 500) };
    if (memo) memo.onchange = () => { clearTimeout(tm); bookSet(id, { memo: memo.value.trim() }) };
  });
}
function qBrief(sub, q) {
  if (q.t === "ex") { const x = D[sub].ex[q.k]; return { head: x.gen ? "✏️ 보충 문제" : `📜 제${x.y}회 ${x.n}번`, text: plain(x.q), u: x.u } }
  const b = D[sub].oxBy[q.id]; return { head: "⭕ O·X 지문", text: plain(b.s), u: b.u };
}
function renderBookPick() {
  const sub = V.sub, tag = BK_TAGS.some(t => t[0] === V.arg) ? V.arg : "", all = bookList(sub), list = bookList(sub, tag);
  if (!all.length) { $("#main").innerHTML = `<section class="card center"><div class="bigemo" aria-hidden="true">📒</div><p class="exp"><b>합격노트가 비어 있어요.</b><br>문제를 풀다가 헷갈리거나 중요한 문제에서 <b>📒 합격노트에 저장</b>을 누르면 여기에 모여요. 🔁 헷갈림 · ⭐ 중요 · 🧠 암기로 나누고 한 줄 메모도 붙일 수 있어요.</p></section>`; return }
  const cnt = k => all.filter(x => (x.b.tags || []).includes(k)).length;
  $("#main").innerHTML = `<div class="bkfilter" role="tablist">${[["", "📒", "전체", all.length], ...BK_TAGS.map(([k, e, n]) => [k, e, n, cnt(k)])].map(([k, e, n, c]) => `<button role="tab" aria-selected="${tag === k}" data-k="${k}">${e} ${n} <b>${c}</b></button>`).join("")}</div>
    ${list.length ? `<button class="btn" id="bkPlay">⚔️ ${tag ? BK_TAGS.find(t => t[0] === tag)[2] + " " : ""}${list.length}문제 다시 풀기</button>` : `<p class="exp">이 분류에 저장한 문제가 없어요.</p>`}
    <ul class="bklist">${list.map(({ id, q, b }) => {
      const br = qBrief(sub, q), h = S.hist[id], un = D[sub].ub[br.u];
      return `<li><div class="bkh"><b>${br.head}</b><span class="bkt2">${(b.tags || []).map(k => BK_TAGS.find(t => t[0] === k)[1]).join("")}</span><span class="rec" title="마지막 결과">${h ? (h.ok ? "✅" : "❌") : "·"}</span></div>
        <p class="bkq">${esc2(br.text.length > 90 ? br.text.slice(0, 90) + "…" : br.text)}</p>${b.memo ? `<p class="bkm">✍️ ${esc2(b.memo)}</p>` : ""}
        <div class="bkf"><small>${esc2(un ? un.nm : "")}</small><button data-one="${esc2(id)}">▶ 풀기</button><button class="gh" data-out="${esc2(id)}">빼기</button></div></li>`;
    }).join("")}</ul>`;
  $("#main").querySelectorAll(".bkfilter button").forEach(b => b.onclick = () => go(`#/s/${sub}/book${b.dataset.k ? "/" + b.dataset.k : ""}`));
  if ($("#bkPlay")) $("#bkPlay").onclick = () => go(`#/s/${sub}/book/play${tag ? "-" + tag : ""}`);
  $("#main").querySelectorAll("[data-one]").forEach(b => b.onclick = () => go(`#/s/${sub}/book/q=${encodeURIComponent(b.dataset.one)}`));
  $("#main").querySelectorAll("[data-out]").forEach(b => b.onclick = () => { bookSet(b.dataset.out, { on: false }); toast("합격노트에서 뺐어요"); render() });
  $("#foot").textContent = "합격노트는 기기 간 동기화에 함께 저장돼요. 다시 풀기는 제한시간 없이, 최근에 저장한 문제부터 나옵니다.";
}

/* ───────── 라우팅 ───────── */
function go(hash) { if (location.hash !== hash) location.hash = hash; else route() }
function route() {
  closeModal();
  const p = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  tmStop(); saveTimer();
  if (p[0] === "settings") { V = { route: "settings", key: "settings" }; return renderSettings() }
  if (p[0] === "s" && D[p[1]]) {
    const sub = p[1], tab = ["note", "daily", "unit", "wrong", "book", "map", "sent"].includes(p[2]) ? p[2] : "daily", arg = p[3] || "";
    const key = [sub, tab, arg].join("/");
    if (V.key === key && V.route === "subject") return render();
    V = { route: "subject", sub, tab, mode: null, unit: null, Q: [], res: [], idx: 0, key, arg };
    if (tab === "note" || tab === "sent") return render();
    if (tab === "daily" && arg === "extra") {
      /* 추가 문제는 화면을 나갔다 와도 같은 세트·남은 시간 그대로 (예전엔 나갈 때마다 새 세트 + 20분으로 리셋) */
      const x = extraGet(sub); V.mode = "extra";
      if (x) { V.Q = x.Q; V.res = x.res; T = { used: x.used, run: 0, paused: !!x.paused } }
      else { V.Q = buildSet(sub, day + "#" + Math.random(), day); T = { used: 0, run: 0, paused: false }; V.res = []; extraPut(sub) }
    }
    else if (tab === "daily") { const e = dailyEntry(sub, true); V.mode = "daily"; V.Q = e.set; V.res = e.res; T = { used: e.tm ? e.tm.used : 0, run: 0, paused: !!(e.tm && e.tm.paused) } }
    else if (tab === "unit" && arg && D[sub].ub[arg]) {
      V.mode = "unit"; V.unit = arg;
      const rank = x => { const h = S.hist[`${sub}:${x.k}`]; return !h ? 0 : h.ok ? 2 : 1 };
      V.Q = exOfU(sub, arg).slice().sort((a, b) => rank(a) - rank(b) || (b.y || 0) - (a.y || 0) || (a.n || 0) - (b.n || 0)).map(x => ({ t: "ex", k: x.k }));
    }
    else if (tab === "wrong" && arg === "play") { V.mode = "wrong"; V.Q = wrongList(sub).map(x => x.q) }
    else if (tab === "book" && arg.startsWith("play")) { V.mode = "book"; V.Q = bookList(sub, arg.split("-")[1] || "").map(x => x.q) }
    else if (tab === "book" && arg.startsWith("q=")) { const q = qOfId(sub, decodeURIComponent(arg.slice(2))); V.mode = "book"; V.Q = q ? [q] : [] }
    V.idx = V.res.filter(Boolean).length >= V.Q.length ? V.Q.length : Math.max(0, nextUn(-1));
    return render();
  }
  V = { route: "home", key: "home" }; renderHome();
}
window.addEventListener("hashchange", route);
function onRemoteChange() {
  if (V.route === "subject" && V.mode === "daily" && $("#modal").hidden && !$("#psheet.in")) { const e = entry(V.sub); if (e && e !== V.entryRef) { V.key = ""; route() } }
  else if (V.route === "home") renderHome();
}
function refreshHomeIfShown() { if (V.route === "home") renderHome() }

/* ───────── 공통 머리 ───────── */
function chrome({ subject = "", back = null, eyebrow = "", title = "", meta = "", tabs = false, stats = false }) {
  document.body.classList.remove("split");
  document.body.dataset.subject = subject;
  $("#topbar").innerHTML = `${back ? `<button class="back" id="backBtn">‹ ${back.label}</button>` : `<span class="brand">🎯 감평 1차</span>`}<span class="tright"><button class="iconbtn" id="themeBtn"></button><button class="pill" id="syncPill"></button></span>`;
  if (back) $("#backBtn").onclick = () => go(back.hash);
  $("#syncPill").onclick = () => go("#/settings");
  $("#themeBtn").onclick = () => { localStorage.setItem(LS_THEME, isDark() ? "light" : "dark"); applyTheme(); if (V.route === "settings") renderSettings() };
  drawSync(); drawThemeBtn();
  $("#eyebrow").textContent = eyebrow; $("#title").innerHTML = title; $("#meta").innerHTML = meta;
  $("#tabs").hidden = !tabs; $("#stats").hidden = !stats;
  $("#timerbar").hidden = true; $("#progress").hidden = true; $("#foot").textContent = "";
  $("#seg").hidden = true; $("#notebox").hidden = true; document.body.classList.remove("noting"); $("#main").hidden = false; $("#eyebrow").hidden = false; $("#meta").hidden = false;
}
const EXAM1 = "2027-04-04";      // 1차 시험일 가정: 2026년 제37회(4월 4일)와 같은 날짜
function dday() { const n = Math.round((Date.parse(EXAM1) - Date.parse(day)) / 864e5); return `<span class="dday" title="2026년 1차 시험일(4월 4일)과 같은 날짜로 가정">${n > 0 ? "D-" + n + "일" : n === 0 ? "D-day" : "D+" + -n + "일"} <small>(26년도 기준)</small></span>` }
const dateLabel = () => { const d = new Date(day + "T00:00:00"); return `<b>${day.replace(/-/g, ".")}</b> (${"일월화수목금토"[d.getDay()]}) ${dday()}` };
function lecLabel(sub, lec) { const m = D[sub].meta; return m.stepLabel === "강" ? `${lec}강 · ${m.lectures[lec - 1] || ""}` : `${m.lectures[lec - 1] || ""}` }

/* ───────── 게임 요소 (기록에서 계산만 하고 따로 저장하지 않음) ───────── */
const EMO = { acct: "🧮", econ: "📈", civil: "⚖️", law: "🏛️", re: "🏠" };
const emoOf = s => EMO[s] || "📘";
const starRow = (n, max) => `<span class="stars" role="img" aria-label="별 ${max}개 중 ${n}개">${'<i class="on">★</i>'.repeat(n)}${"<i>★</i>".repeat(Math.max(0, max - n))}</span>`;
function accOf(sub) { let s = 0, o = 0; for (const [id, h] of Object.entries(S.hist)) if (id.startsWith(sub + ":")) { s++; if (h.ok) o++ } return { s, o, p: s ? Math.round(o / s * 100) : 0 } }
function bestStreak(sub) {
  const ds = Object.keys(S.days).filter(d => { const v = S.days[d][sub]; return v && v.total && v.done >= v.total }).sort();
  let best = 0, run = 0, prev = 0;
  for (const d of ds) { const t = Date.parse(d); run = prev && t - prev === 864e5 ? run + 1 : 1; prev = t; best = Math.max(best, run) }
  return best;
}
function badgeList() {
  const subs = SUBJ.map(s => s.id), hist = Object.entries(S.hist);
  const seenEx = hist.filter(([id]) => !/:ox\d+$/.test(id)).length, fixed = hist.filter(([, h]) => h.ok && h.wrong > 0).length;
  const best = Math.max(0, ...subs.map(bestStreak)), vals = Object.values(S.days).flatMap(v => Object.values(v));
  const B = [
    ["first", "🌱", "첫걸음", "문제 1개 풀기", hist.length > 0],
    ["clear", "✅", "오늘 클리어", "오늘의 문제 한 세트 끝내기", vals.some(x => x.total && x.done >= x.total)],
    ["double", "🎯", "올클리어", "하루에 모든 과목 오늘의 문제 끝내기", Object.values(S.days).some(v => subs.every(s => v[s] && v[s].total && v[s].done >= v[s].total))],
    ["perfect", "💯", "만점", `오늘의 문제 ${DAILY_N}개 전부 맞히기`, vals.some(x => x.total && x.ok >= x.total)],
    ["s3", "🔥", "3일 연속", "한 과목 3일 연속 완료", best >= 3],
    ["s7", "☄️", "7일 연속", "한 과목 7일 연속 완료", best >= 7],
    ["s30", "💎", "30일 연속", "한 과목 30일 연속 완료", best >= 30],
    ["ex100", "📚", "기출 100", "서로 다른 기출 100문항 풀기", seenEx >= 100],
    ["ex300", "🏆", "기출 300", "서로 다른 기출 300문항 풀기", seenEx >= 300],
    ["fix10", "🧹", "오답 정리왕", "틀렸던 문제 10개 다시 맞히기", fixed >= 10],
    ["half", "🗺️", "반환점", "한 과목 진도 절반 넘기기", subs.some(s => lecOf(s) * 2 >= D[s].meta.lectures.length)],
    ["book10", "📒", "합격노트 10", "합격노트에 10문제 모으기", Object.values(S.book || {}).filter(b => b.on).length >= 10]
  ];
  return B.map(([id, e, n, d, ok]) => ({ id, e, n, d, ok }));
}
const LS_BADGE = "dora-exam-badges";
/* 새로 딴 배지: 이 기기에서 아직 축하하지 않은 배지 */
function newBadges() {
  let seen = []; try { seen = JSON.parse(localStorage.getItem(LS_BADGE)) || [] } catch (e) { }
  const got = badgeList().filter(b => b.ok), fresh = got.filter(b => !seen.includes(b.id));
  try { localStorage.setItem(LS_BADGE, JSON.stringify(got.map(b => b.id))) } catch (e) { }
  return fresh;
}
function toast(html) {
  let t = $("#toast"); if (!t) { t = document.createElement("div"); t.id = "toast"; t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t) }
  t.innerHTML = html; t.hidden = false; t.classList.remove("show"); void t.offsetWidth; t.classList.add("show");
  clearTimeout(t._h); t._h = setTimeout(() => { t.hidden = true }, 4200);
}
function celebrate() { const f = newBadges(); if (f.length) toast(`<b>🏅 새 배지!</b> ${f.map(b => `${b.e} ${b.n}`).join(" · ")}`) }
function pathDots(sub) {
  const m = D[sub].meta, L = lecOf(sub);
  return `<div class="path" role="img" aria-label="진도 ${L} / ${m.lectures.length}">${m.lectures.map((_, i) => `<i class="${i + 1 < L ? "done" : i + 1 === L ? "cur" : ""}"></i>`).join("")}</div>`;
}

/* ───────── 업데이트 소식 · 사용방법 ───────── */
const LS_SEENVER = "dora-exam-seenver";
const NEWS = [
  ["1.9.19", "2026.11.18", ["회계 25단원(재무비율 분석), 경제 51강(AD-AS · 경기변동) 기출 · 문장 · 개념정리 추가"]],
  ["1.9.18", "2026.11.18", ["회계 24단원(현금흐름표), 경제 47강(IS-LM · 재정 · 통화정책) 기출 · 문장 · 개념정리 추가"]],
  ["1.9.17", "2026.11.18", ["회계 35회 69번(전항 정답)에도 정답 처리 사유 추가"]],
  ["1.9.16", "2026.11.18", ["전항 · 복수 정답 6문항 해설에 '⚠️ 정답 처리 사유'(문제의 어느 부분이 오류인지) 추가"]],
  ["1.9.15", "2026.11.18", ["10개년 최종정답표로 회계 · 경제 기출 전체 정답 대조 → 모두 '공식' 정답으로 표시", "전항 정답 문항 반영: 회계 31회 67번, 경제 30회 79번 · 36회 50번 · 37회 52번"]],
  ["1.9.14", "2026.11.18", ["회계 22단원(회계변경 · 오류수정) · 23단원(주당이익), 경제 44강(승수 · 대부자금 · 화폐) 기출 · 문장 · 개념정리 추가"]],
  ["1.9.13", "2026.11.18", ["회계 21단원(법인세), 경제 41강(소비 · 투자 이론) 기출 · 문장 · 개념정리 추가"]],
  ["1.9.12", "2026.11.18", ["회계 20단원(리스), 경제 39강(국민소득 · 물가지수) 기출 · 문장 · 개념정리 추가"]],
  ["1.9.11", "2026.11.18", ["홈 버튼을 '📢 업데이트 정보' · '❓ 사용방법' 글자와 함께 표시"]],
  ["1.9.10", "2026.11.18", ["날짜 옆에 1차 시험 D-day 표시(2026년 시험일 4월 4일 기준)", "회계 33회 63번 정답을 ④(₩1,260,000)로 바로잡음(정답표 옮겨 적기 실수)"]],
  ["1.9.9", "2026.11.18", ["홈 제목 옆에 업데이트 정보 · 사용방법 버튼 추가"]],
  ["1.9.8", "2026.11.18", ["회계 18·19단원(종업원급여 · 주식기준보상), 경제 35강(시장실패) 기출 · 문장 · 개념정리 추가", "회계 33회 63번 해설 정리"]],
  ["1.9.2~1.9.7", "2026.11.17", ["회계 12~17단원(금융자산 · 사채 · 전환사채 · 충당부채 · 자본 · 수익) 기출 · 문장 · 개념정리 추가", "경제 22~34강(비용이론 · 완전경쟁 · 독점 · 과점 · 요소시장 · 후생경제) 기출 · 문장 · 개념정리 추가"]],
  ["1.9.1", "2026.11.17", ["경제 오늘의 문제를 기출만으로(보충 문제 제외)", "문장 훈련: 문제 상황 자동 표시, 📜 원래 문제 보기, 🤔 상황이 부족해요 표시"]],
  ["1.9.0", "2026.11.17", ["개념정리도 진도까지만 보이게(안 배운 단원은 🔒)", "회계 11단원(현금 · 수취채권), 경제 21강(규모수익) 추가"]],
  ["1.8.0~1.8.1", "2026.11.16", ["회계 문장 훈련 추가, 오늘의 문제는 기출만 10문제", "오늘의 문장 20개로"]],
  ["1.7.0", "2026.11.16", ["경제 문장 훈련(기출 지문 O·X 해석) 추가"]],
  ["1.6.0", "2026.11.16", ["해설을 문제와 함께 보기"]],
  ["1.5.0~1.5.3", "2026.11.15", ["합격노트(저장 · 분류 · 메모 · 다시 풀기) 추가, 진도 버튼을 공부하기 · 도전하기 줄로", "제한시간 리셋 오류 수정, 경제 20강(기대효용) 반영"]],
  ["1.4.0~1.4.1", "2026.11.15", ["게임형 화면: 레벨 · 진도 점 · 별 · 연속 · 배지 · 콤보, 🌙/☀️ 전환", "휴대폰 강제 어둡게 모드에 덮이던 문제 수정"]],
];
const HELP = () => [
  ["🏠 홈", "과목 카드마다 오늘 진행, 🔥 연속 일수, 정답률, 오답 수, 합격노트 수가 보여요. Lv. 숫자를 누르면 진도를 바꿀 수 있어요."],
  ["🗺️ 진도 맞추기", "인강에서 들은 강(단원)까지 Lv.을 올려 두세요. 문제 · 문장 · 개념정리 모두 그 진도까지만 나와요. 안 배운 부분은 🔒로 잠겨요."],
  ["📖 공부하기", "개념정리. 결론 한 줄 → 시험에서 묻는 방식 → 표 · 그래프(슬라이더로 숫자 바꿔 보기) → 자주 틀리는 지점 → 버려도 되는 주제 순서예요."],
  ["⚔️ 도전하기", `오늘의 문제 ${DAILY_N}문제 · 문제당 ${SEC_PER_Q}초. 매일 자정(한국시간)에 바뀌어요. 다 풀면 추가 문제도 풀 수 있어요.`],
  ["🧩 단원별 · ❌ 오답", "단원별은 원하는 단원 기출만 모아 풀기(별 3개 → 👑). 오답 탭에서 틀린 문제를 다시 풀면 맞힐 때 빠져요."],
  ["📒 합격노트", "해설 화면에서 저장한 문제를 분류 · 메모와 함께 모아 두고 다시 풀어요."],
  ["📝 문장 훈련", `기출 지문 한 줄을 O·X로 판단하고 쉬운 말 풀이 · 용어 · 고친 문장을 봐요. 하루 ${SENT_N}개. 상황이 부족하면 📜 원래 문제 보기, 그래도 모르겠으면 🤔 표시 후 목록을 복사해 Claude에게 보내 주세요.`],
  ["☁️ 동기화", "설정에서 한 번 연결하면 휴대폰과 PC 기록이 이어져요. 연결 전에는 이 기기에만 저장돼요."],
  ["💬 Claude에게 부탁하기", "\"회계 ○단원 들었어\" · \"경제 ○강까지 들었어\"라고 말하면 그 범위 기출 · 문장 · 개념정리를 추가해요. 해설이 이상하면 문제 번호(예: 33-63)와 함께 알려 주세요."],
];
function openInfo(kind) {
  const box = $("#infoSheet");
  if (kind === "news") {
    localStorage.setItem(LS_SEENVER, APP_VER);
    box.innerHTML = `<h2 id="infoTitle">📢 업데이트 정보</h2><p class="exp">지금 버전 v${APP_VER}</p>` + NEWS.map(([v, d, items], i) => `<div class="news${i ? "" : " cur"}"><div class="nh"><b>v${v}</b><small>${d}</small></div><ul>${items.map(t => `<li>${esc2(t)}</li>`).join("")}</ul></div>`).join("");
  } else {
    box.innerHTML = `<h2 id="infoTitle">❓ 사용방법</h2>` + HELP().map(([h, t]) => `<div class="news"><div class="nh"><b>${h}</b></div><p>${esc2(t)}</p></div>`).join("");
  }
  box.insertAdjacentHTML("beforeend", `<div class="row" style="justify-content:center"><button class="btn" id="infoClose">닫기</button></div>`);
  $("#infoClose").onclick = closeInfo; $("#info").hidden = false; $("#infoClose").focus({ preventScroll: true }); box.scrollTop = 0;
  if (V.route === "home") drawInfoBtns();
}
function closeInfo() { $("#info").hidden = true }
function drawInfoBtns() {
  const nw = localStorage.getItem(LS_SEENVER) !== APP_VER;
  $("#title").innerHTML = `<span class="tt">오늘의 공부</span><span class="tbtns"><button class="tbtn${nw ? " dot" : ""}" id="newsBtn"${nw ? ' aria-label="업데이트 정보 (새 소식 있음)"' : ""}><span aria-hidden="true">📢</span> 업데이트 정보</button><button class="tbtn" id="helpBtn"><span aria-hidden="true">❓</span> 사용방법</button></span>`;
  $("#newsBtn").onclick = () => openInfo("news"); $("#helpBtn").onclick = () => openInfo("help");
}
$("#info").addEventListener("click", e => { if (e.target.id === "info") closeInfo() });
document.addEventListener("keydown", e => { if (e.key === "Escape" && !$("#info").hidden) closeInfo() });

/* ───────── 홈 ───────── */
function renderHome() {
  chrome({ eyebrow: "감정평가사 1차 · 문제풀이", title: "오늘의 공부", meta: `<span>${dateLabel()}</span>` });
  drawInfoBtns();
  const bl = badgeList(), got = bl.filter(b => b.ok).length;
  const best = Math.max(0, ...SUBJ.map(s => streak(s.id)));
  const tot = SUBJ.reduce((a, s) => { const sm = summary(s.id); a.d += sm.done; a.t += sm.total; return a }, { d: 0, t: 0 });
  const cards = SUBJ.map(s => {
    const sm = summary(s.id), st = streak(s.id), wr = wrongList(s.id).length, m = D[s.id].meta, L = lecOf(s.id), ac = accOf(s.id);
    const done = sm.done >= sm.total, state = !sm.started ? "오늘 시작 전" : done ? "클리어! 🎉" : `${sm.done}/${sm.total} 진행 중`;
    const nx = m.lectures[L];
    return `<div class="scard" data-s="${s.id}">
      <div class="row1"><span class="semo" aria-hidden="true">${emoOf(s.id)}</span><span class="ttl"><h2>${m.name}</h2><span class="sub">${m.teacher} ${m.course}</span></span><button class="lvl" data-go="map" aria-label="진도 바꾸기 · 지금 Lv.${L}">Lv.<b>${L}</b><small>/${m.lectures.length}</small></button></div>
      ${pathDots(s.id)}
      <div class="cap">📍 ${esc2(lecLabel(s.id, L))}${nx ? `<span>다음 ▶ ${esc2(m.stepLabel === "강" ? L + 1 + "강" : nx)}</span>` : ""}</div>
      <div class="today">${starRow(Math.floor(sm.done / Math.max(1, sm.total) * 5), 5)}<span>오늘 <b>${sm.done}</b>/${sm.total}${sm.done ? ` · 맞힘 ${sm.ok}` : ""}</span></div>
      <div class="chips"><span class="chip ${st ? "fire" : ""}">🔥 ${st}일 연속</span><span class="chip">🎯 정답률 ${ac.s ? ac.p + "%" : "–"}</span><span class="chip ${wr ? "bad" : ""}">❌ 오답 ${wr}</span><span class="chip">📒 합격노트 ${bookList(s.id).length}</span></div>
      <div class="two"><button data-go="note">📖 공부하기<small>${m.notes ? "개념정리" : "준비 중"}</small></button><button class="main ${done ? "clear" : ""}" data-go="daily">⚔️ 도전하기<small>${state}</small></button></div>
    </div>`;
  }).join("");
  $("#main").innerHTML = `<div class="hero">
      <div class="hx"><span class="he" aria-hidden="true">🔥</span><b>${best}</b><small>일 연속</small></div>
      <div class="hx"><span class="he" aria-hidden="true">⭐</span><b>${tot.d}</b><small>/${tot.t} 오늘</small></div>
      <a class="hx" href="#badges"><span class="he" aria-hidden="true">🏅</span><b>${got}</b><small>/${bl.length} 배지</small></a>
    </div>
    <div class="subjects">${cards}</div>
    ${syncOn() ? "" : `<div class="warnbox">☁️ 지금은 이 기기에만 기록이 저장돼요. 휴대폰과 PC 기록을 이으려면 <a href="#/settings">설정 → 기기 간 동기화</a>를 한 번 연결해 주세요.</div>`}
    <section class="card" id="badges"><h2 class="sec" style="margin:0">🏅 배지 ${got}/${bl.length}</h2>
      <ul class="badges">${bl.map(b => `<li class="${b.ok ? "got" : ""}"><span class="be" aria-hidden="true">${b.e}</span><b>${b.n}</b><small>${b.ok ? "획득" : b.d}</small></li>`).join("")}</ul></section>
    <div class="row"><a class="btn ghost sm" href="#/settings">⚙️ 설정</a></div>`;
  document.querySelectorAll(".scard button[data-go]").forEach(b => b.onclick = () => go(`#/s/${b.closest(".scard").dataset.s}/${b.dataset.go}`));
  $("#main").querySelector('a[href="#badges"]').onclick = e => { e.preventDefault(); $("#badges").scrollIntoView({ behavior: "smooth" }) };
  $("#foot").textContent = `오늘의 문제는 매일 자정(한국시간)에 새로 바뀌고, 과목마다 ${DAILY_N}문제 · ${DAILY_N * SEC_PER_Q / 60}분입니다. 별은 오늘 푼 비율(★5 = 다 풂), 배지는 지금까지 기록으로 계산합니다.`;
  celebrate();
}
const esc2 = s => String(s).replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

/* ───────── 과목 화면 ───────── */
function render() {
  if (V.route !== "subject") return;
  const sub = V.sub, m = D[sub].meta, L = lecOf(sub);
  const wrN = wrongList(sub).length;
  chrome({
    subject: sub, back: { label: "홈", hash: "#/" }, eyebrow: `감정평가사 1차 · ${m.name} · ${m.teacher} ${m.course}`,
    title: `<span class="temo" aria-hidden="true">${emoOf(sub)}</span>` + (V.mode === "daily" ? `오늘의 ${V.Q.length}문제` : V.mode === "extra" ? `추가 ${V.Q.length}문제` : V.mode === "unit" ? esc2(D[sub].ub[V.unit].nm) : V.mode === "wrong" ? "오답 정리" : V.mode === "book" ? "합격노트 복습" : V.mode === "retry" ? "방금 틀린 문제" : V.tab === "unit" ? "단원별 도전" : V.tab === "wrong" ? "오답 정리" : V.tab === "book" ? "합격노트" : V.tab === "note" ? `${m.name} 개념정리` : V.tab === "sent" ? "문장 훈련" : "진도 설정"),
    meta: `<span>${dateLabel()}</span><span>Lv.${L} · <b>${esc2(lecLabel(sub, L))}</b>까지</span>`, tabs: true, stats: true
  });
  drawSeg();
  if (V.tab === "note") { $("#tabs").hidden = true; $("#stats").hidden = true; return renderNote() }
  if (V.tab === "map") { $("#tabs").hidden = true; $("#stats").hidden = true; return renderMap() }
  if (V.tab === "sent") { $("#tabs").hidden = true; $("#stats").hidden = true; return renderSent() }
  const bkN = bookList(sub).length;
  const tabs = [["daily", "🎯 오늘"], ["unit", "🧩 단원별"], ["wrong", "❌ 오답"], ["book", "📒 합격노트"]];
  $("#tabs").innerHTML = tabs.map(([t, n]) => `<button role="tab" data-t="${t}" aria-selected="${V.tab === t}">${n}${t === "wrong" && wrN ? `<span class="cnt">${wrN}</span>` : t === "book" && bkN ? `<span class="cnt bk">${bkN}</span>` : ""}</button>`).join("");
  $("#tabs").querySelectorAll("button").forEach(b => b.onclick = () => go(`#/s/${sub}/${b.dataset.t}`));
  stats();
  if (V.tab === "unit" && !V.mode) return renderUnitPick();
  if (V.tab === "book" && !V.mode) return renderBookPick();
  if (V.tab === "wrong" && !V.mode) return renderWrongPick();
  renderPlay();
}
function stats() {
  const sub = V.sub, sm = summary(sub), st = streak(sub);
  const ex = D[sub].exam.filter(x => !x.skip && !x.gen), seen = ex.filter(x => S.hist[`${sub}:${x.k}`]).length, wr = wrongList(sub).length;
  const tile = (e, v, u, l, cls = "") => `<span class="st ${cls}"><span class="si" aria-hidden="true">${e}</span><span><b>${v}</b>${u}</span><small>${l}</small></span>`;
  $("#stats").innerHTML = tile("⭐", sm.done, "/" + sm.total, "오늘") + tile("🔥", st, "일", "연속", st ? "fire" : "") + tile("📚", seen, "/" + ex.length, "푼 기출") + tile("❌", wr, "개", "오답", wr ? "warn" : "");
}

/* 단원 노드 (스테이지) */
function mastery(sub, x) {
  const ex = exOfU(sub, x.u), hs = ex.map(q => S.hist[`${sub}:${q.k}`]).filter(Boolean), ok = hs.filter(h => h.ok).length;
  const st = !ex.length || !hs.length ? 0 : hs.length === ex.length && ok / hs.length >= .8 ? 3 : hs.length * 2 >= ex.length && ok / hs.length >= .6 ? 2 : 1;
  return { ex: ex.length, seen: hs.length, ok, wr: hs.length - ok, st };
}
function unitRow(sub, x, withBtn) {
  const m = D[sub].meta, Lr = lecOf(sub), L = Math.min(Lr, m.dataThrough), open = x.lec <= L, ox = oxOfU(sub, x.u).length, ms = mastery(sub, x);
  const lecTxt = m.stepLabel === "강" ? `${x.lec}강~ · ` : `${x.lec}단원 · `;
  const sub2 = x.lec > Lr ? `${lecTxt}아직 수강 전` : !open ? `${lecTxt}수강했지만 기출 추가 전` : ms.ex ? `${lecTxt}${ms.seen}/${ms.ex}문항 풀어 봄${ms.wr ? ` · ❌ ${ms.wr}` : ""}${ox ? ` · O·X ${ox}` : ""}` : `${lecTxt}기출 미수록`;
  const cur = x.lec === Lr, icon = x.lec > Lr ? "🔒" : cur ? "📍" : ms.st === 3 ? "👑" : open ? "✅" : "⏳";
  const lv = lvOf(x.n);
  return `<li class="unit ${x.lec > Lr ? "locked" : "open"} ${cur ? "cur" : ""}"><span class="node" aria-hidden="true">${icon}</span><span class="nm">${esc2(x.nm)}<small>${sub2}</small>${open && ms.ex ? starRow(ms.st, 3) : ""}</span>
   <span class="ct"><span class="lv ${lv === "상" ? "h" : lv === "중" ? "m" : ""}" title="10년간 ${x.n}문항">${lv === "상" ? "🔥" : ""}${lv} ${x.n}</span>${withBtn && open && ms.ex ? `<button data-u="${x.u}">▶ 도전</button>` : ""}</span></li>`;
}
function renderUnitPick() {
  const sub = V.sub, L = Math.min(lecOf(sub), D[sub].meta.dataThrough);
  const list = D[sub].meta.units.filter(x => x.lec <= L);
  $("#main").innerHTML = list.length ? `<ul class="units stage">${list.map(x => unitRow(sub, x, true)).join("")}</ul>` : `<p class="exp">아직 열린 단원이 없어요. '🗺️ 진도'에서 진도를 올려 주세요.</p>`;
  $("#main").querySelectorAll("button[data-u]").forEach(b => b.onclick = () => go(`#/s/${sub}/unit/${b.dataset.u}`));
  $("#foot").textContent = "별 = 그 단원 정복도(★ 풀기 시작 · ★★ 절반 이상 풀고 60% 이상 맞힘 · ★★★ 전부 풀고 80% 이상 맞힘 → 👑). 상·중·하와 숫자 = 제28~37회(10년) 출제 비중(15문항 이상 상, 8~14 중, 7 이하 하). 단원 안에서는 안 푼 문제 → 틀린 문제 → 맞힌 문제 순으로 나옵니다.";
}
function renderWrongPick() {
  const sub = V.sub, list = wrongList(sub);
  if (!list.length) { $("#main").innerHTML = `<section class="card center"><div class="bigemo" aria-hidden="true">✨</div><p class="exp">틀린 채로 남은 문제가 없어요. 다시 풀어서 맞히면 이 목록에서 빠집니다.</p></section>`; return }
  const byU = {};
  for (const x of list) { const u = x.q.t === "ex" ? D[sub].ex[x.q.k].u : D[sub].oxBy[x.q.id].u; byU[u] = (byU[u] || 0) + 1 }
  const mx = Math.max(...Object.values(byU));
  $("#main").innerHTML = `<section class="card center"><div class="bigemo" aria-hidden="true">🧹</div><div class="score">${list.length}<small> 문제</small></div>
    <p class="exp">마지막에 틀린 문제만 모았어요. 여러 번 틀린 문제부터 나오고, 맞히면 목록에서 빠집니다. 제한시간 없음.</p>
    <div class="row" style="justify-content:center"><button class="btn" id="goWrong">⚔️ 오답 ${list.length}문제 정리하기</button></div></section>
    <h2 class="sec">단원별 남은 오답</h2>
    <ul class="units">${D[sub].meta.units.filter(u => byU[u.u]).map(u => `<li class="unit"><span class="nm">${esc2(u.nm)}</span><span class="ct"><span class="bar"><i style="width:${Math.round(byU[u.u] / mx * 100)}%;background:var(--x)"></i></span>❌ ${byU[u.u]}</span></li>`).join("")}</ul>`;
  $("#goWrong").onclick = () => go(`#/s/${sub}/wrong/play`);
}
function renderMap() {
  const sub = V.sub, m = D[sub].meta, L = lecOf(sub), units = m.units;
  const openN = units.filter(x => x.lec <= Math.min(L, m.dataThrough)).reduce((a, b) => a + b.n, 0), all = units.reduce((a, b) => a + b.n, 0);
  const nxt = units.filter(x => x.lec > L).sort((a, b) => a.lec - b.lec)[0];
  const grps = [...new Set(units.map(u => u.grp))], pc = Math.round(openN / all * 100);
  $("#main").innerHTML = `<div class="lec"><button id="lm" aria-label="진도 한 ${m.stepLabel} 빼기">◀</button><span class="num"><span class="lvbig">Lv.${L}<small>/${m.lectures.length}</small></span><b>${esc2(lecLabel(sub, L))}</b></span><button id="lp" aria-label="진도 한 ${m.stepLabel} 더하기">▶</button>
     ${pathDots(sub)}
     <span class="lname">🗺️ 10년 기출 ${all}문항 중 <b>${openN}문항(${pc}%)</b>을 정복할 수 있어요.${nxt ? `<br>다음 스테이지 ▶ ${esc2(nxt.nm)} (10년 ${nxt.n}문항, 비중 ${lvOf(nxt.n)})` : ""}</span></div>
   ${L <= m.dataThrough && units.some(x => x.lec <= L && !exOfU(sub, x.u).length && !oxOfU(sub, x.u).length) ? `<div class="warnbox">⏳ 수강한 단원 중 아직 기출이 들어 있지 않은 단원이 있어요. Claude에게 "${m.name} ○○ 단원 들었어"라고 알려 주시면 그 단원 기출을 해설과 함께 추가합니다. 그 전까지는 문제가 있는 단원에서만 냅니다.</div>` : ""}
   ${L > m.dataThrough ? `<div class="warnbox">⏳ 문제는 ${m.stepLabel === "강" ? m.dataThrough + "강" : esc2(m.lectures[m.dataThrough - 1])}까지 들어 있어요. Claude에게 "${m.name} ${m.stepLabel === "강" ? L + "강" : "○○ 단원"}까지 들었어"라고 알려 주시면 그 범위 기출을 해설과 함께 추가합니다.</div>` : ""}
   ${grps.map(g => { const us = units.filter(u => u.grp === g), n = us.reduce((a, b) => a + b.n, 0); return `<h2 class="sec">${g} · 10년 ${n}문항 (${Math.round(n / all * 100)}%)</h2><ul class="units stage">${us.map(x => unitRow(sub, x, false)).join("")}</ul>` }).join("")}`;
  const step = d => { const nl = Math.max(1, Math.min(m.lectures.length, L + d)); if (nl === L) return; setLec(sub, nl); const e = entry(sub); if (e && !(e.res || []).filter(Boolean).length) delete S.daily[day][sub]; touch(); render(); if (d > 0) celebrate() };
  $("#lm").onclick = () => step(-1); $("#lp").onclick = () => step(1);
  $("#foot").textContent = "📍 지금 진도 · ✅ 열린 단원 · 👑 정복(전부 풀고 80% 이상) · 🔒 수강 전. " + (m.mapNote || "") + " 진도를 바꾸면 아직 한 문제도 안 푼 오늘 세트는 새 범위로 다시 만들어집니다.";
}

/* ───────── 개념정리 ───────── */
function noteOf(sub, q) {
  const m = D[sub].meta; if (!m.notes) return "";
  const u = q.t === "ex" ? D[sub].ex[q.k].u : q.t === "ox" ? D[sub].oxBy[q.id].u : q.u;
  return (D[sub].ub[u] || {}).note || "";
}
function drawSeg() {
  const sub = V.sub, m = D[sub].meta, sm = summary(sub), seg = $("#seg"); seg.hidden = false;
  const cur = V.tab === "note" ? "note" : V.tab === "map" ? "map" : V.tab === "sent" ? "sent" : "daily", hasS = sentOpen(sub).length > 0;
  seg.classList.toggle("four", hasS);
  seg.innerHTML = `<button role="tab" aria-selected="${cur === "note"}" data-go="note">📖 공부하기<small>${m.notes ? "개념정리" : "준비 중"}</small></button><button role="tab" aria-selected="${cur === "daily"}" data-go="daily">⚔️ 도전하기<small>오늘 ${sm.done}/${sm.total}</small></button>${hasS ? `<button role="tab" aria-selected="${cur === "sent"}" data-go="sent">📝 문장 훈련<small>O·X 해석</small></button>` : ""}<button role="tab" aria-selected="${cur === "map"}" data-go="map">🗺️ 진도<small>Lv.${lecOf(sub)} 바꾸기</small></button>`;
  seg.querySelectorAll("button").forEach(b => b.onclick = () => { if (b.dataset.go !== cur) go(`#/s/${sub}/${b.dataset.go}`) });
}
/* 문제풀이에서 빠진 개념 O·X(★개념문제)의 예전 풀이 기록을 문장 훈련 기록으로 이어 준다 (한 번만, 이미 있으면 그대로) */
function migrateOxToSent() {
  let n = 0;
  for (const s of SUBJ) for (const b of D[s.id].sent || []) {
    if (!b.ox) continue;
    const h = S.hist[`${s.id}:ox${b.ox}`], k = `${s.id}:s${b.id}`;
    if (h && !S.sent[k]) { S.sent[k] = { seen: h.seen || 1, wrong: h.wrong || 0, ok: h.ok, last: h.last, t: h.t || Date.now() }; n++ }
  }
  if (n) saveLocal();
}
/* ───────── 문장 훈련 (문제풀이와 별개: 기록은 S.sent, 오늘의 문제·배지·통계에 안 섞임) ───────── */
const LS_SENT = "dora-exam-sent";
const SENT_N = 20;               // 오늘의 문장 수 (과목별)
const sid = (sub, b) => `${sub}:s${b.id}`;
function sentOpen(sub) { const us = new Set(openUnits(sub).map(u => u.u)); return (D[sub].sent || []).filter(b => us.has(b.u)) }
const sentH = (sub, b) => (S.sent || {})[sid(sub, b)];
function sentCur(sub) { try { const x = JSON.parse(localStorage.getItem(LS_SENT)) || {}; return x[sub] || null } catch (e) { return null } }
function sentSave(sub, c) { try { const x = JSON.parse(localStorage.getItem(LS_SENT)) || {}; if (c) x[sub] = c; else delete x[sub]; localStorage.setItem(LS_SENT, JSON.stringify(x)) } catch (e) { } }
function sentBuild(sub, kind) {
  const all = sentOpen(sub), r = rng(sub + day + kind + (kind === "today" ? "" : Math.random()));
  if (kind === "wrong") return shuffle(all.filter(b => { const h = sentH(sub, b); return h && !h.ok }), r).map(b => b.id);
  if (kind.startsWith("u-")) { const u = kind.slice(2); return all.filter(b => b.u === u).map(b => b.id) }
  /* 오늘의 문장 SENT_N개: 안 본 문장 → 헷갈린 문장 → 익힌 지 오래된 문장 */
  const rank = b => { const h = sentH(sub, b); return !h ? 0 : !h.ok ? 1 : 2 };
  return shuffle(all.slice(), r).sort((a, b) => rank(a) - rank(b) || (rank(a) === 2 ? (sentH(sub, a).t - sentH(sub, b).t) : 0)).slice(0, SENT_N).map(b => b.id);
}
function renderSent() {
  const sub = V.sub, m = D[sub].meta, all = sentOpen(sub);
  $("#eyebrow").hidden = true;
  if (!all.length) { $("#main").innerHTML = `<section class="card"><p class="exp">${m.name}은 아직 문장 훈련이 없어요.</p></section>`; return }
  const by = Object.fromEntries((D[sub].sent || []).map(b => [b.id, b]));
  let c = sentCur(sub);
  if (V.arg && V.arg !== "home") {
    if (!c || c.kind !== V.arg || (V.arg === "today" && (c.day !== day || (!c.res.length && c.Q.length < Math.min(SENT_N, sentOpen(sub).length))))) { c = { kind: V.arg, day, Q: sentBuild(sub, V.arg), idx: 0, res: [] }; sentSave(sub, c) }
    c.Q = c.Q.filter(id => by[id]);
    if (!c.Q.length) { sentSave(sub, null); return go(`#/s/${sub}/sent`) }
    return c.idx >= c.Q.length ? sentEnd(sub, c, by) : sentCard(sub, c, by);
  }
  const hs = all.map(b => sentH(sub, b)), ok = hs.filter(h => h && h.ok).length, wr = hs.filter(h => h && !h.ok).length;
  const us = openUnits(sub).map(u => ({ u, n: all.filter(b => b.u === u.u) })).filter(x => x.n.length);
  const resume = c && c.idx < c.Q.length && c.res.length && !(c.kind === "today" && c.day !== day);
  const fl = (sflagGet()[sub] || []).filter(id => by[id]);
  $("#main").innerHTML = `<section class="card center"><div class="bigemo" aria-hidden="true">📝</div>
    <p class="exp">기출 지문을 한 문장씩 쪼갰어요. <b>문장이 무슨 말인지</b> 먼저 읽고, 맞는 말인지 O·X로 골라 보세요. 막히면 <b>🗣️ 쉬운 말로 보기</b>를 누르면 됩니다. 여기 기록은 문제풀이 점수에 섞이지 않아요.</p>
    <p class="answer">열린 문장 <b>${all.length}</b> · 익힘 <b>${ok}</b> · 헷갈림 <b>${wr}</b></p>
    <div class="row" style="justify-content:center;flex-wrap:wrap;gap:8px">
      ${resume ? `<button class="btn" data-k="${c.kind}">↩️ 하던 것 이어서 (${c.res.length}/${c.Q.length})</button>` : ""}
      <button class="btn ${resume ? "ghost" : ""}" data-k="today">▶ 오늘의 문장 ${Math.min(SENT_N, all.length)}개</button>
      ${wr ? `<button class="btn ghost" data-k="wrong">🔁 헷갈린 문장 ${wr}개</button>` : ""}</div></section>
    ${fl.length ? `<section class="card"><p class="exp">🤔 <b>상황이 부족하다고 표시한 문장 ${fl.length}개</b> · Claude에게 아래 문구를 보내면 문제 상황을 보강해 드려요.</p><p class="fix" id="flagTxt">${m.name} 문장 상황 보강해줘: ${fl.map(i => "s" + i).join(", ")}</p><div class="row" style="gap:8px;flex-wrap:wrap"><button class="btn ghost sm" id="flagCopy">📋 문구 복사</button><button class="btn ghost sm" id="flagClear">표시 모두 지우기</button></div></section>` : ""}
    <h2 class="sec">단원별</h2>
    <ul class="units">${us.map(({ u, n }) => { const o = n.filter(b => { const h = sentH(sub, b); return h && h.ok }).length; return `<li class="unit open"><span class="nm">${esc2(u.nm)}<small>${n.length}문장 중 ${o}개 익힘</small></span><span class="ct"><span class="bar"><i style="width:${Math.round(o / n.length * 100)}%"></i></span><button data-k="u-${u.u}">▶ 훈련</button></span></li>` }).join("")}</ul>`;
  $("#main").querySelectorAll("button[data-k]").forEach(b => b.onclick = () => {
    const k = b.dataset.k, cc = sentCur(sub);
    if (!(resume && cc && cc.kind === k && b.textContent.includes("이어서"))) sentSave(sub, { kind: k, day, Q: sentBuild(sub, k), idx: 0, res: [] });
    go(`#/s/${sub}/sent/${k}`);
  });
  if ($("#flagCopy")) $("#flagCopy").onclick = () => { const t = $("#flagTxt").textContent; (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(() => toast("복사했어요"), () => toast("길게 눌러 직접 복사해 주세요")) };
  if ($("#flagClear")) $("#flagClear").onclick = () => { const f = sflagGet(); delete f[sub]; try { localStorage.setItem(LS_SFLAG, JSON.stringify(f)) } catch (e) { } renderSent() };
  $("#foot").textContent = "익힘 = 마지막에 맞힌 문장, 헷갈림 = 마지막에 틀린 문장. 오늘의 문장은 안 본 문장 → 헷갈린 문장 → 오래전에 익힌 문장 순으로 뽑습니다. 진도를 올리면 그 단원 문장이 열립니다.";
}
/* 문장의 원래 기출 문제(k)와 자동 상황 문구 */
const sentSrcK = b => { const m = /^(\d+)회 (\d+)번/.exec(b.src || ""); return m ? `${m[1]}-${m[2]}` : "" };
const sentSrcQ = (sub, b) => { const k = sentSrcK(b); return k && D[sub].ex[k] ? D[sub].ex[k] : null };
function sentCtx(sub, b) {
  if (b.ctx) return b.ctx;
  const x = sentSrcQ(sub, b); if (!x) return "";
  let t = plain(x.q).replace(/\s*\(단,[^)]*\)\s*$/, "").replace(/\s*(으로|로)?\s*(옳은|옳지 않은|가장 옳은)\s*것(을 모두 고른 것|만을 모두 고른 것)?은\s*\?\s*$/, "").replace(/[,\s]*(아래|다음)?\s*(설명|내용)?\s*중\s*$/, "").trim();
  if (t === plain(x.q).trim()) t = t.replace(/\?$/, "");
  return esc2(t.length > 140 ? t.slice(0, 140) + "…" : t);
}
/* 상황이 부족한 문장 표시(이 기기에만 저장 → Claude에게 번호를 알려 주면 보강) */
const LS_SFLAG = "dora-exam-sentflag";
function sflagGet() { try { return JSON.parse(localStorage.getItem(LS_SFLAG)) || {} } catch (e) { return {} } }
function sflagToggle(sub, id) { const f = sflagGet(), a = new Set(f[sub] || []); a.has(id) ? a.delete(id) : a.add(id); f[sub] = [...a].sort((x, y) => x - y); try { localStorage.setItem(LS_SFLAG, JSON.stringify(f)) } catch (e) { } return a.has(id) }
function sentOrigHtml(sub, b) {
  const x = sentSrcQ(sub, b); if (!x) return "";
  return `<div class="orig" id="orig" hidden><p class="ohead">📜 제${x.y}회 ${x.n}번 원래 문제</p><p class="stem">${x.q}</p>
    ${x.fig ? `<div class="fig">${x.fig}</div>` : ""}
    ${x.tbl ? `<div class="tblw"><table class="tbl">${x.tbl.map((r, i) => `<tr>${r.map(c => i ? `<td>${c}</td>` : `<th>${c}</th>`).join("")}</tr>`).join("")}</table></div>` : ""}
    ${x.box ? `<div class="box">${x.box.map(t => `<p>${t.t}</p>`).join("")}</div>` : ""}
    ${x.box ? "" : `<ol class="oopts">${x.o.map((t, i) => `<li><span>${N5[i]}</span> ${t}</li>`).join("")}</ol>`}</div>`;
}
const srcTag = b => b.src === "보충" ? "✏️ 보충" : b.src === "개념문제" ? "📘 개념문제" : "📜 " + b.src;
function srcLine(b) {
  if (b.src === "보충") return "📜 출처 · 보충 문장(기출 아님)";
  if (b.src === "개념문제") return "📘 출처 · ★개념문제 파일" + (b.links && b.links.length ? " · 기출에 나온 곳: " + b.links.map(l => { const [k, o] = l.split(" "), [y, n] = k.split("-"); return `${y}회 ${n}번${o ? " " + o : ""}` }).join(", ") : "");
  return "📜 출처 · 제" + b.src;
}
function sentCard(sub, c, by) {
  const b = by[c.Q[c.idx]], un = D[sub].ub[b.u] || {}, r = c.res[c.idx];
  const terms = (b.terms || []).map(([t, d]) => `<li><b>${t}</b> · ${d}</li>`).join("");
  const ctx = sentCtx(sub, b), orig = sentOrigHtml(sub, b), flagged = (sflagGet()[sub] || []).includes(b.id);
  $("#main").innerHTML = `<section class="card q sent">
    <div class="qhead"><span class="qno">문장 ${c.idx + 1} / ${c.Q.length} <small class="sidno">s${b.id}</small></span><span class="tags"><span class="tag">${esc2(un.nm || "")}</span><span class="tag exb">${srcTag(b)}</span></span></div>
    ${ctx ? `<p class="ctx">📌 <b>문제 상황</b> · ${ctx}</p>` : ""}
    <p class="stem">${b.s}</p>
    <div class="row sbtns"><button class="hintbtn" id="plainBtn" ${r ? "hidden" : ""}>🗣️ 쉬운 말로 보기</button>${orig ? `<button class="hintbtn" id="origBtn">📜 원래 문제 보기</button>` : ""}<button class="hintbtn flag ${flagged ? "on" : ""}" id="flagBtn" aria-pressed="${flagged}">🤔 ${flagged ? "상황 부족 표시됨" : "상황이 부족해요"}</button></div>
    ${orig}
    <div class="plain" id="plain" ${r ? "" : "hidden"}><p><b>쉬운 말로 바꾸면</b> ${b.plain}</p>${terms ? `<ul>${terms}</ul>` : ""}</div>
    <div class="ox"><button data-v="1" class="o" aria-label="O 맞는 말">O<small>맞는 말</small></button><button data-v="0" class="x" aria-label="X 틀린 말">X<small>틀린 말</small></button></div>
    <div id="sfb"></div></section>
    <div class="qnav"><button class="btn ghost" id="sHome">◀ 목록</button><button class="btn" id="sNext" ${r ? "" : "hidden"}>${c.idx + 1 < c.Q.length ? "다음 문장 ▶" : "결과 보기 ▶"}</button></div>`;
  const fb = (v, ok) => {
    $("#plainBtn").hidden = true; $("#plain").hidden = false;
    $("#main").querySelectorAll(".ox button").forEach(x => { x.disabled = true; const xv = x.dataset.v === "1"; x.classList.add(xv === b.a ? "is-key" : xv === v ? "is-picked" : "is-dim") });
    $("#sfb").innerHTML = `<p class="answer">${ok ? "✅" : "❌"} 정답 <b>${b.a ? "O" : "X"}</b> · 내 답 <b>${v ? "O" : "X"}</b></p><p class="exp">${b.e}</p>
      ${!b.a && b.fix ? `<p class="fix">✅ <b>바르게 고치면</b> · ${b.fix}</p>` : ""}
      <p class="point">${srcLine(b)}${un.note && D[sub].meta.notes ? ` · <a href="#/s/${sub}/note/${un.note}">📖 개념정리에서 보기</a>` : ""}</p>`;
    $("#sNext").hidden = false;
  };
  if (r) fb(r.v, r.ok);
  if ($("#origBtn")) $("#origBtn").onclick = () => { const o = $("#orig"); o.hidden = !o.hidden; $("#origBtn").textContent = o.hidden ? "📜 원래 문제 보기" : "📜 원래 문제 접기" };
  $("#flagBtn").onclick = () => { const on = sflagToggle(sub, b.id); $("#flagBtn").classList.toggle("on", on); $("#flagBtn").setAttribute("aria-pressed", on); $("#flagBtn").textContent = on ? "🤔 상황 부족 표시됨" : "🤔 상황이 부족해요"; toast(on ? "표시했어요. 문장 훈련 목록에서 모아 볼 수 있어요" : "표시를 지웠어요") };
  $("#plainBtn").onclick = () => { $("#plain").hidden = false; $("#plainBtn").hidden = true; c.peek = c.peek || []; c.peek[c.idx] = 1; sentSave(sub, c) };
  $("#main").querySelectorAll(".ox button").forEach(x => { if (!r) x.onclick = () => {
    const v = x.dataset.v === "1", ok = v === b.a, k = sid(sub, b), h = Object.assign({ seen: 0, wrong: 0 }, (S.sent = S.sent || {})[k]);
    h.seen++; if (!ok) h.wrong++; h.ok = ok; h.last = day; h.t = Date.now(); S.sent[k] = h; touch();
    c.res[c.idx] = { v, ok }; sentSave(sub, c); fb(v, ok);
  } });
  $("#sNext").onclick = () => { c.idx++; sentSave(sub, c); renderSent(); scrollTo({ top: 0 }) };
  $("#sHome").onclick = () => go(`#/s/${sub}/sent`);
  $("#foot").textContent = "읽는 순서: ① 문장을 끝까지 읽고 주어·결론을 찾기 → ② 모르는 말이 있으면 🗣️ 쉬운 말로 보기 → ③ O·X. 틀려도 괜찮아요. 해설과 '바르게 고치면' 문장을 소리 내어 한 번 읽으면 됩니다.";
}
function sentEnd(sub, c, by) {
  const ok = c.res.filter(x => x && x.ok).length, n = c.Q.length, bad = c.Q.filter((id, i) => c.res[i] && !c.res[i].ok);
  $("#main").innerHTML = `<section class="card center"><div class="bigemo" aria-hidden="true">${ok === n ? "🏆" : ok * 2 >= n ? "👏" : "💪"}</div><div class="score">${ok}<small> / ${n}</small></div>
    <p class="exp">${ok === n ? "전부 맞혔어요!" : "틀린 문장은 '헷갈린 문장'에 모여 있어요. 내일 한 번 더 보면 확 줄어듭니다."}</p>
    ${bad.length ? `<ul class="ol">${bad.map(id => { const b = by[id]; return `<li><span class="k ${b.a ? "t" : "f"}">${b.a ? "O" : "X"}</span><span>${b.a ? b.s : b.fix || b.s}</span></li>` }).join("")}</ul>` : ""}
    <div class="row" style="justify-content:center;gap:8px;flex-wrap:wrap"><button class="btn" id="sBack">목록으로</button>${bad.length ? `<button class="btn ghost" id="sRe">🔁 틀린 ${bad.length}개 다시</button>` : ""}</div></section>`;
  $("#sBack").onclick = () => { sentSave(sub, null); go(`#/s/${sub}/sent`) };
  if ($("#sRe")) $("#sRe").onclick = () => { sentSave(sub, { kind: "wrong", day, Q: bad, idx: 0, res: [] }); V.key = ""; go(`#/s/${sub}/sent/wrong`) };
}
function renderNote() {
  const sub = V.sub, m = D[sub].meta;
  $("#eyebrow").hidden = true; $("#meta").hidden = true;
  if (!m.notes) {
    $("#main").innerHTML = `<section class="card"><p class="exp">${m.name} 개념정리는 아직 없어요.</p><p class="exp" style="font-size:14.5px">Claude에게 "${m.name} 개념정리 만들어 줘"라고 하면 경제학 요약노트처럼 단원마다 <b>결론 한 줄 → 도식 → 자주 틀리는 지점 → 관련 기출 → 내 오답</b> 순서로 만들어 이 자리에 넣습니다.</p><div class="row"><button class="btn" id="toPlay">문제풀이로 가기</button></div></section>`;
    $("#toPlay").onclick = () => go(`#/s/${sub}/daily`); return;
  }
  $("#main").innerHTML = ""; $("#main").hidden = true; document.body.classList.add("noting");
  const box = $("#notebox"), fr = $("#noteFrame"); box.hidden = false;
  const want = m.notes + (V.arg ? "#" + V.arg : "");
  if (fr.dataset.src !== want) { fr.dataset.src = want; fr.onload = () => enhanceNote(sub); fr.src = want }
  else enhanceNote(sub);
  fitNote();
}
function fitNote() {
  const box = $("#notebox"); if (box.hidden) return;
  scrollTo({ top: 0 });
  const top = box.getBoundingClientRect().top;
  $("#noteFrame").style.height = Math.max(320, innerHeight - top) + "px";
}
addEventListener("resize", () => fitNote());
/* 노트 안에 '내 기록'과 '이 주제 기출 풀기'를 지금 기록으로 채운다 (같은 주소라 노트 화면을 직접 고칠 수 있음) */
function enhanceNote(sub) {
  let doc; try { doc = $("#noteFrame").contentDocument } catch (e) { return }
  if (!doc || !doc.body) return;
  setThemeOn(doc);
  if (!doc.getElementById("appStyle")) {
    const st = doc.createElement("style"); st.id = "appStyle";
    st.textContent = `[hidden]{display:none!important}header .eyebrow,header h1{display:none}.appgo{display:flex;flex-wrap:wrap;gap:8px;margin:4px 0 0}.appgo button{font:500 14px var(--f-body);padding:8px 14px;border-radius:8px;border:1px solid var(--accent);background:var(--accent);color:var(--accent-ink);cursor:pointer}.appgo button.gh{background:transparent;color:var(--accent)}`;
    doc.head.appendChild(st);
  }
  const units = D[sub].meta.units, bySec = {};
  units.forEach(u => { if (u.note) (bySec[u.note] = bySec[u.note] || []).push(u.u) });
  const rec = us => {
    const ex = D[sub].exam.filter(x => us.includes(x.u) && !x.skip);
    const seen = ex.filter(x => S.hist[`${sub}:${x.k}`]), ok = seen.filter(x => S.hist[`${sub}:${x.k}`].ok);
    const wrong = seen.filter(x => S.hist[`${sub}:${x.k}`].ok === false);
    return { ex, seen: seen.length, ok: ok.length, wrong };
  };
  const ask = doc.querySelector("#map .ask"); if (ask) ask.innerHTML = "숫자 = 10년간 출제 문항 수. <b>내 기록</b> = 문제풀이에서 푼 문제 중 마지막에 맞힌 수 / 푼 문제 수 (지금 기록 기준).";
  doc.querySelectorAll("#mapBody tr").forEach(tr => {
    const a = tr.querySelector("a[href^='#']"), us = a && bySec[a.getAttribute("href").slice(1)];
    if (!us) return; const r = rec(us), td = tr.lastElementChild;
    td.textContent = r.seen ? `${r.ok}/${r.seen}` : r.ex.length ? "아직 안 풂" : "문제 없음";
  });
  /* 수강 진도 이후 단원은 숨김: 섹션 · 목차 링크 · 빈출 지도 행 · 암기카드 행(data-sec) */
  const L = lecOf(sub), hid = [];
  /* 섹션이 data-lec을 가지면 그 강부터 공개(단원 첫 강의 내용이 섹션에 먼저 들어간 경우) */
  const lecOfSec = sec => { const el = doc.getElementById(sec), o = el && +el.dataset.lec; return o || Math.min(...bySec[sec].map(u => D[sub].ub[u].lec)) };
  for (const sec of Object.keys(bySec)) {
    const off = lecOfSec(sec) > L; if (off) hid.push(sec);
    const el = doc.getElementById(sec); if (el) el.hidden = off;
    doc.querySelectorAll(`nav a[href="#${sec}"], #mapBody tr a[href="#${sec}"], [data-sec="${sec}"]`).forEach(a => { const row = a.closest("tr") || a; row.hidden = off; if (a.tagName === "A" && !a.closest("tr")) a.hidden = off });
  }
  let ban = doc.getElementById("lockNote");
  if (!ban) { ban = doc.createElement("p"); ban.id = "lockNote"; ban.className = "ask"; const h = doc.querySelector("header"); h && h.after(ban) }
  ban.hidden = !hid.length;
  ban.innerHTML = hid.length ? `🔒 아직 수강 전인 단원 ${hid.length}개는 숨겨 두었어요. 🗺️ 진도를 올리면 그 단원 개념정리가 열립니다.` : "";
  for (const [sec, us] of Object.entries(bySec)) {
    const el = doc.getElementById(sec); if (!el || el.hidden) continue;
    const r = rec(us), mine = el.querySelector(".mine");
    const lab = x => x.gen ? "보충 문제" : `${x.y}회 ${x.n}번`;
    if (mine) mine.innerHTML = r.wrong.length ? `내 오답 ${r.wrong.map(x => `<span>${lab(x)}</span>`).join("")}` : r.seen ? `내 오답 없음 · ${r.seen}문항 풀어 봄` : "아직 푼 문제 없음";
    let go = el.querySelector(".appgo"); if (!go) { go = doc.createElement("p"); go.className = "appgo"; el.appendChild(go) }
    const withQ = us.filter(u => exOfU(sub, u).length);
    go.innerHTML = withQ.map((u, i) => `<button data-u="${u}" class="${i ? "gh" : ""}">${withQ.length > 1 ? esc2(D[sub].ub[u].nm) + " · " : "이 주제 "}기출 ${exOfU(sub, u).length}문항 풀기 →</button>`).join("");
    go.querySelectorAll("button").forEach(b => b.onclick = () => go2(`#/s/${sub}/unit/${b.dataset.u}`));
  }
}
const go2 = h => go(h);

/* ───────── 풀이 ───────── */
function progressNav() {
  const pg = $("#progress"); pg.hidden = false;
  pg.innerHTML = V.Q.map((_, i) => `<button data-j="${i}" class="${V.res[i] ? (V.res[i].ok ? "ok" : "ng") : ""} ${i === V.idx ? "cur" : ""}" aria-label="${i + 1}번${V.res[i] ? (V.res[i].ok ? " 맞음" : " 틀림") : " 안 품"}">${i + 1}</button>`).join("");
  pg.querySelectorAll("button").forEach(b => b.onclick = () => { if (tmPaused()) return; V.idx = +b.dataset.j; render(); scrollTo({ top: 0 }) });
}
function renderPlay() {
  const sub = V.sub, m = $("#main");
  if (V.mode === "daily") V.entryRef = entry(sub);
  $("#foot").textContent = V.mode === "daily" || V.mode === "extra"
    ? `수강한 단원에 10년 출제 비율대로 나눠 냅니다. 단원 안에서는 안 푼 문제 → 틀린 문제 → 오래 안 본 문제 순으로 더 자주 나와요. 제한시간은 문제당 1분이고, 다른 화면으로 나가면 자동으로 멈춥니다.`
    : `정답은 모두 회차별 최종정답 기준이에요. 전항 정답·복수 정답 문항은 해당 보기를 모두 정답으로 인정해요.`;
  if (!V.Q.length) { m.innerHTML = `<section class="card"><p class="exp">풀 문제가 없어요. 진도를 확인해 주세요.</p></section>`; return }
  if (answered() >= V.Q.length || V.idx >= V.Q.length) { tmStop(); saveTimer(); tmDraw(); return result() }
  if (V.idx < 0) V.idx = nextUn(-1);
  progressNav();
  if (tmPaused()) {
    tmDraw();
    m.innerHTML = `<section class="card center"><div class="bigemo" aria-hidden="true">⏸️</div><div class="qhead" style="justify-content:center"><span class="qno">일시정지</span><span class="tag">${answered()} / ${V.Q.length} 풀이</span></div>
      <p class="exp">문제는 가려 두었어요. 남은 시간 <b>${fmt(Math.max(0, tmLimit() - tmUsed()))}</b>${tmLimit() < tmUsed() ? " (제한시간 초과)" : ""} 그대로 멈춰 있습니다.</p>
      <div class="row"><button class="btn" id="resume">▶ 이어서 풀기</button></div></section>`;
    $("#resume").onclick = () => { T.paused = false; tmGo(); saveTimer(); render() }; return;
  }
  if (timed()) tmGo(); tmDraw();
  const q = V.Q[V.idx], no = `Q${String(V.idx + 1).padStart(2, "0")} / ${V.Q.length}`;
  let html;
  if (q.t === "ox") {
    const b = D[sub].oxBy[q.id], un = D[sub].ub[b.u];
    html = `<section class="card q"><div class="qhead"><span class="qno">${no}</span><span class="tags"><span class="tag">⭕ O·X · ${esc2(un ? un.nm : "")}</span></span></div>
      <p class="stem">${b.s}</p><div class="ox"><button data-v="1" class="o" aria-label="O 맞다">O<small>맞다</small></button><button data-v="0" class="x" aria-label="X 틀리다">X<small>틀리다</small></button></div>`;
  } else if (q.t === "ex") {
    const x = D[sub].ex[q.k];
    const tag = x.gen ? `<span class="tag gen">✏️ 보충 문제 · 기출 아님</span>` : `<span class="tag exb">📜 기출 · 제${x.y}회(${x.yr}) ${x.n}번${x.old ? " · 구 기준" : ""}</span>`;
    html = `<section class="card q"><div class="qhead"><span class="qno">${no}</span><span class="tags">${tag}${q.after ? '<span class="tag">🔗 방금 지문이 나온 문제</span>' : ""}</span></div>
      <p class="stem">${x.q}</p>
      ${x.fig ? `<div class="fig">${x.fig}</div>` : ""}
      ${x.tbl ? `<div class="tblw"><table class="tbl">${x.tbl.map((r, i) => `<tr>${r.map(c => i ? `<td>${c}</td>` : `<th>${c}</th>`).join("")}</tr>`).join("")}</table></div>` : ""}
      ${x.box ? `<div class="box">${x.box.map(b => `<p>${b.t}</p>`).join("")}</div>` : ""}
      ${x.h && !V.res[V.idx] ? `<button class="hintbtn" id="hintBtn">💡 힌트 보기</button><p class="hint" id="hint" hidden>${x.h}</p>` : ""}
      <ul class="opts">${x.o.map((t, i) => `<li><button data-v="${i}"><span class="n">${N5[i]}</span><span>${t}</span></button></li>`).join("")}</ul>`;
  } else {
    const un = D[sub].ub[q.u];
    html = `<section class="card q"><div class="qhead"><span class="qno">${no}</span><span class="tag">🧠 5지선다 · 개념 O·X로 구성</span></div>
      <p class="stem">${esc2(un ? un.nm : "")}에 관한 설명으로 <b>${q.neg ? "옳지 않은" : "옳은"}</b> 것은?</p>
      <ul class="opts">${q.opts.map((id, i) => `<li><button data-v="${i}"><span class="n">${N5[i]}</span><span>${D[sub].oxBy[id].s}</span></button></li>`).join("")}</ul>`;
  }
  const r = V.res[V.idx], nx = nextUn(V.idx);
  if (r) html += `<p class="done-note">${r.ok ? "✅" : "❌"} 이미 푼 문제 · 내 답 ${q.t === "ox" ? (r.v ? "O" : "X") : N5[r.v]} (${r.ok ? "정답" : "오답"}) <button class="btn ghost sm" id="review">해설 보기</button></p>`;
  html += `</section><div class="qnav"><button class="btn ghost" id="prevQ" ${V.idx === 0 ? "disabled" : ""}>◀ 이전</button>${nx >= 0 && nx !== V.idx ? `<button class="btn ghost" id="skipQ">${r ? "다음 안 푼 문제" : "건너뛰기"} ▶</button>` : ""}</div>`;
  document.body.classList.remove("split");
  const cut = html.indexOf('<div class="qnav">');
  m.innerHTML = `<div class="playgrid"><div class="pq">${html.slice(0, cut)}</div><div class="ps" id="psheet"></div></div>${html.slice(cut)}`;
  m.querySelector(".card.q .qhead").insertAdjacentHTML("afterend", bookBar(qid(sub, q), q));
  bindBook(m);
  m.querySelectorAll(".ox button,.opts button").forEach(b => { if (r) { b.disabled = true; b.style.opacity = .55 } else b.onclick = () => answer(q.t === "ox" ? b.dataset.v === "1" : +b.dataset.v) });
  if ($("#hintBtn")) $("#hintBtn").onclick = () => { $("#hint").hidden = false; $("#hintBtn").remove() };
  if (r) $("#review").onclick = () => answer(r.v, true);
  $("#prevQ").onclick = () => { V.idx = Math.max(0, V.idx - 1); render(); scrollTo({ top: 0 }) };
  if ($("#skipQ")) $("#skipQ").onclick = () => { V.idx = nextUn(V.idx); render(); scrollTo({ top: 0 }) };
}
function record(id, ok) {
  const h = Object.assign({ seen: 0, wrong: 0 }, S.hist[id]);
  h.seen++; if (!ok) h.wrong++; h.ok = ok; h.last = day; h.t = Date.now(); S.hist[id] = h;
}
const markOf = e => /^(맞다|정답)/.test(e || "") ? "t" : /^(틀리다|오답)/.test(e || "") ? "f" : "";
function answer(v, review) {
  const sub = V.sub, q = V.Q[V.idx]; let ok, html;
  if (q.t === "ox") {
    const b = D[sub].oxBy[q.id]; ok = v === b.a;
    html = `<p class="answer">정답 <b>${b.a ? "O" : "X"}</b> · 내 답 <b>${v ? "O" : "X"}</b></p><p class="exp">${b.e}</p><p class="point">시험 포인트 · ${b.p}</p>${linkLine(b)}`;
  } else if (q.t === "ex") {
    const x = D[sub].ex[q.k], ki = x.a - 1; ok = v === ki || (x.alt || []).includes(v + 1);
    html = `<p class="answer">정답 <b>${N5[ki]}</b>${x.alt ? ` <small>(${x.alt.map(n => N5[n - 1]).join("·")}도 정답 인정)</small>` : ""} · 내 답 <b>${N5[v]}</b>${x.gen ? `<span class="src">보충 문제</span>` : `<span class="src ${x.src === "공식" ? "off" : ""}">${x.src === "공식" ? "공식 정답" : "자체 풀이"}</span>`}</p>
      ${x.why ? `<p class="why"><b>⚠️ ${(x.alt || []).length >= 4 ? "전항 정답" : "복수 정답"} 처리 사유</b>${x.why}</p>` : ""}
      ${x.box ? `<ul class="ol">${x.box.map(b => `<li><span class="k ${b.a ? "t" : "f"}">${plain(b.t)[0]}${b.a ? "O" : "X"}</span><span>${b.e}</span></li>`).join("")}</ul>` : ""}
      <ul class="ol">${x.o.map((t, i) => { const tf = markOf(x.e[i]); return `<li class="${i === ki ? "key" : ""} ${i === v && !ok ? "picked" : ""}"><span class="k ${tf}">${N5[i]}${tf === "t" ? "O" : tf === "f" ? "X" : ""}</span><span>${(() => { const ex = x.e[i] || (i === ki ? "정답" : ""), short = plain(t).length < 40; return short ? `<b>${t}</b>${ex ? " · " + ex : ""}` : ex || t })()}</span></li>` }).join("")}</ul>
      ${x.s ? `<p class="steps">${x.s}</p>` : ""}
      ${x.p ? `<p class="point">시험 포인트 · ${x.p}</p>` : ""}${x.note ? `<p class="point">참고 · ${x.note}</p>` : ""}`;
  } else {
    const ki = q.opts.indexOf(q.key); ok = v === ki;
    html = `<p class="answer">정답 <b>${N5[ki]}</b> · 내 답 <b>${N5[v]}</b></p>
      <ul class="ol">${q.opts.map((id, i) => { const b = D[sub].oxBy[id]; return `<li class="${i === ki ? "key" : ""} ${i === v && !ok ? "picked" : ""}"><span class="k ${b.a ? "t" : "f"}">${N5[i]}${b.a ? "O" : "X"}</span><span>${b.e}${i === ki ? `<small>시험 포인트 · ${b.p}</small>` : ""}</span></li>` }).join("")}</ul>${linkLine(D[sub].oxBy[q.key])}`;
  }
  if (!review) {
    record(qid(sub, q), ok);
    V.res[V.idx] = { ok, v }; if (timed() && tmUsed() > tmLimit()) V.res[V.idx].late = true;
    if (V.mode === "extra") extraPut(sub);
    if (answered() >= V.Q.length) tmStop();
    if (V.mode === "daily") {
      const e = entry(sub); e.res = V.res; e.t = Date.now(); e.tm = { used: Math.max(tmUsed(), (e.tm || {}).used || 0), paused: false };
      (S.days[day] = S.days[day] || {})[sub] = { done: answered(), ok: V.res.filter(r => r && r.ok).length, total: V.Q.length };
    }
    V.combo = ok ? (V.combo || 0) + 1 : 0;
    touch(); stats(); progressNav();
  }
  const nx = nextUn(V.idx), last = nx < 0, inline = sheetMode() === "inline";
  const cheer = ok ? ["좋아요!", "정확해요!", "완벽!", "그대로 가요!"][(V.combo || 1) % 4] : "괜찮아요, 해설 보고 다음에 맞혀요";
  const body = `<div class="verdict"><span class="mark" aria-hidden="true">${ok ? "🎉" : "💥"}</span><span><span id="vtext">${ok ? "정답!" : "오답"}</span><small>${review ? "다시 보는 해설" : cheer}</small></span>${!review && ok && V.combo >= 2 ? `<span class="combo">🔥 ${V.combo}콤보</span>` : ""}</div>${inline ? "" : bookBar(qid(sub, q), q, !ok)}${html}
    <div class="row"><button class="btn" id="next">${review ? "해설 닫기" : last ? "🏁 결과 보기" : "다음 문제 ▶"}</button>${noteOf(sub, q) ? `<button class="notelink" id="toNote">📖 개념정리에서 보기</button>` : ""}${inline ? `<button class="notelink upq" id="upQ">⬆ 문제 다시 보기</button>` : ""}</div>`;
  let box;
  if (inline) {
    /* 문제를 가리지 않고 문제 바로 아래(넓은 화면은 오른쪽)에 해설을 펼친다 */
    markQuestion(q, v, ok);
    box = $("#psheet"); box.className = "ps sheet in " + (ok ? "good" : "bad"); box.innerHTML = body;
    box.closest(".playgrid").classList.add("has-sheet"); document.body.classList.add("split");
    const bk = $("#main .card.q .bk"); if (bk && !review && !ok && !(S.book[qid(sub, q)] || {}).on) bk.dataset.w = "1";
    if ($("#hintBtn")) $("#hintBtn").remove();
    const wide = matchMedia("(min-width: 1100px)").matches;
    if (!wide) box.scrollIntoView({ behavior: "smooth", block: "start" });
    $("#upQ").onclick = () => $("#main .card.q").scrollIntoView({ behavior: "smooth", block: "start" });
  } else {
    box = $("#sheet"); box.className = "sheet " + (ok ? "good" : "bad"); box.innerHTML = body;
    bindBook(box); $("#modal").hidden = false; box.scrollTop = 0;
  }
  $("#next").focus({ preventScroll: true });
  const leave = () => { closeModal(); if (!review) V.idx = last ? V.Q.length : nx; };
  $("#next").onclick = () => { if (review && inline) { render(); return } leave(); render(); scrollTo({ top: 0 }) };
  if ($("#toNote")) $("#toNote").onclick = () => { leave(); tmStop(); T.paused = timed(); saveTimer(); go(`#/s/${sub}/note/${noteOf(sub, q)}`) };
}
/* 해설을 펼친 뒤 문제 쪽 보기에도 정답·내 답 표시 */
function markQuestion(q, v, ok) {
  const sub = V.sub, card = $("#main .card.q"); if (!card) return;
  const key = q.t === "ox" ? (D[sub].oxBy[q.id].a ? "1" : "0") : q.t === "ex" ? String(D[sub].ex[q.k].a - 1) : String(q.opts.indexOf(q.key));
  const mine = q.t === "ox" ? (v ? "1" : "0") : String(v);
  card.querySelectorAll(".ox button,.opts button").forEach(b => {
    b.disabled = true; b.onclick = null; b.style.opacity = "";
    if (b.dataset.v === key) b.classList.add("is-key");
    else if (b.dataset.v === mine && !ok) b.classList.add("is-picked");
    else b.classList.add("is-dim");
  });
  const dn = card.querySelector(".done-note"); if (dn) dn.remove();
}
const LS_SHEET = "dora-exam-sheet";
const sheetMode = () => localStorage.getItem(LS_SHEET) === "modal" ? "modal" : "inline";
function linkLine(b) {
  if (!b || !b.links) return "";
  const lab = s => { const [k, o] = s.split(" "), [y, n] = k.split("-"); return `제${y}회 ${n}번${o ? " " + o : ""}` };
  return `<p class="point">기출 출제 · ${b.links.map(lab).join(", ")}</p>`;
}
function closeModal() { $("#modal").hidden = true }
document.addEventListener("keydown", e => { if (e.target.closest && e.target.closest("input,textarea")) return; if ((!$("#modal").hidden || $("#psheet.in")) && $("#next") && (e.key === "Enter" || (e.key === "Escape" && !$("#modal").hidden))) { e.preventDefault(); $("#next").click() } });
$("#modal").addEventListener("click", e => { if (e.target.id === "modal") $("#next").click() });

function result() {
  const sub = V.sub, n = V.res.filter(r => r && r.ok).length, wr = V.Q.map((q, i) => ({ q, r: V.res[i] })).filter(x => x.r && !x.r.ok);
  const item = ({ q }) => {
    if (q.t === "ex") { const x = D[sub].ex[q.k], t = plain(x.q); return `<li>${x.gen ? "보충 문제" : `제${x.y}회 ${x.n}번`} · ${esc2(t.length > 60 ? t.slice(0, 60) + "…" : t)}<span>정답 ${N5[x.a - 1]} · ${plain(x.e[x.a - 1])}</span></li>` }
    const b = D[sub].oxBy[q.t === "ox" ? q.id : q.key]; return `<li>${b.s}<span>정답 ${b.a ? "O" : "X"} · ${b.e}</span></li>`;
  };
  $("#progress").hidden = true;
  const ratio = n / Math.max(1, V.Q.length), st3 = ratio >= .9 ? 3 : ratio >= .7 ? 2 : ratio >= .5 ? 1 : 0;
  const [me, mt] = ratio === 1 ? ["🏆", "퍼펙트! 전부 맞혔어요"] : ratio >= .8 ? ["🥇", "훌륭해요!"] : ratio >= .6 ? ["🥈", "잘했어요! 틀린 것만 정리하면 끝"] : ratio >= .4 ? ["🥉", "절반은 넘었어요. 오답을 다시 봐요"] : ["💪", "괜찮아요. 오답 정리로 한 번 더!"];
  $("#main").innerHTML = `<section class="card center result"><div class="qhead" style="justify-content:center"><span class="tag">🏁 ${V.mode === "daily" ? "오늘의 문제 클리어" : "스테이지 완료"}</span></div>
    <div class="bigemo" aria-hidden="true">${me}</div>${starRow(st3, 3)}
    <div class="score">${n}<small> / ${V.Q.length}</small></div><p class="exp"><b>${mt}</b> · 정답률 ${Math.round(ratio * 100)}%</p>
    ${timed() ? `<p class="note">⏱️ ${fmt(tmUsed())} / 제한 ${fmt(tmLimit())}${V.res.some(r => r && r.late) ? ` · 제한시간 지나서 푼 문제 ${V.res.filter(r => r && r.late).length}개` : " · 시간 안에 완료 ⚡"}</p>` : ""}
    <div id="newBadge"></div>
    <div class="row" style="justify-content:center">${wr.length ? `<button class="btn" id="retry">🔁 틀린 ${wr.length}문제 다시</button>` : ""}${V.mode === "daily" || V.mode === "extra" ? `<button class="btn ghost" id="extra">➕ 추가 ${DAILY_N}문제</button>` : ""}<button class="btn ghost" id="home">🏠 홈으로</button></div></section>
    ${wr.length ? `<h2 class="sec">❌ 틀린 문제</h2><section class="card"><ul class="wrong">${wr.map(item).join("")}</ul></section>` : ""}`;
  const fresh = newBadges();
  if (fresh.length) $("#newBadge").innerHTML = `<div class="newb"><b>🏅 새 배지!</b>${fresh.map(b => `<span><i aria-hidden="true">${b.e}</i>${b.n}</span>`).join("")}</div>`;
  if ($("#retry")) $("#retry").onclick = () => { V.Q = wr.map(x => x.q); V.res = []; V.idx = 0; V.mode = "retry"; render() };
  if ($("#extra")) $("#extra").onclick = () => { extraClear(sub); V.key = ""; go(`#/s/${sub}/daily/extra`) };
  $("#home").onclick = () => go("#/");
}

/* ───────── 타이머 ───────── */
const tmLimit = () => V.Q.length * SEC_PER_Q * 1000;
const tmUsed = () => T.used + (T.run ? Date.now() - T.run : 0);
function tmStop() { if (T.run) { T.used += Date.now() - T.run; T.run = 0 } }
function tmGo() { if (!T.run && !T.paused && answered() < V.Q.length) T.run = Date.now() }
const tmPaused = () => timed() && T.paused;
const fmt = ms => { const s = Math.floor(Math.abs(ms) / 1000); return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}` };
function saveTimer() {
  if (V.route !== "subject") return;
  if (V.mode === "extra") return extraPut(V.sub);
  if (V.mode !== "daily") return;
  const e = entry(V.sub);
  if (!e || JSON.stringify(e.set) !== JSON.stringify(V.Q)) return;          // 다른 세트로 바뀌었으면 이 화면의 시간을 덮어쓰지 않음
  e.tm = { used: Math.max(tmUsed(), (e.tm || {}).used || 0), paused: T.paused }; e.t = Date.now(); touch();
}
/* 추가 문제 세트: 이 기기에만 그날 하나 보관 */
const LS_EXTRA = "dora-exam-extra";
function extraAll() { try { return JSON.parse(localStorage.getItem(LS_EXTRA)) || {} } catch (e) { return {} } }
function extraGet(sub) {
  const x = extraAll()[sub];
  if (!x || x.day !== day || !Array.isArray(x.Q) || !x.Q.length) return null;
  if ((x.res || []).filter(Boolean).length >= x.Q.length) return null;
  if (!x.Q.every(q => q.t === "ex" ? D[sub].ex[q.k] : q.t === "ox" ? D[sub].oxBy[q.id] : D[sub].oxBy[q.key])) return null;
  return x;
}
function extraPut(sub) { const a = extraAll(); a[sub] = { day, Q: V.Q, res: V.res, used: tmUsed(), paused: T.paused }; try { localStorage.setItem(LS_EXTRA, JSON.stringify(a)) } catch (e) { } }
function extraClear(sub) { const a = extraAll(); delete a[sub]; try { localStorage.setItem(LS_EXTRA, JSON.stringify(a)) } catch (e) { } }
function tmDraw() {
  const bar = $("#timerbar");
  if (!timed() || !V.Q.length || answered() >= V.Q.length || V.idx >= V.Q.length) { bar.hidden = true; return }
  bar.hidden = false;
  const left = tmLimit() - tmUsed(), over = left < 0; bar.classList.toggle("over", over);
  if (!$("#tmBtn")) {
    bar.innerHTML = `<span class="tico" aria-hidden="true">⏱️</span><span class="tt" id="tmT"></span><span class="tl" id="tmL"></span><button id="tmBtn"></button><span class="tfill"><i id="tmF"></i></span>`;
    $("#tmBtn").onclick = () => { if (T.paused) { T.paused = false; tmGo() } else { tmStop(); T.paused = true } saveTimer(); render() };
  }
  $("#tmT").textContent = (over ? "+" : "") + fmt(left);
  $("#tmL").textContent = T.paused ? "일시정지 중" : over ? `제한 초과 · 계속 풀 수 있어요` : `남은 시간 · 제한 ${fmt(tmLimit())}`;
  $("#tmBtn").textContent = T.paused ? "▶ 계속" : "⏸ 일시정지";
  const f = Math.max(0, Math.min(1, left / tmLimit())); $("#tmF").style.width = (f * 100).toFixed(1) + "%"; bar.classList.toggle("low", !over && f < .2);
}
let tick = 0;
setInterval(() => {
  if (!timed()) return; tmDraw();
  /* 15초마다 흐른 시간을 이 기기에 저장 (앱이 갑자기 꺼져도 시간이 되돌아가지 않게) */
  if (T.run && ++tick % 15 === 0) {
    if (V.mode === "extra") extraPut(V.sub);
    else { const e = entry(V.sub); if (e && JSON.stringify(e.set) === JSON.stringify(V.Q)) { e.tm = { used: Math.max(tmUsed(), (e.tm || {}).used || 0), paused: false }; saveLocal() } }
  }
}, 1000);
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    if (timed() && T.run) { tmStop(); T.paused = true; saveTimer(); render() }
    if (syncOn()) syncNow();
  } else {
    if (today() !== day) { day = today(); V.key = ""; route() }
    if (syncOn()) syncNow();
  }
});
setInterval(() => { if (today() !== day) { day = today(); if (!timed() || answered() === 0) { V.key = ""; route() } } }, 60000);

/* ───────── 설정 ───────── */
function renderSettings() {
  chrome({ back: { label: "홈", hash: "#/" }, eyebrow: "감정평가사 1차 · 문제풀이", title: "⚙️ 설정" });
  const theme = localStorage.getItem(LS_THEME) || "auto";
  $("#main").innerHTML = `
  <section class="card"><h2 class="sec" style="margin:0">☁️ 기기 간 동기화 (GitHub 비공개 저장소)</h2>
    <p class="exp" style="font-size:14.5px">휴대폰과 PC 기록을 잇는 설정이에요. 기기마다 <b>한 번씩</b> 입력하면 됩니다. 입력한 토큰은 이 기기 안에만 저장돼요.</p>
    <div class="form">
      <label>GitHub 아이디<small>github.com 오른쪽 위 프로필 사진을 누르면 보이는 이름</small><input id="fOwner" autocomplete="off" autocapitalize="off" spellcheck="false" value="${esc2(SY.owner || "")}"></label>
      <label>기록 저장소 이름<small>비공개(Private)로 만든 저장소</small><input id="fRepo" autocomplete="off" autocapitalize="off" spellcheck="false" value="${esc2(SY.repo || "dora-exam-records")}"></label>
      <label>토큰<small>github_pat_ 로 시작하는 긴 글자</small><input id="fToken" type="password" autocomplete="off" spellcheck="false" value="${esc2(SY.token || "")}"></label>
      <div class="row"><button class="btn" id="fSave">연결하고 동기화</button>${syncOn() ? `<button class="btn ghost" id="fOff">이 기기 연결 끊기</button>` : ""}</div>
      <p class="msg ${syncState.status === "ok" ? "ok" : syncState.status === "err" ? "err" : ""}" id="fMsg">${syncOn() ? (syncState.msg || (syncState.status === "ok" ? "연결됨 · 마지막 동기화 " + new Date(syncState.at).toLocaleTimeString("ko-KR") : "연결 정보가 저장돼 있어요.")) : "아직 연결 전이에요."}</p>
    </div></section>
  <section class="card"><h2 class="sec" style="margin:0">🎨 화면 밝기</h2>
    <div class="themes" role="radiogroup" aria-label="화면 밝기">${[["auto", "🖥️", "기기 설정"], ["light", "☀️", "라이트"], ["dark", "🌙", "다크"]].map(([v, e, n]) => `<button role="radio" aria-checked="${theme === v}" data-t="${v}"><span aria-hidden="true">${e}</span>${n}</button>`).join("")}</div>
    <p class="note">화면 위 오른쪽 ${isDark() ? "☀️" : "🌙"} 버튼으로도 바로 바꿀 수 있어요.</p></section>
  <section class="card"><h2 class="sec" style="margin:0">📝 해설 보기 방식</h2>
    <div class="themes two" role="radiogroup" aria-label="해설 보기 방식">${[["inline", "📄", "문제와 함께", "문제 아래에 펼침 · PC는 오른쪽"], ["modal", "🪟", "팝업", "문제 위에 창으로"]].map(([v, e, n, d]) => `<button role="radio" aria-checked="${sheetMode() === v}" data-sm="${v}"><span aria-hidden="true">${e}</span>${n}<small>${d}</small></button>`).join("")}</div></section>
  <section class="card"><h2 class="sec" style="margin:0">💾 기록 백업</h2>
    <p class="exp" style="font-size:14.5px">기록을 파일로 내려받거나, 내려받은 파일을 불러와 합칠 수 있어요(기존 기록은 지워지지 않고 합쳐집니다).</p>
    <div class="row"><button class="btn ghost" id="fExport">기록 내려받기</button><label class="btn ghost" style="cursor:pointer">기록 불러오기<input type="file" id="fImport" accept="application/json,.json" hidden></label></div></section>
  <p class="note">앱 버전 ${APP_VER} · 문제 회계 ${D.acct ? D.acct.exam.length + D.acct.ox.length : 0}개, 경제 ${D.econ ? D.econ.exam.length : 0}개</p>`;
  document.querySelectorAll(".themes button[data-sm]").forEach(b => b.onclick = () => { localStorage.setItem(LS_SHEET, b.dataset.sm); renderSettings() });
  document.querySelectorAll(".themes button[data-t]").forEach(b => b.onclick = () => { localStorage.setItem(LS_THEME, b.dataset.t); applyTheme(); renderSettings() });
  $("#fSave").onclick = async () => {
    SY.owner = $("#fOwner").value.trim().replace(/^@/, ""); SY.repo = $("#fRepo").value.trim(); SY.token = $("#fToken").value.trim();
    const msg = $("#fMsg"); msg.className = "msg"; msg.textContent = "확인 중…";
    if (!syncOn()) { msg.className = "msg err"; msg.textContent = "세 칸을 모두 채워 주세요."; return }
    try {
      const r = await ghFetch("");
      if (r.status !== 200) { msg.className = "msg err"; msg.textContent = ghMsg(r.status); return }
      const j = await r.json();
      if (!j.private) { msg.className = "msg err"; msg.textContent = "이 저장소는 공개(Public)예요. 기록용은 비공개(Private) 저장소로 만들어 주세요."; return }
      if (j.permissions && !j.permissions.push) { msg.className = "msg err"; msg.textContent = ghMsg(403); return }
      saveSY(); await syncNow();
      msg.className = "msg " + (syncState.status === "ok" ? "ok" : "err");
      msg.textContent = syncState.status === "ok" ? "연결됐어요. 이제 이 기기의 기록이 자동으로 맞춰집니다." : syncState.msg;
    } catch (e) { msg.className = "msg err"; msg.textContent = "GitHub에 연결하지 못했어요. 인터넷 연결을 확인해 주세요." }
  };
  if ($("#fOff")) $("#fOff").onclick = () => { if (!confirm("이 기기의 동기화 연결을 끊을까요? (기록은 지워지지 않아요)")) return; SY = {}; saveSY(); syncState = { busy: false, again: false, status: "", msg: "", at: 0 }; renderSettings() };
  $("#fExport").onclick = () => {
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([JSON.stringify(exportState(), null, 1)], { type: "application/json" }));
    a.download = `감평기록-${day}.json`; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  };
  $("#fImport").onchange = async e => {
    const f = e.target.files[0]; if (!f) return;
    try { const j = JSON.parse(await f.text()); if (!j.hist) throw 0; S = merge(S, j); touch(); alert("기록을 합쳤어요.") } catch (err) { alert("이 파일은 기록 파일이 아니에요.") }
  };
}
function setThemeOn(doc) { const t = localStorage.getItem(LS_THEME) || "auto"; if (t === "auto") doc.documentElement.removeAttribute("data-theme"); else doc.documentElement.dataset.theme = t }
function isDark() { const t = localStorage.getItem(LS_THEME) || "auto"; return t === "dark" || (t === "auto" && matchMedia("(prefers-color-scheme: dark)").matches) }
function drawThemeBtn() { const b = $("#themeBtn"); if (!b) return; const d = isDark(); b.textContent = d ? "☀️" : "🌙"; b.setAttribute("aria-label", d ? "라이트 모드로 바꾸기" : "다크 모드로 바꾸기"); b.title = b.getAttribute("aria-label") }
function applyTheme() {
  setThemeOn(document);
  try { const d = $("#noteFrame").contentDocument; if (d && d.documentElement) setThemeOn(d) } catch (e) { }
  document.querySelectorAll('meta[name="theme-color"]').forEach(m => m.content = isDark() ? "#141a17" : "#f3f5f2");
  drawThemeBtn();
}
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => applyTheme());

/* ───────── 시작 ───────── */
(async function init() {
  applyTheme();
  try { await loadData() } catch (e) { $("#title").textContent = "문제를 불러오지 못했어요"; $("#main").innerHTML = `<p class="exp">인터넷 연결을 확인하고 다시 열어 주세요. (${esc2(e.message)})</p>`; return }
  S = loadLocal();
  if (!S || !S.hist) { S = blank(); try { S = merge(S, await getJSON("data/migrate.json")) } catch (e) { } saveLocal() }
  S.daily = S.daily || {}; S.days = S.days || {}; S.subjects = S.subjects || {}; S.book = S.book || {}; S.sent = S.sent || {};
  migrateOxToSent();
  route();
  if (syncOn()) syncNow();
  if ("serviceWorker" in navigator && location.protocol === "https:") {
    const hadSW = !!navigator.serviceWorker.controller;
    navigator.serviceWorker.register("sw.js").then(r => r.update()).catch(() => { });
    /* 새 버전이 설치되면 한 번 새로고침해 바로 적용 (풀던 시험 중이면 다음에 열 때 적용) */
    let reloaded = false;
    navigator.serviceWorker.addEventListener("controllerchange", () => {
      if (!hadSW || reloaded) return;
      if (timed() && answered() > 0 && answered() < V.Q.length) { toast("🆕 새 버전이 준비됐어요. 앱을 다시 열면 적용돼요."); return }
      reloaded = true; saveTimer(); location.reload();
    });
  }
})();
