import json
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="pv"' not in h
sec='''<!-- 15. 충당부채 · 보고기간후사건 -->
<section id="pv" class="sec" aria-labelledby="h-pv">
  <div class="shead"><h2 id="h-pv">충당부채 · 보고기간후사건</h2><span class="badge hi">비중 상 · 12문항</span><span class="lec">15단원</span></div>
  <div class="key">충당부채 = ① 과거사건으로 생긴 현재의무 ② 유출 가능성 높음 ③ 금액 신뢰성 있는 추정. 셋 다면 부채로, 하나라도 빠지면 우발부채(주석).<small>현재의무 판단 기준 한 줄: '회사가 앞으로 무엇을 하든 피할 수 없는가?' 피할 수 있으면(미래 영업·정비·교육) 의무 아님.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1~2문항. ① 이론 O·X(28·29·33·36회) ② 여러 사건 중 충당부채 금액 고르기(28회 48번 · 32회 58번 · 35회 56번) ③ 제품보증 계산(32회 70번 · 34회 55번 · 36회 60번) ④ 보고기간후사건 수정/비수정(28회 45번 · 30회 56번)</p>

  <h3>① 인식 판단표</h3>
  <div class="tw c1"><table>
    <thead><tr><th>유출 가능성 ＼ 금액 추정</th><th>신뢰성 있게 추정 가능</th><th>추정 불가</th></tr></thead>
    <tbody>
      <tr><td>높음(50% 초과)</td><td><b>충당부채 인식</b></td><td>우발부채(주석)</td></tr>
      <tr><td>높지 않음</td><td>우발부채(주석)</td><td>우발부채(주석)</td></tr>
      <tr><td>아주 낮음</td><td colspan="2">공시도 안 함</td></tr>
    </tbody>
  </table></div>
  <div class="tw c1"><table>
    <thead><tr><th>상황</th><th>충당부채?</th><th>기출</th></tr></thead>
    <tbody>
      <tr><td>복구의무(법·협약), 이미 오염 + 법 제정 거의 확실</td><td>O</td><td>28-48 · 32-58 · 35-56 ㄷ</td></tr>
      <tr><td>의제의무(정화 방침 공표·준수)</td><td>O</td><td>35-56 ㄹ</td></tr>
      <tr><td>제품보증(확신유형) · 손실부담계약</td><td>O</td><td>32-70 · 36-59 ②</td></tr>
      <tr><td>구조조정: 이행 착수 또는 공표 후</td><td>O (계획만이면 X)</td><td>32-58</td></tr>
      <tr><td>미래 영업손실 · 교육훈련 · 정기 대수리·정비 · 여과장치 설치</td><td><b>X</b></td><td>28-48 · 29-58 · 35-56 ㄱㄴ</td></tr>
      <tr><td>패소 가능성 높지 않은 소송</td><td>X(우발부채)</td><td>32-58</td></tr>
    </tbody>
  </table></div>

  <h3>② 측정 규칙</h3>
  <div class="grid2">
    <div class="mini"><h3>금액</h3><p>최선의 추정치(다수 = 기댓값, 34회 55번: 100 × 10% + 4,000 × 5% = 210) · 현재가치(할인율 <b>세전</b>) · 측정도 <b>세전</b> · 자산 처분이익 고려 X.</p></div>
    <div class="mini"><h3>변제(보험금 등)</h3><p>받을 것이 거의 확실할 때만 <b>별도 자산</b>(한도 = 충당부채). 손익계산서에서는 비용과 상계 가능, 재무상태표에서는 상계 X.</p></div>
  </div>

  <div class="lab">
    <h3>제품보증 충당부채 · 2년 보증</h3>
    <div class="slider"><label for="pv1">1년차 매출</label><input type="range" id="pv1" min="0" max="400000" step="10000" value="200000"><output id="pv1Out">200000</output></div>
    <div class="slider"><label for="pv2">2년차 매출</label><input type="range" id="pv2" min="0" max="400000" step="10000" value="250000"><output id="pv2Out">250000</output></div>
    <div class="readout" id="pvOut" aria-live="polite"></div>
  </div>
  <p class="foot">36회 60번 숫자: 추정률 5% · 6%, 실제 발생 1년차분 2,500 + 3,000, 2년차분 4,000. 판매연도별로 '예상 − 실제'를 구해 더한다.</p>

  <h3>③ 보고기간후사건(12/31 ~ 발행승인일)</h3>
  <div class="tw c1"><table>
    <thead><tr><th>수정(장부 금액 고침)</th><th>비수정(주석)</th></tr></thead>
    <tbody>
      <tr><td>결산일에 있던 소송의 판결 확정 · 상여금 확정 · 결산 전 거래 금액 확정 · 결산일 거래처 파산 확인 · 부정·오류 발견</td><td>화재 · 새 보증계약 · 결산 후 <b>배당 선언</b> · 투자자산 공정가치 하락 · 대규모 매입</td></tr>
    </tbody>
  </table></div>
  <p class="foot">예외: 보고기간 후 청산·영업중단을 결정하면 계속기업 가정 자체를 쓰지 않는다(28회 45번 ⑤). 도로공사 비유: 준공검사 전(결산일)에 있던 하자가 나중에 확인되면 준공서류를 고치지만, 준공 후 새로 난 사고는 별도 보고.</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>정기 대수리·정비를 충당부채로(28회 48번 · 35회 56번 ㄱ).</span>
    <span>"우발부채는 인식" / "한 번 우발부채면 계속 우발부채" → X(36회 59번 · 28회 70번).</span>
    <span>세후 금액 측정 → X. 세전(33회 54번).</span>
    <span>보험사 변제를 충당부채에서 차감 → X(32회 58번: 보증 350,000 전액).</span>
    <span>복구원가를 명목금액으로 넣는다. 현재가치(32회 58번: 120,000).</span>
    <span>결산 후 배당 선언을 부채로 → X(28회 45번).</span>
    <span>2년 보증에서 전년도 판매분 잔액을 빼먹는다(32회 70번 · 36회 60번).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>판단표 · 보증 계산 · 수정/비수정 구분은 매년 나오는 쉬운 점수. 구조조정 충당부채에 포함할 원가 세부, 충당부채 할인의 이자비용(복구원가는 유형자산 단원과 겹침)은 과락 회피 목표라면 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#cb">전환사채·BW</a>','<a href="#cb">전환사채·BW</a><a href="#pv">충당부채</a>',1)
h=h.replace('["전환사채·신주인수권부사채","#cb","14단원",10,"hi"],','["전환사채·신주인수권부사채","#cb","14단원",10,"hi"],["충당부채·보고기간후사건","#pv","15단원",12,"hi"],',1)
a='      <tr data-sec="cb"><td>CB 전환 vs BW 행사</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="pv"><td>충당부채 3요건</td><td>현재의무(피할 수 없나) · 유출 가능성 높음 · 신뢰성 있는 추정 / 미래 영업·정비 X</td></tr>
      <tr data-sec="pv"><td>보고기간후사건</td><td>결산일 상황 증거 = 수정 / 새 사건(화재·배당 선언·FV 하락) = 주석</td></tr>
'''+h[j:]
js='''
/* 15. 제품보증 */
function pvCalc(){const s1=+$("#pv1").value,s2=+$("#pv2").value;$("#pv1Out").textContent=s1;$("#pv2Out").textContent=s2;
 const e1=s1*.05,e2=s2*.06,u1=2500+3000,u2=4000,r1=Math.max(0,e1-u1),r2=Math.max(0,e2-u2);
 $("#pvOut").innerHTML=`1년차분: 예상 ${w(e1)} − 실제 ${w(u1)} = ${w(r1)} · 2년차분: 예상 ${w(e2)} − 실제 ${w(u2)} = ${w(r2)}<br>2년차 말 제품보증충당부채 <b>${w(r1+r2)}</b> (실제가 예상보다 많으면 0으로 보고 초과분은 비용)`}
["pv1","pv2"].forEach(i=>$("#"+i).addEventListener("input",pvCalc));pvCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='PV': x['note']='pv'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
