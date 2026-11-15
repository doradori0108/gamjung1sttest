/* 감평 1차 문제풀이 (PWA)
   - 문제: data/<과목>/units.json · exam.json · ox.json
   - 기록: 이 기기(localStorage)에 바로 저장 → 설정에서 연결하면 GitHub 비공개 저장소 progress.json과 동기화
   - 문항 ID: "<과목>:<회차-번호>" (기출·보충), "<과목>:ox<번호>" (개념 O·X) */
"use strict";
const APP_VER = "1.2.0";
const DAILY_N = 20;               // 오늘의 문제 수 (과목별)
const SEC_PER_Q = 60;             // 문제당 제한시간(초) → 20문제 = 20분
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
    const [meta, exam, ox] = await Promise.all([getJSON(`data/${s.id}/units.json`), getJSON(`data/${s.id}/exam.json`), getJSON(`data/${s.id}/ox.json`).catch(() => [])]);
    D[s.id] = { meta, exam, ox, ex: Object.fromEntries(exam.map(x => [x.k, x])), oxBy: Object.fromEntries(ox.map(b => [b.id, b])), ub: Object.fromEntries(meta.units.map(u => [u.u, u])) };
  }));
}

/* ───────── 기록 ───────── */
let S = null;
function blank() { return { v: 1, subjects: {}, hist: {}, days: {}, daily: {} } }
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
      if (nx !== ny) M.daily[d][s] = nx > ny ? x : y;
      else if (JSON.stringify(x.set) !== JSON.stringify(y.set)) M.daily[d][s] = (x.c || 0) <= (y.c || 0) ? x : y;
      else M.daily[d][s] = (x.t || 0) >= (y.t || 0) ? x : y;
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
  const [cls, txt] = !syncOn() ? ["", "기기 간 동기화 꺼짐"] : syncState.status === "busy" ? ["", "동기화 중…"] : syncState.status === "ok" ? ["ok", `동기화됨 ${t}`] : syncState.status === "offline" ? ["", "오프라인 · 나중에 동기화"] : syncState.status === "err" ? ["err", "동기화 오류 · 눌러서 확인"] : ["", "동기화 대기"];
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
const exOfU = (sub, u) => D[sub].exam.filter(x => x.u === u && !x.skip);
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
  if (e && valid && !((e.res || []).filter(Boolean).length === 0 && e.lec !== L)) return e;
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

/* ───────── 라우팅 ───────── */
function go(hash) { if (location.hash !== hash) location.hash = hash; else route() }
function route() {
  closeModal();
  const p = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  tmStop(); saveTimer();
  if (p[0] === "settings") { V = { route: "settings", key: "settings" }; return renderSettings() }
  if (p[0] === "s" && D[p[1]]) {
    const sub = p[1], tab = ["note", "daily", "unit", "wrong", "map"].includes(p[2]) ? p[2] : "daily", arg = p[3] || "";
    const key = [sub, tab, arg].join("/");
    if (V.key === key && V.route === "subject") return render();
    V = { route: "subject", sub, tab, mode: null, unit: null, Q: [], res: [], idx: 0, key, arg };
    if (tab === "note") return render();
    if (tab === "daily" && arg === "extra") { V.mode = "extra"; V.Q = buildSet(sub, day + "#" + Math.random(), day); T = { used: 0, run: 0, paused: false } }
    else if (tab === "daily") { const e = dailyEntry(sub, true); V.mode = "daily"; V.Q = e.set; V.res = e.res; T = { used: e.tm ? e.tm.used : 0, run: 0, paused: !!(e.tm && e.tm.paused) } }
    else if (tab === "unit" && arg && D[sub].ub[arg]) {
      V.mode = "unit"; V.unit = arg;
      const rank = x => { const h = S.hist[`${sub}:${x.k}`]; return !h ? 0 : h.ok ? 2 : 1 };
      V.Q = exOfU(sub, arg).slice().sort((a, b) => rank(a) - rank(b) || (b.y || 0) - (a.y || 0) || (a.n || 0) - (b.n || 0)).map(x => ({ t: "ex", k: x.k }));
    }
    else if (tab === "wrong" && arg === "play") { V.mode = "wrong"; V.Q = wrongList(sub).map(x => x.q) }
    V.idx = V.res.filter(Boolean).length >= V.Q.length ? V.Q.length : Math.max(0, nextUn(-1));
    return render();
  }
  V = { route: "home", key: "home" }; renderHome();
}
window.addEventListener("hashchange", route);
function onRemoteChange() {
  if (V.route === "subject" && V.mode === "daily" && $("#modal").hidden) { const e = entry(V.sub); if (e && e !== V.entryRef) { V.key = ""; route() } }
  else if (V.route === "home") renderHome();
}
function refreshHomeIfShown() { if (V.route === "home") renderHome() }

