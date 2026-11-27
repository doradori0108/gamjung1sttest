import re,sys,json
out={}
for y in [28,29,30,31,35,36,37]:
    t=open(f'{y}.txt',encoding='utf-8',errors='ignore').read()
    m=re.search(r'회 *계 *학\s*\n(?:.*\n){0,12}?\s*41\s*\.',t); i=m.start() if m else 0
    t=t[i:]
    parts=re.split(r'\n\s*(\d{2})\s*\.\s', '\n'+t)
    qs={}
    for k in range(1,len(parts)-1,2):
        n=int(parts[k]); 
        if 41<=n<=80 and n not in qs: qs[n]=parts[k+1]
    out[y]=qs
    hits=[n for n,s in qs.items() if re.search('투자부동산|생물자산|농림어업|수확물|농산물|공정가치모형|임대', re.sub(r'\s','',s))]
    print(y,len(qs),hits)
json.dump(out,open('qs.json','w'),ensure_ascii=False)
