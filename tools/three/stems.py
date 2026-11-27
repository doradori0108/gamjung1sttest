import re,json,sys
def stems(path,lo,hi):
    t=open(path).read()
    out={}
    for n in range(lo,hi+1):
        m=re.search(rf'(?m)^\s*\|?\s*{n}\s*\.\s*(.*?)(?=^\s*\|?\s*①|\Z)',t,re.S)
        if m: out[n]=re.sub(r'\s+',' ',m.group(1).replace('|',' '))[:160]
    return out
R={}
for y in ['28','29','30','31','35','36','37']:
    R['civ'+y]=stems(f'/home/claude/econsrc/e{y}.txt',1,40)
    R['re'+y]=stems(f'/home/claude/econsrc/e{y}.txt',81,120)
    R['law'+y]=stems(f'/home/claude/src/{y}.txt',1,40)
json.dump(R,open('stems.json','w'),ensure_ascii=False,indent=0)
for k,v in R.items(): print(k,len(v),[n for n in range(1,121) if (n in range(1,41) and not k.startswith('re') or n in range(81,121) and k.startswith('re')) and n not in v])