/* ───────── 공통 머리 ───────── */
function chrome({ subject = "", back = null, eyebrow = "", title = "", meta = "", tabs = false, stats = false }) {
  document.body.dataset.subject = subject;
  $("#topbar").innerHTML = `${back ? `<button class="back" id="backBtn">‹ ${back.label}</button>` : `<span class="note">감정평가사 1차</span>`}<button class="pill" id="syncPill"></button>`;
  if (back) $("#backBtn").onclick = () => go(back.hash);
  $("#syncPill").onclick = () => go("#/settings");
  drawSync();
  $("#eyebrow").textContent = eyebrow; $("#title").innerHTML = title; $("#meta").innerHTML = meta;
  $("#tabs").hidden = !tabs; $("#stats").hidden = !stats;
  $("#timerbar").hidden = true; $("#progress").hidden = true; $("#foot").textContent = "";
  $("#seg").hidden = true; $("#notebox").hidden = true; document.body.classList.remove("noting"); $("#main").hidden = false; $("#eyebrow").hidden = false; $("#meta").hidden = false;
}
const dateLabel = () => { const d = new Date(day + "T00:00:00"); return `<b>${day.replace(/-/g, ".")}</b> (${"일월화수목금토"[d.getDay()]})` };
function lecLabel(sub, lec) { const m = D[sub].meta; return m.stepLabel === "강" ? `${lec}강 · ${m.lectures[lec - 1] || ""}` : `${m.lectures[lec - 1] || ""}` }

/* ───────── 홈 ───────── */
function renderHome() {
  chrome({ eyebrow: "감정평가사 1차 · 문제풀이", title: "오늘의 공부", meta: `<span>${dateLabel()}</span>` });
  const cards = SUBJ.map(s => {
    const sm = summary(s.id), st = streak(s.id), wr = wrongList(s.id).length, m = D[s.id].meta, L = lecOf(s.id);
    const state = !sm.started ? "오늘 시작 전" : sm.done >= sm.total ? "오늘 완료 ✓" : `오늘 ${sm.done}/${sm.total} 푸는 중`;
    return `<div class="scard" data-s="${s.id}">
      <div class="row1"><h2>${m.name}</h2><span class="sub">${m.teacher} ${m.course} · ${m.stepLabel === "강" ? L + "강까지" : esc2(m.lectures[L - 1]) + "까지"}</span></div>
      <span class="bar"><i style="width:${Math.round(sm.done / Math.max(1, sm.total) * 100)}%"></i></span>
      <div class="nums"><span>오늘 <b>${sm.done}/${sm.total}</b>${sm.done ? ` (맞힘 ${sm.ok})` : ""}</span><span>연속 완료 <b>${st}</b>일</span><span>누적 틀린 문제 <b>${wr}</b>개</span></div>
      <div class="two"><button data-go="note">1 개념정리<small>${m.notes ? "요약노트" : "준비 중"}</small></button><button class="main" data-go="daily">2 문제풀이<small>${state}</small></button></div>
    </div>`;
  }).join("");
  $("#main").innerHTML = `<div class="subjects">${cards}</div>
    ${syncOn() ? "" : `<div class="warnbox">지금은 이 기기에만 기록이 저장돼요. 휴대폰과 PC 기록을 이으려면 <a href="#/settings">설정 → 기기 간 동기화</a>를 한 번 연결해 주세요.</div>`}
    <div class="row"><a class="btn ghost sm" href="#/settings">설정</a></div>`;
  document.querySelectorAll(".scard button[data-go]").forEach(b => b.onclick = () => go(`#/s/${b.closest(".scard").dataset.s}/${b.dataset.go}`));
  $("#foot").textContent = `오늘의 문제는 매일 자정(한국시간)에 새로 바뀌고, 과목마다 ${DAILY_N}문제 · ${DAILY_N * SEC_PER_Q / 60}분입니다.`;
}
const esc2 = s => String(s).replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

