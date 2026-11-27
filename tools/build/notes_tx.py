import json,re
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="tx"' not in h and not re.search(r"id=\"tq\d|tqOut|function tqCalc",h)
sec='''<!-- 21. 법인세 -->
<section id="tx" class="sec" aria-labelledby="h-tx">
  <div class="shead"><h2 id="h-tx">법인세(이연법인세)</h2><span class="badge mid">비중 중 · 8문항</span><span class="lec">21단원</span></div>
  <div class="key">법인세비용 = 당기법인세(과세소득 × 세율) ± 이연법인세 변동. 세율이 일정하면 지름길: <b>(세전이익 + 영구적차이) × 세율</b>.<small>일시적차이 = 회계와 세법의 시점만 다른 차이(나중에 반대로 풀림). 영구적차이 = 세법이 끝까지 인정 안 하는 차이(접대비·벌과금 한도초과).</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1문항 계산. ① 법인세비용(29·30·31·34·36회) ② 비용 + 이연법인세 잔액(28회, 세율 변경) ③ 유효세율(32회) ④ 미수이자 누락 오류 영향(33회)</p>
  <div class="tw c1"><table>
    <thead><tr><th>세무조정 항목</th><th>종류</th><th>이연</th></tr></thead>
    <tbody>
      <tr><td>감가상각비 한도초과 · 충당부채 · 손실충당금 한도초과</td><td>차감할 일시적차이(지금 세금 더 냄)</td><td><b>자산</b></td></tr>
      <tr><td>정기예금 미수이자 · FVPL 평가이익(세법 불인정)</td><td>가산할 일시적차이(나중에 더 냄)</td><td><b>부채</b></td></tr>
      <tr><td>접대비·벌과금 한도초과</td><td>영구적차이</td><td>없음</td></tr>
      <tr><td>자기주식처분이익(자본) · 재평가잉여금(OCI)</td><td>자본 항목</td><td>세효과를 자본에서 직접 차감(34-64)</td></tr>
    </tbody>
  </table></div>
  <div class="lab">
    <h3>법인세비용 계산기 · 31회 62번 기본값</h3>
    <div class="slider"><label for="tq1">세전이익</label><input type="range" id="tq1" min="100000" max="1000000" step="10000" value="490000"><output id="tq1Out">490000</output></div>
    <div class="slider"><label for="tq2">영구적차이(접대비 등)</label><input type="range" id="tq2" min="0" max="100000" step="5000" value="60000"><output id="tq2Out">60000</output></div>
    <div class="slider"><label for="tq3">차감할 일시적차이(감가상각 한도초과)</label><input type="range" id="tq3" min="0" max="300000" step="5000" value="125000"><output id="tq3Out">125000</output></div>
    <div class="slider"><label for="tq4">가산할 일시적차이(미수이자)</label><input type="range" id="tq4" min="0" max="150000" step="5000" value="25000"><output id="tq4Out">25000</output></div>
    <div class="slider"><label for="tq5">미래 세율(%)</label><input type="range" id="tq5" min="10" max="30" step="1" value="20"><output id="tq5Out">20</output></div>
    <div class="readout" id="tqOut" aria-live="polite"></div>
  </div>
  <p class="foot">당기 세율 20%, 설립 첫해(기초 이연법인세 0) 가정. 미래 세율을 25%로 올리면 28회 50번처럼 '풀릴 때 세율'로 이연을 잰다.</p>
  <ol class="steps">
    <li>과세소득 = 세전이익 + 가산조정 − 차감조정 → × 당기 세율 = 당기법인세</li>
    <li>기말 이연법인세 = 일시적차이 × <b>풀릴 때 세율</b> → 기초와의 차이가 이연법인세 변동</li>
    <li>법인세비용 = 당기법인세 − 이연자산 증가(+ 이연부채 증가) − 자본 항목 세효과</li>
  </ol>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>미수이자를 이연법인세'자산'으로(31-62, 33-59). 나중에 과세 → 부채.</span>
    <span>세율이 바뀌는데 당기 세율로 이연을 계산(28-50).</span>
    <span>미수이자 누락 오류에 '당기법인세' 영향을 고름(33-59). 영향은 이연부채 60 · 비용 60 · 순이익 140.</span>
    <span>자기주식처분이익 세효과를 비용에 남김(34-64).</span>
    <span>전기 일시적차이의 소멸(20×1 미수이자가 20×2 과세)을 빠뜨림(36-66).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>지름길 공식과 위 표만. 이연법인세자산 실현가능성 판단, 결손금 이월공제, 사업결합·종속기업 투자 관련 이연법인세는 과락 회피 목표라면 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#ls">리스</a>','<a href="#ls">리스</a><a href="#tx">법인세</a>',1)
h=h.replace('["리스","#ls","20단원",9,"mid"],','["리스","#ls","20단원",9,"mid"],["법인세","#tx","21단원",8,"mid"],',1)
a='      <tr data-sec="ls"><td>리스이용자</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'      <tr data-sec="tx"><td>법인세비용</td><td>당기법인세 ± 이연 변동 · 세율 일정이면 (세전이익 + 영구적차이) × 세율 · 미수이자 = 이연부채 · 한도초과 감가상각 = 이연자산</td></tr>\n'+h[j:]
js='''
/* 21. 법인세비용 */
function tqCalc(){const b=+$("#tq1").value,p=+$("#tq2").value,d=+$("#tq3").value,a=+$("#tq4").value,r=+$("#tq5").value/100;["tq1","tq2","tq3","tq4","tq5"].forEach(i=>$("#"+i+"Out").textContent=$("#"+i).value);
 const ti=b+p+d-a,cur=ti*.2,dta=d*r,dtl=a*r,exp=cur-dta+dtl;
 $("#tqOut").innerHTML=`과세소득 ${w(ti)} × 20% = 당기법인세 ${w(cur)}<br>이연자산 ${w(dta)} · 이연부채 ${w(dtl)} → 법인세비용 <b>${w(Math.round(exp))}</b> · 유효세율 ${(exp/b*100).toFixed(1)}%`}
["tq1","tq2","tq3","tq4","tq5"].forEach(i=>$("#"+i).addEventListener("input",tqCalc));tqCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='TX': x['note']='tx'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
