"""Store transcribed 32~34회 questions: I(key, stem, opts, box=None)."""
import json, os
P = os.path.join(os.path.dirname(__file__), 'img_q.json')
D = json.load(open(P)) if os.path.exists(P) else {}
def I(k, stem, o, box=None):
    assert len(o) == 5, k
    D[k] = dict(stem=stem, o=o, box=box)
def save():
    json.dump(D, open(P, 'w'), ensure_ascii=False, indent=1)
    print('img_q', len(D))