/* ───────── 과목 화면 ───────── */
function render() {
  if (V.route !== "subject") return;
  const sub = V.sub, m = D[sub].meta, L = lecOf(sub);
  const wrN = wrongList(sub).length;
  chrome({
    subject: sub, back: { label: "홈", hash: "#/" }, eyebrow: `감정평가사 1차 · ${m.name} · ${m.teacher} ${m.course}`,
    title: V.mode === "daily" ? `오늘의 ${V.Q.length}문제` : V.mode === "extra" ? `추가 ${V.Q.length}문제` : V.mode === "unit" ? esc2(D[sub].ub[V.unit].nm) : V.mode === "wrong" ? "틀린 문제 다시 풀기" : V.mode === "retry" ? "방금 틀린 문제" : V.tab === "unit" ? "단원별 기출" : V.tab === "wrong" ? "틀린 문제" : V.tab === "note" ? `${m.name} 개념정리` : "진도 · 출제 지도",
    meta: `<span>${dateLabel()}</span><span>진도 <b>${esc2(lecLabel(sub, L))}</b>까지</span>`, tabs: true, stats: true
  });
  drawSeg();
  if (V.tab === "note") { $("#tabs").hidden = true; $("#stats").hidden = true; return renderNote() }
  const tabs = [["daily", "오늘의 문제"], ["unit", "단원별"], ["wrong", "틀린 문제"], ["map", "진도 지도"]];
  $("#tabs").innerHTML = tabs.map(([t, n]) => `<button role="tab" data-t="${t}" aria-selected="${V.tab === t}">${n}${t === "wrong" && wrN ? `<span class="cnt">${wrN}</span>` : ""}</button>`).join("");
  $("#tabs").querySelectorAll("button").forEach(b => b.onclick = () => go(`#/s/${sub}/${b.dataset.t}`));
  stats();
  if (V.tab === "map") return renderMap();
  if (V.tab === "unit" && !V.mode) return renderUnitPick();
  if (V.tab === "wrong" && !V.mode) return renderWrongPick();
  renderPlay();
}
function stats() {
  const sub = V.sub, sm = summary(sub), st = streak(sub);
  const ex = D[sub].exam.filter(x => !x.skip && !x.gen), seen = ex.filter(x => S.hist[`${sub}:${x.k}`]).length, wr = wrongList(sub).length;
  $("#stats").innerHTML = `<span class="st"><span><b>${sm.done}</b>/${sm.total}</span><small>오늘 푼 문제</small></span><span class="st"><span><b>${st}</b>일</span><small>연속 완료</small></span><span class="st"><span><b>${seen}</b>문항</span><small>풀어 본 기출 (수록 ${ex.length})</small></span><span class="st ${wr ? "warn" : ""}"><span><b>${wr}</b>개</span><small>누적 틀린 문제</small></span>`;
}

