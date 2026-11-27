import json
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="rv"' not in h
sec='''<!-- 17. 수익 -->
<section id="rv" class="sec" aria-labelledby="h-rv">
  <div class="shead"><h2 id="h-rv">수익(고객과의 계약 · 건설계약)</h2><span class="badge hi">비중 상 · 18문항</span><span class="lec">17단원</span></div>
  <div class="key">수익 = 5단계(계약 → 수행의무 → 거래가격 → 배분 → 인식). 시험은 5단계 이론 O·X와 특수 거래(포인트·반품·재매입·건설계약) 계산 두 종류.<small>수행의무 = 고객에게 넘기기로 한 약속 하나하나. 통제가 넘어갈 때(한 시점) 또는 넘어가는 만큼(기간에 걸쳐) 수익.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 2문항 안팎. ① 5단계 이론(32·33·34·35회) ② 포인트(32·34·36회) ③ 재매입약정(31·33·37회) ④ 반품(37회 58번) ⑤ 건설계약 이익·계약자산(28·30·34·37회) ⑥ 유의적 금융요소(31회 54번)</p>

  <h3>① 5단계 · 두문자 '계·수·거·배·인'</h3>
  <div class="tw c1"><table>
    <thead><tr><th>단계</th><th>핵심</th><th>함정</th></tr></thead>
    <tbody>
      <tr><td>1 계약 식별</td><td>승인(서면·구두·관행) · 권리 · 지급조건 · <b>상업적 실질</b> · 회수 가능성 높음</td><td>"상업적 실질 불필요" X(32-61)</td></tr>
      <tr><td>2 수행의무</td><td>구별되는 약속마다. 관행으로 생긴 암묵적 약속 포함</td><td>"계약서 기재분만" X(34-63)</td></tr>
      <tr><td>3 거래가격</td><td>변동대가: 결과 다수 = 기댓값, 둘 = 최빈값 · 제3자 대신 받는 돈 제외 · 유의적 금융요소</td><td>"둘이면 기댓값" X(32-51)</td></tr>
      <tr><td>4 배분</td><td>상대적 개별 판매가격(잔여법 가능)</td><td></td></tr>
      <tr><td>5 인식</td><td>통제 이전 시점 / 기간에 걸쳐(동시 소비·고객 자산 증대·대체 용도 없고 지급청구권)</td><td></td></tr>
    </tbody>
  </table></div>

  <h3>② 특수 거래</h3>
  <div class="tw c1"><table>
    <thead><tr><th>거래</th><th>처리</th><th>기출</th></tr></thead>
    <tbody>
      <tr><td>고객충성 포인트</td><td>배분액 이연 → 수익 = 배분액 × 사용분/예상 사용 총량</td><td>32-48 · 34-53 · 36-64</td></tr>
      <tr><td>반품권</td><td>예상 반품분: 매출 대신 <b>환불부채</b>, 원가 대신 <b>반환제품회수권</b>(손상·반품비용 차감)</td><td>37-58</td></tr>
      <tr><td>재매입(회사 콜옵션)</td><td>고객 통제 X → 재매입가 ≥ 판매가 = 금융약정, &lt; = 리스</td><td>33-55</td></tr>
      <tr><td>재매입(고객 풋옵션)</td><td>행사 유인 유의 + 재매입가 ≥ 판매가 = 금융약정 · 유인 없으면 반품권 판매</td><td>31-60 · 37-59</td></tr>
      <tr><td>위탁판매</td><td>수탁자가 팔 때 수익. 적송운임은 원가에 포함</td><td>32-63</td></tr>
      <tr><td>선수금 + 금융요소</td><td>계약부채에 이자 가산 → 이전 시 수익(31-54: 100,000 → 121,000)</td><td>31-54 · 33-58 ②</td></tr>
    </tbody>
  </table></div>

  <div class="lab">
    <h3>건설계약 진행기준 · 37회 60번 기본값(원가 기준으로 바꿔 보기)</h3>
    <div class="slider"><label for="rv1">계약금액(만 원)</label><input type="range" id="rv1" min="80" max="160" step="5" value="120"><output id="rv1Out">120</output></div>
    <div class="slider"><label for="rv2">1년차 진행률(%)</label><input type="range" id="rv2" min="5" max="60" step="5" value="20"><output id="rv2Out">20</output></div>
    <div class="slider"><label for="rv3">2년차 누적 진행률(%)</label><input type="range" id="rv3" min="10" max="95" step="5" value="50"><output id="rv3Out">50</output></div>
    <div class="slider"><label for="rv4">2년차 추정 총원가(만 원)</label><input type="range" id="rv4" min="60" max="180" step="5" value="100"><output id="rv4Out">100</output></div>
    <div class="readout" id="rvOut" aria-live="polite"></div>
  </div>
  <p class="foot">1년차 추정 총원가는 80만 원으로 고정. 당기 이익 = 누적 이익 − 전기까지 이익. 총원가가 계약금액을 넘으면 손실 전액을 즉시 인식(손실부담). 도로공사 기성 비유: 공정률만큼 기성금(수익)을 잡고, 청구액보다 많으면 미청구공사(계약자산).</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>당기 공사이익을 누적이익으로 답한다(30-51 · 37-60).</span>
    <span>계약자산·부채를 '회수액'과 비교. <b>청구액</b>과 비교(34-56).</span>
    <span>진행률 기준을 문제에서 바꿔 준다(37-60 노동시간). 원가로 계산하면 오답.</span>
    <span>포인트 수익 분모를 '부여 총량'으로. <b>사용 예상 총량</b>(36-64: 9,000).</span>
    <span>반품 예상 원가를 그대로 자산으로. 손상·반품비용을 뺀다(37-58).</span>
    <span>재매입을 판매로 처리(37-59 ⑤ · 33-55).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>5단계 표·포인트·건설계약은 매년 점수. 계약변경 회계처리, 라이선스(접근권·사용권), 본인 vs 대리인 세부, 고객에게 지급할 대가, 보증의 용역유형 구분은 과락 회피 목표라면 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#eq">자본</a>','<a href="#eq">자본</a><a href="#rv">수익</a>',1)
h=h.replace('["재고자산","#iv","4단원",31,"hi"],','["재고자산","#iv","4단원",31,"hi"],["수익(고객과의 계약·건설계약)","#rv","17단원",18,"hi"],',1)
a='      <tr data-sec="eq"><td>우선주 배당</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="rv"><td>수익 5단계</td><td>계·수·거·배·인 (계약 → 수행의무 → 거래가격 → 배분 → 인식)</td></tr>
      <tr data-sec="rv"><td>재매입약정</td><td>콜옵션: 재매입가 ≥ 판매가 금융약정 / 풋옵션: 유인 유의 + ≥ 판매가 금융약정, 유인 없으면 반품권</td></tr>
'''+h[j:]
js='''
/* 17. 건설계약 */
function rvCalc(){const T=+$("#rv1").value,p1=+$("#rv2").value/100,p2=+$("#rv3").value/100,C2=+$("#rv4").value;["rv1","rv2","rv3","rv4"].forEach(i=>$("#"+i+"Out").textContent=$("#"+i).value);
 const C1=80,pr1=(T-C1)*p1,cum2=T<C2?(T-C2):(T-C2)*p2,pr2=cum2-pr1;
 $("#rvOut").innerHTML=`1년차 이익 (${T} − ${C1}) × ${Math.round(p1*100)}% = <b>${f(pr1,1)}</b>만 원 · 2년차 누적 ${T<C2?"손실 전액 "+f(T-C2,1):"("+T+" − "+C2+") × "+Math.round(p2*100)+"% = "+f(cum2,1)} → 2년차 이익 <b>${f(pr2,1)}</b>만 원`}
["rv1","rv2","rv3","rv4"].forEach(i=>$("#"+i).addEventListener("input",rvCalc));rvCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='RV': x['note']='rv'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
