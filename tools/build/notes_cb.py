import json
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="cb"' not in h
sec='''<!-- 14. 복합금융상품 -->
<section id="cb" class="sec" aria-labelledby="h-cb">
  <div class="shead"><h2 id="h-cb">복합금융상품(전환사채 · 신주인수권부사채)</h2><span class="badge hi">비중 상 · 10문항</span><span class="lec">14단원</span></div>
  <div class="key">발행가를 '부채'와 '권리(자본)'로 쪼갠다. 부채 = 미래 현금흐름 ÷ 일반사채 시장이자율, 나머지 = 전환권(신주인수권)대가. 이후 부채는 13단원 사채와 똑같이 상각한다.<small>전환사채(CB) = 사채를 주식으로 '바꾸는' 권리 → 전환하면 사채가 사라짐. 신주인수권부사채(BW) = 돈을 더 내고 주식을 '사는' 권리 → 행사해도 사채는 남음.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1문항, 전부 계산. ① 전환권대가(30회 61번) ② 상환할증금(34회 50번) ③ 이자비용(28회 64번 · 33회 52번 · 36회 58번) ④ 전환 시 주발초(29회 53번 · 31회 65번) ⑤ 전환 시 자본증가(32회 49번) ⑥ BW 행사 후 주발초·이자비용(35회 52번 · 37회 53번)</p>

  <div class="lab">
    <h3>쪼개기 실습 · 액면발행 · 3년 · 매년 말 이자</h3>
    <div class="slider"><label for="cb1">표시이자율(%)</label><input type="range" id="cb1" min="0" max="10" step="1" value="6"><output id="cb1Out">6</output></div>
    <div class="slider"><label for="cb2">시장이자율(%)</label><input type="range" id="cb2" min="4" max="14" step="1" value="10"><output id="cb2Out">10</output></div>
    <div class="slider"><label for="cb3">상환할증(액면 대비 %)</label><input type="range" id="cb3" min="0" max="15" step="0.5" value="0"><output id="cb3Out">0</output></div>
    <div class="readout" id="cbOut" aria-live="polite"></div>
  </div>
  <p class="foot">기본값은 30회 61번(A): 액면 500,000을 100이라 보면 전환권대가 ≈ 9.9%. 상환할증을 6.5%로 올리면 B(≈ 5.1%)에 가까워진다.</p>

  <h3>단계별 공식</h3>
  <div class="tw c1"><table>
    <thead><tr><th>단계</th><th>공식</th><th>함정</th></tr></thead>
    <tbody>
      <tr><td>상환할증금</td><td>(보장수익률 − 표시이자율) × 액면 × 보장수익률 연금 미래가치</td><td>시장이자율 X(34-50)</td></tr>
      <tr><td>부채요소</td><td>(액면 + 할증금) × 단일현가 + 표시이자 × 연금현가 @ <b>일반사채 시장이자율</b></td><td>표시·보장수익률로 할인 X</td></tr>
      <tr><td>전환권대가</td><td>발행가 − 부채요소 (자본)</td><td>할증 있으면 작아짐(30-61)</td></tr>
      <tr><td>이자비용</td><td>기초 부채 × 시장이자율 · 총액 = 총지급 − 최초 부채</td><td>표시이자 X(36-58 ①)</td></tr>
      <tr><td>CB 전환</td><td>주발초 = 전환분 부채 − 액면 + 전환권대가 × 비율</td><td>전환권대가 대체 누락(29-53 ③)</td></tr>
      <tr><td>CB 전환 자본증가</td><td>전환분 부채 장부금액만</td><td>전환권대가는 이미 자본(32-49)</td></tr>
      <tr><td>BW 행사</td><td>주발초 = 현금 − 액면 + 대가 × 비율 + 행사분 할증금 현가</td><td>사채는 남는다(35-52)</td></tr>
      <tr><td>BW 행사 후 이자</td><td>(기초 부채 − 행사분 할증금 현가) × 시장이자율</td><td>할증금 감소 누락(37-53 ⑤)</td></tr>
    </tbody>
  </table></div>
  <ol class="steps">
    <li>29회 53번: 부채 = 1,198,600 × 0.7118 + 50,000 × 2.4018 = 973,253 → 전환권대가 26,747</li>
    <li>20×2년 말 부채 1,114,849. 40% 전환 → 부채 445,940, 주식 200주 × 1,000 = 자본금 200,000</li>
    <li>주발초 = 445,940 − 200,000 + 26,747 × 40% = <b>256,638</b></li>
  </ol>
  <div class="grid2">
    <div class="mini"><h3>CB 전환</h3><p>부채(사채 + 할증금) 소멸 → 자본금 + 주발초. 돈이 들어오지 않는다.</p></div>
    <div class="mini"><h3>BW 행사</h3><p>행사가격만큼 현금 유입 → 자본금 + 주발초. 사채는 그대로, 할증금만 줄어든다.</p></div>
  </div>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>부채요소를 표시이자율이나 보장수익률로 할인한다. 일반사채 시장이자율(30회 61번).</span>
    <span>상환할증금을 시장이자율로 계산한다. 보장수익률(34회 50번).</span>
    <span>전환 시 주발초에서 전환권대가 대체분을 뺀다(29회 53번 · 31회 65번).</span>
    <span>전환으로 자본이 '부채 + 전환권'만큼 는다고 본다. 부채만(32회 49번).</span>
    <span>BW 행사 후에도 할증금 부채를 그대로 둔다(37회 53번).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>쪼개기(부채 현가 → 전환권대가)와 전환 시 주발초는 매년 나오니 반드시. 전환사채 조기상환(공정가치로 부채·자본 배분), 유도전환, 분리형 BW는 과락 회피 목표라면 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#fl">금융부채(사채)</a>','<a href="#fl">금융부채(사채)</a><a href="#cb">전환사채·BW</a>',1)
h=h.replace('["금융부채(사채)","#fl","13단원",12,"hi"],','["금융부채(사채)","#fl","13단원",12,"hi"],["전환사채·신주인수권부사채","#cb","14단원",10,"hi"],',1)
a='      <tr data-sec="fl"><td>조기상환</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="cb"><td>전환사채 쪼개기</td><td>부채 = (액면 + 할증금)·이자 현가 @ 일반사채 이자율 · 나머지 = 전환권대가(자본)</td></tr>
      <tr data-sec="cb"><td>CB 전환 vs BW 행사</td><td>CB: 부채 → 자본(현금 X) / BW: 현금 유입, 사채 남음, 할증금만 감소</td></tr>
'''+h[j:]
js='''
/* 14. 전환사채 쪼개기 */
function cbCalc(){const c=+$("#cb1").value/100,r=+$("#cb2").value/100,pr=+$("#cb3").value/100;["cb1","cb2","cb3"].forEach(i=>$("#"+i+"Out").textContent=$("#"+i).value);
 const F=100;let L=F*(1+pr)/(1+r)**3;for(let t=1;t<=3;t++)L+=F*c/(1+r)**t;const eq=F-L;
 $("#cbOut").innerHTML=`액면 100 기준 → 부채요소 <b>${L.toFixed(2)}</b> · 전환권대가 <b>${eq.toFixed(2)}</b>${eq<0?" (음수: 조건이 시장보다 유리 → 현실적으로 성립 X)":""}<br>상환할증을 올리면 부채↑ 전환권대가↓ · 시장이자율을 올리면 부채↓ 전환권대가↑`}
["cb1","cb2","cb3"].forEach(i=>$("#"+i).addEventListener("input",cbCalc));cbCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='CB': x['note']='cb'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