/* 단원 행 */
function unitRow(sub, x, withBtn) {
  const L = Math.min(lecOf(sub), D[sub].meta.dataThrough), open = x.lec <= L, m = D[sub].meta;
  const ex = exOfU(sub, x.u), ox = oxOfU(sub, x.u).length, done = ex.filter(q => S.hist[`${sub}:${q.k}`]).length;
  const wr = ex.filter(q => (S.hist[`${sub}:${q.k}`] || {}).ok === false).length;
  const lecTxt = m.stepLabel === "강" ? `${x.lec}강~ · ` : "";
  const sub2 = x.lec > lecOf(sub) ? `${lecTxt}아직 수강 전` : !open ? `${lecTxt}수강했지만 기출 추가 전` : ex.length ? `${lecTxt}수록 ${ex.length}문항 · ${done}문항 풀어 봄${wr ? ` · 틀림 ${wr}` : ""}${ox ? ` · 개념 O·X ${ox}` : ""}` : `${lecTxt}기출 미수록`;
  return `<li class="unit ${open ? "open" : "locked"}"><span class="nm">${esc2(x.nm)}<small>${sub2}</small></span>
   <span class="ct"><span class="lv ${lvOf(x.n) === "상" ? "h" : ""}">${lvOf(x.n)}</span><span class="bar" title="10년간 ${x.n}문항"><i style="width:${Math.round(Math.min(1, x.n / 31) * 100)}%"></i></span>${String(x.n).padStart(2, " ")}${withBtn && open && ex.length ? `<button data-u="${x.u}">풀기</button>` : ""}</span></li>`;
}
function renderUnitPick() {
  const sub = V.sub, L = Math.min(lecOf(sub), D[sub].meta.dataThrough);
  const list = D[sub].meta.units.filter(x => x.lec <= L);
  $("#main").innerHTML = list.length ? `<ul class="units">${list.map(x => unitRow(sub, x, true)).join("")}</ul>` : `<p class="exp">아직 열린 단원이 없어요. '진도 · 출제 지도'에서 진도를 올려 주세요.</p>`;
  $("#main").querySelectorAll("button[data-u]").forEach(b => b.onclick = () => go(`#/s/${sub}/unit/${b.dataset.u}`));
  $("#foot").textContent = "수강한 단원만 열립니다. 숫자와 막대는 제28~37회(10년) 중 그 단원 출제 문항 수, 상·중·하는 출제 비중(15문항 이상 상, 8~14 중, 7 이하 하). 단원 안에서는 안 푼 문제 → 틀린 문제 → 맞힌 문제 순으로 나옵니다.";
}
function renderWrongPick() {
  const sub = V.sub, list = wrongList(sub);
  if (!list.length) { $("#main").innerHTML = `<section class="card"><p class="exp">지금은 틀린 채로 남은 문제가 없어요. 다시 풀어서 맞히면 이 목록에서 빠집니다.</p></section>`; return }
  const byU = {};
  for (const x of list) { const u = x.q.t === "ex" ? D[sub].ex[x.q.k].u : D[sub].oxBy[x.q.id].u; byU[u] = (byU[u] || 0) + 1 }
  $("#main").innerHTML = `<section class="card"><div class="qhead"><span class="qno">틀린 채로 남은 문제</span><span class="tag">${list.length}개</span></div>
    <p class="exp">마지막으로 풀었을 때 틀린 문제만 모았어요. 여러 번 틀린 문제부터 나오고, 맞히면 목록에서 빠집니다. 제한시간은 없어요.</p>
    <div class="row"><button class="btn" id="goWrong">${list.length}문제 풀기</button></div></section>
    <ul class="units">${D[sub].meta.units.filter(u => byU[u.u]).map(u => `<li class="unit"><span class="nm">${esc2(u.nm)}</span><span class="ct">${byU[u.u]}개</span></li>`).join("")}</ul>`;
  $("#goWrong").onclick = () => go(`#/s/${sub}/wrong/play`);
}
function renderMap() {
  const sub = V.sub, m = D[sub].meta, L = lecOf(sub), units = m.units;
  const openN = units.filter(x => x.lec <= Math.min(L, m.dataThrough)).reduce((a, b) => a + b.n, 0), all = units.reduce((a, b) => a + b.n, 0);
  const nxt = units.filter(x => x.lec > L).sort((a, b) => a.lec - b.lec)[0];
  const grps = [...new Set(units.map(u => u.grp))];
  $("#main").innerHTML = `<div class="lec"><button id="lm" aria-label="진도 한 ${m.stepLabel} 빼기">−</button><span class="num">지금 들은 ${m.stepLabel === "강" ? "강의" : "단원"}<b>${esc2(lecLabel(sub, L))}</b></span><button id="lp" aria-label="진도 한 ${m.stepLabel} 더하기">+</button>
     <span class="lname">10년 기출 ${all}문항 중 <b>${openN}문항(${Math.round(openN / all * 100)}%)</b>이 지금까지 배운 범위입니다.${nxt ? ` 다음 단원: ${esc2(nxt.nm)} (10년 ${nxt.n}문항, 비중 ${lvOf(nxt.n)})` : ""}</span></div>
   ${L <= m.dataThrough && units.some(x => x.lec <= L && !exOfU(sub, x.u).length && !oxOfU(sub, x.u).length) ? `<div class="warnbox">수강한 단원 중 아직 기출이 들어 있지 않은 단원이 있어요. Claude에게 "${m.name} ○○ 단원 들었어"라고 알려 주시면 그 단원 기출을 해설과 함께 추가합니다. 그 전까지는 문제가 있는 단원에서만 냅니다.</div>` : ""}
   ${L > m.dataThrough ? `<div class="warnbox">문제는 ${m.stepLabel === "강" ? m.dataThrough + "강" : esc2(m.lectures[m.dataThrough - 1])}까지 들어 있어요. Claude에게 "${m.name} ${m.stepLabel === "강" ? L + "강" : "○○ 단원"}까지 들었어"라고 알려 주시면 그 범위 기출을 해설과 함께 추가합니다.</div>` : ""}
   ${grps.map(g => { const us = units.filter(u => u.grp === g), n = us.reduce((a, b) => a + b.n, 0); return `<h2 class="sec">${g} · 10년 ${n}문항 (${Math.round(n / all * 100)}%)</h2><ul class="units">${us.map(x => unitRow(sub, x, false)).join("")}</ul>` }).join("")}`;
  const step = d => { const nl = Math.max(1, Math.min(m.lectures.length, L + d)); if (nl === L) return; setLec(sub, nl); const e = entry(sub); if (e && !(e.res || []).filter(Boolean).length) delete S.daily[day][sub]; touch(); render() };
  $("#lm").onclick = () => step(-1); $("#lp").onclick = () => step(1);
  $("#foot").textContent = (m.mapNote || "") + " 진도를 바꾸면 아직 한 문제도 안 푼 오늘 세트는 새 범위로 다시 만들어집니다.";
}

