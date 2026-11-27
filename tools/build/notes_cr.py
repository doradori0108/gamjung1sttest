import re,json
P='/home/claude/gamjung1sttest/notes/acct.html'
h=open(P).read()
sec='''<!-- 11. 현금·수취채권 -->
<section id="cr" class="sec" aria-labelledby="h-cr">
  <div class="shead"><h2 id="h-cr">현금 · 수취채권</h2><span class="badge mid">비중 중 · 8문항</span><span class="lec">11단원</span></div>
  <div class="key">이 단원 시험은 세 가지뿐: ① 현금성자산이냐 아니냐 ② 은행계정조정 ③ 어음할인 손실 계산.<small>대손(기대신용손실)은 12단원 금융자산에서 함께 나온다. 현금·수취채권 단독 문제는 거의 매년 1문항.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · "현금및현금성자산이 아닌 것을 모두 고르면"(32회) · "회사 장부에 반영할 항목은"(33·34회) · "수정 전 잔액과 수정 후 잔액은"(30회) · "어음할인 처분손실은"(28·31·36회) · "할인율은"(30회)</p>

  <h3>① 현금성자산 판정: 3개월 · 가치변동 · 사용제한</h3>
  <div class="tw c1"><table>
    <thead><tr><th>항목</th><th>현금및현금성자산?</th><th>이유</th></tr></thead>
    <tbody>
      <tr><td>통화 · 타인발행수표 · 보통·당좌예금</td><td><b>O</b></td><td>바로 쓸 수 있다</td></tr>
      <tr><td>취득일부터 만기 3개월 이내 채권 · 정기예금</td><td><b>O</b></td><td>기준일은 <b>취득일</b>(결산일 아님)</td></tr>
      <tr><td>상환일 정해진 상환우선주를 상환일 3개월 이내에 취득</td><td><b>O</b></td><td>지분상품의 유일한 예외</td></tr>
      <tr><td>보통주(곧 팔 예정이어도)</td><td>X</td><td>만기 없음 · 가치변동 큼</td></tr>
      <tr><td>12개월 이상 사용 제한 예금</td><td>X</td><td>비유동 금융자산</td></tr>
      <tr><td>우표 · 수입인지</td><td>X</td><td>소모품(선급비용)</td></tr>
      <tr><td>자기주식</td><td>X</td><td>자본 차감</td></tr>
      <tr><td>당좌차월</td><td>X(부채)</td><td>단기차입금</td></tr>
    </tbody>
  </table></div>

  <h3>② 은행계정조정: "누가 모르나"로 쪽을 정한다</h3>
  <div class="tw c1"><table>
    <thead><tr><th>사건</th><th>모르는 쪽</th><th>조정</th></tr></thead>
    <tbody>
      <tr><td>기발행 미인출수표(회사가 써 준 수표를 아직 안 찾아감)</td><td>은행</td><td>은행 잔액 −</td></tr>
      <tr><td>미기입예금(회사가 마감 후 입금)</td><td>은행</td><td>은행 잔액 +</td></tr>
      <tr><td>추심어음 입금 · 이자수익 미통지</td><td>회사</td><td><b>회사 장부 +</b></td></tr>
      <tr><td>부도수표 · 은행수수료 · 차입금 이자 자동이체</td><td>회사</td><td><b>회사 장부 −</b></td></tr>
      <tr><td>회사 기장 오류(190을 910으로)</td><td>회사</td><td>회사 장부 ∓(차이 720)</td></tr>
    </tbody>
  </table></div>
  <p class="foot">회사 장부에 분개하는 것은 '회사 쪽' 항목뿐이다(33회 41번). 도로공사 기성금에 비유하면, 발주처가 지급했는데 아직 통보를 못 받은 돈은 '우리 장부'에 넣고, 우리가 하도급사에 끊어 준 수표를 하도급사가 아직 안 찾아간 것은 '은행'만 모르는 일이다.</p>
  <ol class="steps">
    <li>은행 7,810,000 − 미인출수표 2,100,000 = <b>5,710,000</b>(올바른 잔액)</li>
    <li>회사 A − 부도 1,500,000 + 추심 500,000 − 기장오류 720,000 = 5,710,000</li>
    <li>A = <b>7,430,000</b> (30회 65번). 끝나면 양쪽이 같은지 검산</li>
  </ol>

  <div class="lab">
    <h3>③ 어음할인 계산기 · 슬라이더를 움직여 보세요</h3>
    <div class="slider"><label for="cr1">액면</label><input type="range" id="cr1" min="100000" max="1200000" step="10000" value="300000"><output id="cr1Out">300000</output></div>
    <div class="slider"><label for="cr2">표시이자율(%)</label><input type="range" id="cr2" min="0" max="12" step="1" value="5"><output id="cr2Out">5</output></div>
    <div class="slider"><label for="cr3">만기(개월)</label><input type="range" id="cr3" min="2" max="12" step="1" value="3"><output id="cr3Out">3</output></div>
    <div class="slider"><label for="cr4">보유(개월)</label><input type="range" id="cr4" min="1" max="11" step="1" value="1"><output id="cr4Out">1</output></div>
    <div class="slider"><label for="cr5">할인율(%)</label><input type="range" id="cr5" min="1" max="20" step="1" value="8"><output id="cr5Out">8</output></div>
    <div class="readout" id="crOut" aria-live="polite"></div>
  </div>
  <p class="ask">기본값은 28회 43번(정답: 할인액 4,050 · 손실 1,550). 표시이자율을 0으로 내리면 무이자부어음 → 손실 = 할인액.</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>할인액을 액면 기준으로 계산한다. 은행은 <b>만기금액</b>(액면 + 전체 이자)에 할인율을 곱한다(28회 43번 · 36회 56번).</span>
    <span>처분손실을 액면과 비교한다. 이자부어음은 <b>액면 + 보유기간 이자</b>가 장부금액(31회 44번 B).</span>
    <span>미인출수표를 회사 장부에서 뺀다. 은행 쪽이다(34회 49번 · 33회 41번).</span>
    <span>"1개월 내 처분 예정 보통주"를 현금성자산으로 고른다. 주식은 원칙적으로 X(32회 42번).</span>
    <span>만기 3개월을 결산일부터 센다. <b>취득일</b>부터다.</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>은행계정조정과 어음할인 계산은 매년 쉬운 점수라 반드시 잡는다. 받을어음 배서양도·소구의무, 매출채권 팩토링의 세부 분개, 대손 직접상각법은 과락 회피 목표라면 넘긴다(10년간 단독 출제 없음).</span></div>
  <p class="mine"></p>
</section>

'''
assert 'id="cr"' not in h
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#ip">투자부동산·생물자산</a>','<a href="#ip">투자부동산·생물자산</a><a href="#cr">현금·수취채권</a>',1)
h=h.replace('["재무제표 표시","#ps","3단원",9,"mid"]','["재무제표 표시","#ps","3단원",9,"mid"],["현금·수취채권","#cr","11단원",8,"mid"]',1)
card='''      <tr data-sec="cr"><td>현금성자산</td><td>취득일부터 3개월 · 주식 X(상환우선주만 예외) · 사용제한 X · 우표 X · 자기주식 X</td></tr>
      <tr data-sec="cr"><td>은행계정조정</td><td>미인출수표·미기입예금 = 은행 쪽 / 추심·부도·수수료·오기 = 회사 쪽(분개)</td></tr>
      <tr data-sec="cr"><td>어음할인</td><td>할인액 = 만기금액 × 할인율 × 남은기간 / 손실 = (액면 + 보유이자) − 현금</td></tr>
'''
h=h.replace('''      <tr><td>생물자산 · 수확물</td><td>순공정가치 · 당기손익 · 수확물은 어떠한 경우에도 순공정가치</td></tr>
''','''      <tr><td>생물자산 · 수확물</td><td>순공정가치 · 당기손익 · 수확물은 어떠한 경우에도 순공정가치</td></tr>
'''+card,1)
# generic header
h=re.sub(r'<div class="eyebrow">.*?</div>','<div class="eyebrow">감정평가사 1차 · 회계학 · 신은미 기본강의 · 수강한 단원까지 열림</div>',h,1)
h=re.sub(r'<p class="lede">.*?</p>','<p class="lede">제28~37회 회계학 400문항을 강의 순서 38단원으로 나눠 정리합니다. 단원마다 ‘결론 한 줄 → 도식 → 자주 틀리는 지점 → 관련 기출’ 순서이고, 목표가 과락 회피이므로 <b>버려도 되는 주제</b>를 따로 표시했습니다. 아직 수강 전인 단원은 앱의 🗺️ 진도를 올리면 열립니다.</p>',h,1,flags=re.S)
# lab script
js='''
/* 11. 어음할인 */
function crCalc(){const F=+$("#cr1").value,r=+$("#cr2").value/100,m=+$("#cr3").value;let k=+$("#cr4").value;if(k>=m){k=m-1;$("#cr4").value=k}const d=+$("#cr5").value/100;
 ["cr1","cr2","cr3","cr4","cr5"].forEach(i=>$("#"+i+"Out").textContent=$("#"+i).value);
 const M=F*(1+r*m/12),disc=M*d*(m-k)/12,cash=M-disc,bv=F+F*r*k/12,loss=bv-cash;
 $("#crOut").innerHTML=`① 만기금액 ${w(M)} → ② 할인액 ${w(M)} × ${d*100}% × ${m-k}/12 = <b>${w(disc)}</b> → ③ 받는 현금 ${w(cash)}<br>④ 장부금액 ${w(F)} + 보유이자 ${w(F*r*k/12)} = ${w(bv)} → ⑤ 처분${loss>=0?"손실":"이익"} <b>${w(Math.abs(loss))}</b>`}
["cr1","cr2","cr3","cr4","cr5"].forEach(i=>$("#"+i).addEventListener("input",crCalc));crCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'
u=json.load(open(U))
for x in u['units']:
    if x['u']=='CR': x['note']='cr'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1)
print('ok')
