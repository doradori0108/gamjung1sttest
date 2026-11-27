"""Helpers to add exam items to data/<sid>/exam.json for civil/re/law."""
import json, re, sys, os
sys.path.insert(0, '/home/claude/three'); sys.path.insert(0, os.path.dirname(__file__))
from keys3 import K
import parse as _P
_P.DESPACE=True
from parse import parse
REFIX={'개 념':'개념','자 연 적 ㆍ 인 문 적':'자연적ㆍ인문적','정 착 물':'정착물','등 기부등 본 을 통 해':'등기부등본을 통해','임야 의':'임야의','임야 도의 축척 은':'임야도의 축척은','등록 되는':'등록되는','사 정하며':'사정하며','전환 이':'전환이','부동산상 품':'부동산상품','이용실 익':'이용실익'}
REPO = '/home/claude/gamjung1sttest/data/'
SID = {'civ': 'civil', 're': 're', 'law': 'law'}
YR = {y: 1989 + y for y in range(28, 38)}  # 28회=2017
IMG = json.load(open(os.path.join(os.path.dirname(__file__), 'img_q.json'))) if os.path.exists(os.path.join(os.path.dirname(__file__), 'img_q.json')) else {}
_cache = {}

def load(sub):
    sid = SID[sub]
    if sid not in _cache:
        p = REPO + sid + '/exam.json'
        _cache[sid] = json.load(open(p))
    return _cache[sid]

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def key(sub, y, n):
    i = n - 81 if sub == 're' else n - 1
    return K[sub][y][i]

NEG = re.compile(r'옳지 않은|아닌 것|않는 것|틀린 것|해당하지 않는|없는 것|되지 않는|성립하지 않는|인정되지 않는|명시되지 않은')

def Q(sub, k, u, e, p=None, h=None, note=None, box=None, fix=None, alt=None, why=None, old=None, q=None, o=None, s=None):
    """e: list of 5 explanations ('맞다. ..'/'틀리다. ..').
    box: list of (bool, expl) matching parsed ㄱㄴㄷ items, or list of (text, bool, expl) for image years.
    fix: dict of text replacements applied to q/o/box texts."""
    y, n = map(int, k.split('-'))
    if q is None and y in (32, 33, 34):
        R = IMG[f'{sub}{y}-{n}']
        q, o, btxt = R['stem'], R['o'], R['box']
    elif q is None:
        P = parse(sub, y, n)
        assert P and 'err' not in P, (sub, k, P)
        q, o, btxt = P['stem'], P['o'], P['box']
    else:
        btxt = [b[0] for b in box] if box else None
        if o is None:
            if y in (32, 33, 34): o = IMG[f'{sub}{y}-{n}']['o']
            else: o = parse(sub, y, n)['o']
    def fx(t):
        for a, b in list(REFIX.items())+list((fix or {}).items()):
            t = t.replace(a, b)
        return t
    if not box and btxt and btxt[0][:15] not in q:
        q = q + ' ' + ' '.join(btxt)  # 판단 대상이 아닌 ○·ㄱ 목록은 발문에 붙인다
    q = fx(q); o = [fx(x) for x in o]
    a = key(sub, y, n)
    item = dict(k=k, y=y, yr=YR[y], n=n, u=u, src='공식', q=esc(q), o=[esc(x) for x in o])
    if box:
        if btxt and len(box[0]) == 2:
            assert len(btxt) == len(box), (k, len(btxt), len(box), btxt)
            item['box'] = [dict(t=esc(fx(t)), a=bool(b[0]), e=b[1]) for t, b in zip(btxt, box)]
        else:
            item['box'] = [dict(t=esc(fx(b[0])), a=bool(b[1]), e=b[2]) for b in box]
    assert len(e) == 5, k
    if a == 0:
        assert alt and why, ('전항 정답', k)
        a = alt[0]
    if isinstance(a, list):
        alt = alt or a; a = a[0]
    item['a'] = a
    item['e'] = e
    if alt: item['alt'] = alt
    if why: item['why'] = why
    if p: item['p'] = p
    if h: item['h'] = h
    if s: item['s'] = s
    if note: item['note'] = note
    if old: item['old'] = True
    # sanity: marker of answer option
    if not box:
        neg = bool(NEG.search(q))
        m = e[a - 1]
        want = '틀리다' if neg else '맞다'
        if not m.startswith(want):
            print('CHECK marker', sub, k, 'neg' if neg else 'pos', m[:20])
    L = load(sub)
    L[:] = [x for x in L if x['k'] != k]
    L.append(item)
    return item

def save():
    for sid, L in _cache.items():
        L.sort(key=lambda x: (x['y'], x['n']))
        json.dump(L, open(REPO + sid + '/exam.json', 'w'), ensure_ascii=False, indent=1)
        print(sid, len(L))

def show(sub, *ks):
    for k in ks:
        y, n = map(int, k.split('-'))
        P = IMG[f'{sub}{y}-{n}'] if y in (32,33,34) else parse(sub, y, n)
        print('=====', k, '정답', key(sub, y, n))
        print('Q', P.get('stem'))
        if P.get('box'):
            for b in P['box']: print('  ', b)
        for i, x in enumerate(P.get('o', [])): print(' ', '①②③④⑤'[i], x)
