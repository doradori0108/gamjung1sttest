import json
R='/home/claude/gamjung1sttest/'
OUT={}
def load(sub):
    if sub not in OUT: OUT[sub]=json.load(open(R+f'data/{sub}/sent.json'))
    return OUT[sub]
def s(sub,u,src,ctx,text,a,plain,terms,e,fix=''):
    assert a or fix, text
    L=load(sub)
    assert not any(x['s']==text for x in L), 'dup '+text[:30]
    x=dict(u=u,src=src,ctx=ctx,s=text,a=a,plain=plain,terms=terms,e=e,fix=fix,id=max([y['id'] for y in L]+[0])+1)
    L.append(x); return x
def save():
    for sub,L in OUT.items():
        assert all(x is not None for x in L)
        json.dump(L,open(R+f'data/{sub}/sent.json','w'),ensure_ascii=False,indent=1); print(sub,len(L))
