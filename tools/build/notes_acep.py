import json,re
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="ac"' not in h and 'id="ep"' not in h and not re.search(r'id="es\d|esOut|function esCalc',h)
sec='''<!-- 22. 회계변경·오류수정 -->
<section id="ac" class="sec" aria-labelledby="h-ac">
  <div class="shead"><h2 id="h-ac">회계변경 · 오류수정</h2><span class="badge lo">비중 하 · 2문항</span><span class="lec">22단원</span></div>
  <div class="key">정책을 바꾸면 과거도 고친다(소급법), 추정을 바꾸면 지금부터(전진법), 오류는 처음부터 없었던 것처럼(소급 재작성).<small>소급법 = 과거 재무제표를 새 방법으로 다시 작성. 전진법 = 과거는 두고 변경 시점부터 적용.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 단독 출제는 드물고(28·32회), 재고자산·투자부동산 문제 안에 '회계변경 후 이익' 형태로 섞여 나온다(32-67, 37-66).</p>
  <div class="tw c1"><table>
    <thead><tr><th>구분</th><th>예</th><th>처리</th></tr></thead>
    <tbody>
      <tr><td>회계정책 변경</td><td>재고 평균법 → 선입선출법, 투자부동산 원가 → 공정가치모형, 측정기준 변경</td><td>소급법(누적효과는 기초 이익잉여금)</td></tr>
      <tr><td>회계추정 변경</td><td>내용연수·잔존가치·감가상각방법, 손실충당금 추정</td><td>전진법. 구분이 어려우면 <b>추정의 변경</b>으로</td></tr>
      <tr><td>중요한 전기오류</td><td>처분한 자산을 장부에 남겨 둠(32-68)</td><td>소급 재작성. 사후 판단 금지</td></tr>
    </tbody>
  </table></div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>측정기준 변경을 추정의 변경으로(28-60 ①).</span>
    <span>구분이 어려우면 정책의 변경으로(28-60 ⑤) → 추정.</span>
    <span>전기오류의 영향을 발견 연도 당기손익에 넣음(32-68: 20×3년 당기순이익 영향 없음).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>위 표 하나로 충분. 자동조정오류·비자동조정오류 세부 계산은 넘긴다.</span></div>
  <p class="mine"></p>
</section>

<!-- 23. 주당이익 -->
<section id="ep" class="sec" aria-labelledby="h-ep">
  <div class="shead"><h2 id="h-ep">주당이익(EPS)</h2><span class="badge hi">비중 상 · 10문항</span><span class="lec">23단원</span></div>
  <div class="key">기본주당이익 = (당기순이익 − 우선주배당) ÷ 가중평균유통보통주식수. 시험의 80%는 분모(가중평균 주식 수) 계산이고, 핵심은 '싸게 한 유상증자 안의 무상증자 요소'.<small>가중평균유통보통주식수 = 주식 수 × 유통된 개월 ÷ 12를 더한 것. 무상증자·주식분할은 기초부터 있었던 것으로 본다.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1문항. ① 가중평균유통보통주식수(32·33·35회) ② 기본주당이익(29·30회) ③ 역산(31회 순이익, 34회 우선주배당) ④ 희석주당이익 순서·반희석(29·36회) ⑤ O·X(37회)</p>
  <div class="lab">
    <h3>유상증자 무상 요소 계산기 · 33회 62번 기본값</h3>
    <div class="slider"><label for="es1">기초 유통보통주식수</label><input type="range" id="es1" min="1000" max="20000" step="100" value="1600"><output id="es1Out">1600</output></div>
    <div class="slider"><label for="es2">유상증자 주식 수</label><input type="range" id="es2" min="0" max="5000" step="100" value="600"><output id="es2Out">600</output></div>
    <div class="slider"><label for="es3">발행금액 ÷ 공정가치(%)</label><input type="range" id="es3" min="40" max="100" step="5" value="65"><output id="es3Out">65</output></div>
    <div class="slider"><label for="es4">유상증자 월(1~12월 초)</label><input type="range" id="es4" min="1" max="12" step="1" value="7"><output id="es4Out">7</output></div>
    <div class="readout" id="esOut" aria-live="polite"></div>
  </div>
  <p class="foot">33-62는 발행가 400 ÷ 공정가치 600 = 66.7%라 실습 값(65%)과 조금 다르다. 답은 1,600 × 1.1 + 400 × 1.1 × 6/12 = 1,980.</p>
  <ol class="steps">
    <li>공정가치 발행분 = 유상증자 주식 수 × 발행금액 ÷ 공정가치. 나머지 = 무상분</li>
    <li>무상증자비율 = 무상분 ÷ (증자 전 주식 + 공정가치 발행분)</li>
    <li>증자 전에 있던 주식(기초·전환분 포함)에 (1 + 비율)을 곱하고, 공정가치 발행분은 납입일부터 × (1 + 비율)</li>
    <li>자기주식은 취득일부터 빼고, 무상증자·주식분할은 원구주를 따라 소급</li>
    <li>분자: 누적적 우선주는 올해분 배당을 무조건 차감(밀린 전년도분은 빼지 않음, 29-55)</li>
  </ol>
  <div class="grid2">
    <div class="mini"><h3>희석주당이익 순서</h3><p>증분 주당이익(늘어나는 이익 ÷ 늘어나는 주식)이 <b>작은 것부터</b> 넣고, 넣었는데 EPS가 오르면 그 증권부터 제외(36-63: 옵션 0 → BW 50 → 전환우선주 1,900 → 전환사채 2,833은 반희석 → 2,400).</p></div>
    <div class="mini"><h3>희석 ≤ 기본</h3><p>희석주당이익은 기본주당이익보다 클 수 없다. 29-55: 전환 가정 41.96 &gt; 기본 35 → 반희석이라 답 35.</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>유상증자 주식 전부를 납입일부터 셈(무상 요소 무시, 33-62 ③ 1,800).</span>
    <span>4월 무상증자를 4월부터 셈(기초부터 소급, 31-63 · 35-47).</span>
    <span>우선주에 대한 무상증자를 보통주 수에 넣음(34-46).</span>
    <span>희석 순서를 큰 것부터(37-57 ②).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>분모 계산 5단계만 확실히. 조건부발행보통주·매입옵션·중단영업 EPS 구분은 과락 회피 목표라면 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#tx">법인세</a>','<a href="#tx">법인세</a><a href="#ac">회계변경</a><a href="#ep">주당이익</a>',1)
h=h.replace('["법인세","#tx","21단원",8,"mid"],','["법인세","#tx","21단원",8,"mid"],["주당이익","#ep","23단원",10,"hi"],["회계변경·오류수정","#ac","22단원",2,"lo"],',1)
a='      <tr data-sec="tx"><td>법인세비용</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="ac"><td>회계변경</td><td>정책 = 소급(측정기준 변경 포함) · 추정 = 전진(구분 어려우면 추정) · 오류 = 소급 재작성</td></tr>
      <tr data-sec="ep"><td>가중평균 주식 수</td><td>무상·분할 = 기초부터 · 싼 유상증자 = 공정가치 발행분(납입일부터) + 무상분(소급) · 희석은 증분 EPS 작은 것부터</td></tr>
'''+h[j:]
js='''
/* 23. 가중평균유통보통주식수 */
function esCalc(){const b=+$("#es1").value,n=+$("#es2").value,q=+$("#es3").value/100,m=+$("#es4").value;["es1","es2","es3","es4"].forEach(i=>$("#"+i+"Out").textContent=$("#"+i).value);
 const fv=n*q,bon=n-fv,r=bon/(b+fv),mo=13-m,tot=b*(1+r)+fv*(1+r)*mo/12;
 $("#esOut").innerHTML=`공정가치 발행분 ${w(Math.round(fv))}주 · 무상분 ${w(Math.round(bon))}주 → 비율 ${(r*100).toFixed(1)}%<br>${w(b)} × ${(1+r).toFixed(3)} + ${w(Math.round(fv))} × ${(1+r).toFixed(3)} × ${mo}/12 = <b>${w(Math.round(tot))}주</b>`}
["es1","es2","es3","es4"].forEach(i=>$("#"+i).addEventListener("input",esCalc));esCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='AC': x['note']='ac'
    if x['u']=='EP': x['note']='ep'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
