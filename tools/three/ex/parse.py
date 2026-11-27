"""Parse text-year exam blocks into stem / box / options."""
import re, sys, json
sys.path.insert(0, '/home/claude/three')
from qx import block

CIRC = '①②③④⑤'

def clean(t):
    t = re.sub(r'A-\d+-\d+-\[\d교시\]', ' ', t)
    t = re.sub(r'[\u0000-\u0008\u000b-\u001f]', ' ', t)
    t = re.sub(r'[ഀĀྠɌ]+', ' ', t)
    t = re.sub(r'\[표\]', ' ', t)
    t = re.sub(r'\n\s*\|\s*', '\n', t)
    t = re.sub(r'\s*\|\s*\n', '\n', t)
    t = t.replace('|', ' ')
    return t

import os
V = json.load(open(os.path.join(os.path.dirname(__file__), 'vocab.json')))
def _k(w): return re.sub(r'[^\w가-힣]', '', w)
def joinlines(t):
    lines = [l.strip() for l in t.split('\n')]
    out = ''
    for l in lines:
        if not l: continue
        if not out: out = l; continue
        a = out.split()[-1] if out.split() else ''
        b = l.split()[0]
        ka, kb = _k(a), _k(b)
        hangul = bool(re.search(r'[가-힣]$', a)) and bool(re.match(r'^[가-힣]', b))
        if hangul and V.get(ka + kb, 0) > 0 and not re.match(r'^[ㄱ-ㅎ①-⑤]', b):
            out += l
        else:
            out += ' ' + l
    return out
def despace(t):
    toks = t.split(' ')
    out = []
    i = 0
    while i < len(toks):
        cur = toks[i]
        while i + 1 < len(toks):
            nxt = toks[i + 1]
            a, b = _k(cur), _k(nxt)
            if a and b and (len(a) == 1 or len(b) == 1) and re.fullmatch(r'[가-힣]+', a) and re.fullmatch(r'[가-힣]+', b) \
               and V.get(a + b, 0) > max(V.get(a, 0), V.get(b, 0)) / 50 and not (len(a)==1 and V.get(a,0)>200 and len(b)>1 and V.get(b,0)>50):
                cur = cur + nxt; i += 1
            else:
                break
        out.append(cur); i += 1
    return ' '.join(out)
def squash(t):
    t = joinlines(t)
    t = re.sub(r'\s{2,}', ' ', t)
    # Korean word broken across line: keep as-is (spaces); fix common split "옳 은"
    return t.strip()

DESPACE = False
def parse(s, y, n):
    b = block(s, y, n)
    if b is None:
        return None
    b = clean(b)
    b = re.sub(rf'^\s*{n}\s*\.\s*', '', b)
    # options
    idx = [b.find(c) for c in CIRC]
    if any(i < 0 for i in idx) or idx != sorted(idx):
        return {'raw': b, 'err': 'opts'}
    head = b[:idx[0]]
    opts = [squash(b[idx[i] + 1: idx[i + 1] if i < 4 else len(b)]) for i in range(5)]
    # strip trailing junk after option 5 (page footers / next subject headers)
    opts[4] = re.split(r'\s(?:경 제 학|경제학원론|회 계 학|※ 아래의)', opts[4])[0].strip()
    box = None
    m = re.search(r'(?m)(^|\s)ㄱ\s*\.', head)
    if m:
        stem = head[:m.start()]
        rest = head[m.start():]
        parts = re.split(r'\s*(?=(?:^|\s)[ㄱㄴㄷㄹㅁㅂㅅ]\s*\.)', rest)
        box = [squash(p) for p in parts if squash(p)]
    else:
        stem = head
    stem = squash(stem)
    if DESPACE:
        stem = despace(stem); opts = [despace(o) for o in opts]
        box = [despace(b) for b in box] if box else box
    return {'stem': stem, 'box': box, 'o': opts}

if __name__ == '__main__':
    s = sys.argv[1]
    for k in sys.argv[2:]:
        y, n = map(int, k.split('-'))
        print(k, json.dumps(parse(s, y, n), ensure_ascii=False, indent=1))