/* ───────── 개념정리 ───────── */
function noteOf(sub, q) {
  const m = D[sub].meta; if (!m.notes) return "";
  const u = q.t === "ex" ? D[sub].ex[q.k].u : q.t === "ox" ? D[sub].oxBy[q.id].u : q.u;
  return (D[sub].ub[u] || {}).note || "";
}
function drawSeg() {
  const sub = V.sub, m = D[sub].meta, sm = summary(sub), seg = $("#seg"); seg.hidden = false;
  const onNote = V.tab === "note";
  seg.innerHTML = `<button role="tab" aria-selected="${onNote}" data-go="note">1 개념정리<small>${m.notes ? "결론 · 그래프 · 함정 · 기출" : "준비 중"}</small></button><button role="tab" aria-selected="${!onNote}" data-go="daily">2 문제풀이<small>오늘 ${sm.done}/${sm.total}</small></button>`;
  seg.querySelectorAll("button").forEach(b => b.onclick = () => { if ((b.dataset.go === "note") !== onNote) go(`#/s/${sub}/${b.dataset.go}`) });
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
  const t = localStorage.getItem(LS_THEME) || "auto";
  if (t === "auto") doc.documentElement.removeAttribute("data-theme"); else doc.documentElement.dataset.theme = t;
  if (!doc.getElementById("appStyle")) {
    const st = doc.createElement("style"); st.id = "appStyle";
    st.textContent = `header .eyebrow,header h1{display:none}.appgo{display:flex;flex-wrap:wrap;gap:8px;margin:4px 0 0}.appgo button{font:500 14px var(--f-body);padding:8px 14px;border-radius:8px;border:1px solid var(--accent);background:var(--accent);color:var(--accent-ink);cursor:pointer}.appgo button.gh{background:transparent;color:var(--accent)}`;
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
  for (const [sec, us] of Object.entries(bySec)) {
    const el = doc.getElementById(sec); if (!el) continue;
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
    : `'공식' = 큐넷 최종정답, '자체 풀이' = 정답 파일이 없어 직접 푼 정답.`;
  if (!V.Q.length) { m.innerHTML = `<section class="card"><p class="exp">풀 문제가 없어요. 진도를 확인해 주세요.</p></section>`; return }
  if (answered() >= V.Q.length || V.idx >= V.Q.length) { tmStop(); saveTimer(); tmDraw(); return result() }
  if (V.idx < 0) V.idx = nextUn(-1);
  progressNav();
  if (tmPaused()) {
    tmDraw();
    m.innerHTML = `<section class="card"><div class="qhead"><span class="qno">일시정지</span><span class="tag">${answered()} / ${V.Q.length} 풀이</span></div>
      <p class="exp">문제는 가려 두었어요. 남은 시간 <b>${fmt(Math.max(0, tmLimit() - tmUsed()))}</b>${tmLimit() < tmUsed() ? " (제한시간 초과)" : ""} 그대로 멈춰 있습니다.</p>
      <div class="row"><button class="btn" id="resume">▶ 이어서 풀기</button></div></section>`;
    $("#resume").onclick = () => { T.paused = false; tmGo(); saveTimer(); render() }; return;
  }
  if (timed()) tmGo(); tmDraw();
  const q = V.Q[V.idx], no = `Q${String(V.idx + 1).padStart(2, "0")} / ${V.Q.length}`;
  let html;
  if (q.t === "ox") {
    const b = D[sub].oxBy[q.id], un = D[sub].ub[b.u];
    html = `<section class="card q"><div class="qhead"><span class="qno">${no}</span><span class="tags"><span class="tag">O·X · ${esc2(un ? un.nm : "")}</span></span></div>
      <p class="stem">${b.s}</p><div class="ox"><button data-v="1" aria-label="O 맞다">O</button><button data-v="0" aria-label="X 틀리다">X</button></div>`;
  } else if (q.t === "ex") {
    const x = D[sub].ex[q.k];
    const tag = x.gen ? `<span class="tag gen">보충 문제 · 기출 아님</span>` : `<span class="tag exb">기출 · 제${x.y}회(${x.yr}) ${x.n}번${x.old ? " · 구 기준" : ""}</span>`;
    html = `<section class="card q"><div class="qhead"><span class="qno">${no}</span><span class="tags">${tag}${q.after ? '<span class="tag">방금 지문이 나온 문제</span>' : ""}</span></div>
      <p class="stem">${x.q}</p>
      ${x.fig ? `<div class="fig">${x.fig}</div>` : ""}
      ${x.tbl ? `<div class="tblw"><table class="tbl">${x.tbl.map((r, i) => `<tr>${r.map(c => i ? `<td>${c}</td>` : `<th>${c}</th>`).join("")}</tr>`).join("")}</table></div>` : ""}
      ${x.box ? `<div class="box">${x.box.map(b => `<p>${b.t}</p>`).join("")}</div>` : ""}
      ${x.h && !V.res[V.idx] ? `<button class="hintbtn" id="hintBtn">힌트 보기</button><p class="hint" id="hint" hidden>${x.h}</p>` : ""}
      <ul class="opts">${x.o.map((t, i) => `<li><button data-v="${i}"><span class="n">${N5[i]}</span><span>${t}</span></button></li>`).join("")}</ul>`;
  } else {
    const un = D[sub].ub[q.u];
    html = `<section class="card q"><div class="qhead"><span class="qno">${no}</span><span class="tag">5지선다 · 개념 O·X로 구성</span></div>
      <p class="stem">${esc2(un ? un.nm : "")}에 관한 설명으로 <b>${q.neg ? "옳지 않은" : "옳은"}</b> 것은?</p>
      <ul class="opts">${q.opts.map((id, i) => `<li><button data-v="${i}"><span class="n">${N5[i]}</span><span>${D[sub].oxBy[id].s}</span></button></li>`).join("")}</ul>`;
  }
  const r = V.res[V.idx], nx = nextUn(V.idx);
  if (r) html += `<p class="done-note">이미 푼 문제 · 내 답 ${q.t === "ox" ? (r.v ? "O" : "X") : N5[r.v]} (${r.ok ? "정답" : "오답"}) <button class="btn ghost sm" id="review">해설 보기</button></p>`;
  html += `</section><div class="qnav"><button class="btn ghost" id="prevQ" ${V.idx === 0 ? "disabled" : ""}>◀ 이전</button>${nx >= 0 && nx !== V.idx ? `<button class="btn ghost" id="skipQ">${r ? "다음 안 푼 문제" : "건너뛰기"} ▶</button>` : ""}</div>`;
  m.innerHTML = html;
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
    if (answered() >= V.Q.length) tmStop();
    if (V.mode === "daily") {
      const e = entry(sub); e.res = V.res; e.t = Date.now(); e.tm = { used: tmUsed(), paused: false };
      (S.days[day] = S.days[day] || {})[sub] = { done: answered(), ok: V.res.filter(r => r && r.ok).length, total: V.Q.length };
    }
    touch(); stats(); progressNav();
  }
  const nx = nextUn(V.idx), last = nx < 0;
  $("#sheet").className = "sheet " + (ok ? "good" : "bad");
  $("#sheet").innerHTML = `<div class="verdict"><span class="mark">${ok ? "O" : "X"}</span><span id="vtext">${ok ? "정답입니다" : "오답입니다"}</span></div>${html}
    <div class="row"><button class="btn" id="next">${review ? "닫기" : last ? "결과 보기" : "다음 문제"}</button>${noteOf(sub, q) ? `<button class="notelink" id="toNote">개념정리에서 보기</button>` : ""}</div>`;
  $("#modal").hidden = false; $("#sheet").scrollTop = 0; $("#next").focus({ preventScroll: true });
  $("#next").onclick = () => { closeModal(); if (!review) V.idx = last ? V.Q.length : nx; render(); scrollTo({ top: 0 }) };
  if ($("#toNote")) $("#toNote").onclick = () => { closeModal(); if (!review) V.idx = last ? V.Q.length : nx; tmStop(); T.paused = timed(); saveTimer(); go(`#/s/${sub}/note/${noteOf(sub, q)}`) };
}
function linkLine(b) {
  if (!b || !b.links) return "";
  const lab = s => { const [k, o] = s.split(" "), [y, n] = k.split("-"); return `제${y}회 ${n}번${o ? " " + o : ""}` };
  return `<p class="point">기출 출제 · ${b.links.map(lab).join(", ")}</p>`;
}
function closeModal() { $("#modal").hidden = true }
document.addEventListener("keydown", e => { if (!$("#modal").hidden && (e.key === "Enter" || e.key === "Escape")) { e.preventDefault(); $("#next").click() } });
$("#modal").addEventListener("click", e => { if (e.target.id === "modal") $("#next").click() });

function result() {
  const sub = V.sub, n = V.res.filter(r => r && r.ok).length, wr = V.Q.map((q, i) => ({ q, r: V.res[i] })).filter(x => x.r && !x.r.ok);
  const item = ({ q }) => {
    if (q.t === "ex") { const x = D[sub].ex[q.k], t = plain(x.q); return `<li>${x.gen ? "보충 문제" : `제${x.y}회 ${x.n}번`} · ${esc2(t.length > 60 ? t.slice(0, 60) + "…" : t)}<span>정답 ${N5[x.a - 1]} · ${plain(x.e[x.a - 1])}</span></li>` }
    const b = D[sub].oxBy[q.t === "ox" ? q.id : q.key]; return `<li>${b.s}<span>정답 ${b.a ? "O" : "X"} · ${b.e}</span></li>`;
  };
  $("#progress").hidden = true;
  $("#main").innerHTML = `<section class="card"><div class="qhead"><span class="qno">결과</span><span class="tag">${V.mode === "daily" ? "오늘 세트 완료" : "완료"}</span></div>
    <div class="score">${n}<small> / ${V.Q.length}</small></div>
    ${timed() ? `<p class="note">걸린 시간 ${fmt(tmUsed())} / 제한 ${fmt(tmLimit())}${V.res.some(r => r && r.late) ? ` · 제한시간 지나서 푼 문제 ${V.res.filter(r => r && r.late).length}개` : " · 제한시간 안에 완료"}</p>` : ""}
    ${wr.length ? `<ul class="wrong">${wr.map(item).join("")}</ul>` : `<p class="exp">모두 맞혔습니다.</p>`}
    <div class="row">${wr.length ? `<button class="btn" id="retry">틀린 문제 다시 풀기</button>` : ""}${V.mode === "daily" || V.mode === "extra" ? `<button class="btn ghost" id="extra">추가 ${DAILY_N}문제</button>` : ""}<button class="btn ghost" id="home">홈으로</button></div></section>`;
  if ($("#retry")) $("#retry").onclick = () => { V.Q = wr.map(x => x.q); V.res = []; V.idx = 0; V.mode = "retry"; render() };
  if ($("#extra")) $("#extra").onclick = () => { V.key = ""; go(`#/s/${sub}/daily/extra`) };
  $("#home").onclick = () => go("#/");
}

/* ───────── 타이머 ───────── */
const tmLimit = () => V.Q.length * SEC_PER_Q * 1000;
const tmUsed = () => T.used + (T.run ? Date.now() - T.run : 0);
function tmStop() { if (T.run) { T.used += Date.now() - T.run; T.run = 0 } }
function tmGo() { if (!T.run && !T.paused && answered() < V.Q.length) T.run = Date.now() }
const tmPaused = () => timed() && T.paused;
const fmt = ms => { const s = Math.floor(Math.abs(ms) / 1000); return `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}` };
function saveTimer() { if (V.route === "subject" && V.mode === "daily") { const e = entry(V.sub); if (e) { e.tm = { used: tmUsed(), paused: T.paused }; e.t = Date.now(); touch() } } }
function tmDraw() {
  const bar = $("#timerbar");
  if (!timed() || !V.Q.length || answered() >= V.Q.length || V.idx >= V.Q.length) { bar.hidden = true; return }
  bar.hidden = false;
  const left = tmLimit() - tmUsed(), over = left < 0; bar.classList.toggle("over", over);
  if (!$("#tmBtn")) {
    bar.innerHTML = `<span class="tt" id="tmT"></span><span class="tl" id="tmL"></span><button id="tmBtn"></button>`;
    $("#tmBtn").onclick = () => { if (T.paused) { T.paused = false; tmGo() } else { tmStop(); T.paused = true } saveTimer(); render() };
  }
  $("#tmT").textContent = (over ? "+" : "") + fmt(left);
  $("#tmL").textContent = T.paused ? "일시정지 중" : over ? `제한 ${fmt(tmLimit())} 초과 · 남은 문제는 계속 풀 수 있어요` : `남은 시간 · 제한 ${fmt(tmLimit())}`;
  $("#tmBtn").textContent = T.paused ? "▶ 계속" : "⏸ 일시정지";
}
setInterval(() => { if (timed()) tmDraw() }, 1000);
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
  chrome({ back: { label: "홈", hash: "#/" }, eyebrow: "감정평가사 1차 · 문제풀이", title: "설정" });
  const theme = localStorage.getItem(LS_THEME) || "auto";
  $("#main").innerHTML = `
  <section class="card"><h2 class="sec" style="margin:0">기기 간 동기화 (GitHub 비공개 저장소)</h2>
    <p class="exp" style="font-size:14.5px">휴대폰과 PC 기록을 잇는 설정이에요. 기기마다 <b>한 번씩</b> 입력하면 됩니다. 입력한 토큰은 이 기기 안에만 저장돼요.</p>
    <div class="form">
      <label>GitHub 아이디<small>github.com 오른쪽 위 프로필 사진을 누르면 보이는 이름</small><input id="fOwner" autocomplete="off" autocapitalize="off" spellcheck="false" value="${esc2(SY.owner || "")}"></label>
      <label>기록 저장소 이름<small>비공개(Private)로 만든 저장소</small><input id="fRepo" autocomplete="off" autocapitalize="off" spellcheck="false" value="${esc2(SY.repo || "dora-exam-records")}"></label>
      <label>토큰<small>github_pat_ 로 시작하는 긴 글자</small><input id="fToken" type="password" autocomplete="off" spellcheck="false" value="${esc2(SY.token || "")}"></label>
      <div class="row"><button class="btn" id="fSave">연결하고 동기화</button>${syncOn() ? `<button class="btn ghost" id="fOff">이 기기 연결 끊기</button>` : ""}</div>
      <p class="msg ${syncState.status === "ok" ? "ok" : syncState.status === "err" ? "err" : ""}" id="fMsg">${syncOn() ? (syncState.msg || (syncState.status === "ok" ? "연결됨 · 마지막 동기화 " + new Date(syncState.at).toLocaleTimeString("ko-KR") : "연결 정보가 저장돼 있어요.")) : "아직 연결 전이에요."}</p>
    </div></section>
  <section class="card"><h2 class="sec" style="margin:0">화면</h2>
    <div class="form"><label>밝기<select id="fTheme"><option value="auto">기기 설정 따르기</option><option value="light">밝게</option><option value="dark">어둡게</option></select></label></div></section>
  <section class="card"><h2 class="sec" style="margin:0">기록 백업</h2>
    <p class="exp" style="font-size:14.5px">기록을 파일로 내려받거나, 내려받은 파일을 불러와 합칠 수 있어요(기존 기록은 지워지지 않고 합쳐집니다).</p>
    <div class="row"><button class="btn ghost" id="fExport">기록 내려받기</button><label class="btn ghost" style="cursor:pointer">기록 불러오기<input type="file" id="fImport" accept="application/json,.json" hidden></label></div></section>
  <p class="note">앱 버전 ${APP_VER} · 문제 회계 ${D.acct ? D.acct.exam.length + D.acct.ox.length : 0}개, 경제 ${D.econ ? D.econ.exam.length : 0}개</p>`;
  $("#fTheme").value = theme;
  $("#fTheme").onchange = e => { localStorage.setItem(LS_THEME, e.target.value); applyTheme() };
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
function applyTheme() { const t = localStorage.getItem(LS_THEME) || "auto"; if (t === "auto") document.documentElement.removeAttribute("data-theme"); else document.documentElement.dataset.theme = t }

/* ───────── 시작 ───────── */
(async function init() {
  applyTheme();
  try { await loadData() } catch (e) { $("#title").textContent = "문제를 불러오지 못했어요"; $("#main").innerHTML = `<p class="exp">인터넷 연결을 확인하고 다시 열어 주세요. (${esc2(e.message)})</p>`; return }
  S = loadLocal();
  if (!S || !S.hist) { S = blank(); try { S = merge(S, await getJSON("data/migrate.json")) } catch (e) { } saveLocal() }
  S.daily = S.daily || {}; S.days = S.days || {}; S.subjects = S.subjects || {};
  route();
  if (syncOn()) syncNow();
  if ("serviceWorker" in navigator && location.protocol === "https:") navigator.serviceWorker.register("sw.js").catch(() => { });
})();
