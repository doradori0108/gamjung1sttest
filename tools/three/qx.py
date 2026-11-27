import re,sys,json
SRC={'civ':'/home/claude/econsrc/e{y}.txt','re':'/home/claude/econsrc/e{y}.txt','law':'/home/claude/src/{y}.txt'}
def block(s,y,n):
    t=open(SRC[s].format(y=y)).read()
    if s=='civ': t=t[:t.find('경제학원론') if '경제학원론' in t else len(t)]
    if s=='re': i=t.rfind('부동산학원론'); t=t[i:] if i>0 else t
    if s=='law': i=t.find('관계'); j=t.find('회계학',i+10); t=t[i:j if j>0 else len(t)]
    m=re.search(rf'(?m)^\s*{n}\s*\.\s',t)
    if not m: return None
    m2=re.search(rf'(?m)^\s*{n+1}\s*\.\s',t[m.end():])
    b=t[m.start(): m.end()+m2.start() if m2 else m.end()+3000]
    b=re.sub(r'\n.*\d{4}년도? 제\d+회.*\n','\n',b)
    return re.sub(r'[ \t]+',' ',b).strip()
if __name__=='__main__':
    s=sys.argv[1]
    for k in sys.argv[2:]:
        y,n=map(int,k.split('-')); print('=====',k); print(block(s,y,n))
