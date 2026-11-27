P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="cost"' not in h
sec='''<!-- 비용이론 -->
<section id="cost" class="sec" data-lec="22" aria-labelledby="h-cost">
  <div class="shead"><h2 id="h-cost">비용이론 · 비용극소화</h2><span class="badge hi">비중 상 · 14문항</span><span class="lec">22~23강</span></div>
  <div class="key">비용곡선은 생산함수를 뒤집어 본 것이다. 한계생산이 줄면 한계비용이 오르고, 규모수익이 체증이면 장기평균비용이 내려간다.<small>한계비용(MC) = 1개 더 만들 때 느는 비용 · 평균비용(AC) = 총비용 ÷ 생산량 · AFC = 고정비 ÷ 생산량 · AVC = 가변비 ÷ 생산량.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1~2문항. ① 비용곡선 모양 O·X(29·30·35회) ② 비용함수에서 AC·MC 계산(31회 42번) ③ 생산함수 → 비용함수(29회 57번 · 35회 57번) ④ 비용극소화 요소 묶음(31회 45번 · 33회 42번 · 35회 54번) ⑤ 장기비용과 규모수익(31회 57번 · 36회 52번)</p>

  <div class="lab">
    <h3>단기 비용곡선 · 고정비용을 바꿔 보세요</h3>
    <div class="slider"><label for="cs1">고정비용 FC</label><input type="range" id="cs1" min="0" max="120" step="5" value="40"><output id="cs1Out">40</output></div>
    <svg id="svgCost" viewBox="0 0 340 250" role="img" aria-label="한계비용, 평균비용, 평균가변비용, 평균고정비용 곡선"></svg>
    <div class="readout" id="csOut" aria-live="polite"></div>
  </div>
  <p class="foot">파랑 = MC, 주황 = AC, 초록 = AVC, 점선 = AFC. 고정비용을 올려도 MC는 그대로, AC만 위로 · 최저점은 오른쪽으로 간다(30회 48번 ㄴ).</p>

  <div class="tw c1"><table>
    <thead><tr><th>외울 관계</th><th>이유 · 기출</th></tr></thead>
    <tbody>
      <tr><td>MC &lt; AC → AC↓ · MC &gt; AC → AC↑</td><td>평균 점수와 새 점수(29회 45번 ②)</td></tr>
      <tr><td>MC는 AVC · AC의 <b>최저점</b>을 아래→위로 통과</td><td>주어가 MC(35회 53번 ㄷ)</td></tr>
      <tr><td>AC − AVC = AFC → Q↑이면 간격 좁아짐</td><td>30회 48번 ㄷ</td></tr>
      <tr><td>AC 최저점은 AVC 최저점보다 오른쪽</td><td>AC↑ 구간이면 AVC도 ↑(30회 48번 ㄹ)</td></tr>
      <tr><td>MC는 고정비용과 무관</td><td>30회 48번 ㄴ</td></tr>
    </tbody>
  </table></div>

  <h3>비용극소화 = 1원당 한계생산을 같게</h3>
  <div class="tw c1"><table>
    <thead><tr><th>생산함수</th><th>최소 비용 요소 묶음</th><th>기출</th></tr></thead>
    <tbody>
      <tr><td>콥-더글러스 L<sup>α</sup>K<sup>β</sup></td><td>MRTS = (α/β)(K/L) = w/r (접점)</td><td>35회 54번: K/L = 12/24 → L = 2K</td></tr>
      <tr><td>완전대체 aL + bK</td><td>a/w와 b/r 중 큰 쪽 <b>하나만</b>(모서리해)</td><td>31회 45번: 8/5 &gt; 4/3 → K만 15</td></tr>
      <tr><td>max{2x<sub>1</sub>, x<sub>2</sub>}</td><td>C = min{w<sub>1</sub>/2, w<sub>2</sub>}Q</td><td>29회 57번</td></tr>
      <tr><td>완전보완 min{L/a, K/b}</td><td>L = aQ, K = bQ → C = (aw + br)Q (가격 무관하게 꺾인 점)</td><td>32회 50번 · 33회 42번</td></tr>
      <tr><td>공장 2개</td><td>MC<sub>1</sub> = MC<sub>2</sub></td><td>30회 55번: 2q<sub>1</sub> = 2 → (1, 4)</td></tr>
    </tbody>
  </table></div>
  <ol class="steps">
    <li>31회 60번형: MP<sub>K</sub> = 2MP<sub>L</sub>, w = 8, r = 4 → 1원당 MP: 자본 2/4 &gt; 노동 1/8</li>
    <li>→ 자본을 늘리고 노동을 줄이면 같은 양을 더 싸게. 한계생산 체감으로 결국 두 값이 같아질 때까지</li>
  </ol>

  <h3>장기비용 = 규모수익의 거울</h3>
  <div class="grid2">
    <div class="mini"><h3>규모수익 체증(α + β &gt; 1)</h3><p>규모의 경제 · LAC 우하향 · LMC &lt; LAC (36회 52번 ④)</p></div>
    <div class="mini"><h3>불변(= 1)</h3><p>LAC 수평 = LMC. 값은 A·요소가격으로 정해짐("1로 일정"은 X, 36회 52번 ①) · 31회 57번 ③</p></div>
  </div>
  <p class="foot">도로공사 비유: 현장사무소·장비 리스료(고정비)는 공사량이 늘수록 1m당 부담이 줄고(AFC↓), 인력만 계속 투입하면 작업 공간이 비좁아져 1m 더 까는 비용이 오른다(MC↑).</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>"평균비용이 하락할 때 MC &gt; AC" → X. 하락 중이면 MC &lt; AC(29회 45번).</span>
    <span>"AC가 MC의 최저점에서 교차" → X. MC가 AC의 최저점을 지난다(35회 53번).</span>
    <span>평균비용 = 총비용곡선의 접선 기울기 → X. 원점에서 그은 직선의 기울기(30회 48번).</span>
    <span>완전보완형에서 요소가격을 보고 한쪽을 더 쓴다. 가격과 무관하게 꺾인 점(33회 42번).</span>
    <span>생산함수를 L로 풀지 않고 가격을 곱한다. L = Q²/16 먼저(35회 57번).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>쌍대성(비용함수 ↔ 생산함수 수식 증명), 확장경로의 수식 유도는 출제 없음. 위 두 표와 실습 그래프만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#pf">생산함수</a>','<a href="#pf">생산함수</a><a href="#cost">비용이론</a>',1)
h=h.replace('["생산함수·규모수익","#pf","20~21강",9,"mid","앱에서 표시"]','["생산함수·규모수익","#pf","20~21강",9,"mid","앱에서 표시"],["비용이론·비용극소화","#cost","22~23강",14,"hi","앱에서 표시"]',1)
a='      <tr data-sec="pf"><th>콥-더글러스</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="cost"><th>평균-한계</th><td>MC &lt; AC → AC↓ · MC는 AVC·AC 최저점 통과 · AC − AVC = AFC</td></tr>
      <tr data-sec="cost"><th>비용극소화</th><td>MP<sub>L</sub>/w = MP<sub>K</sub>/r · 완전대체 = 싼 요소 하나 · 완전보완 = 꺾인 점</td></tr>
'''+h[j:]
js='''
/* 비용이론: 단기 비용곡선 */
function drawCost(){const FC=+$("#cs1").value;$("#cs1Out").textContent=FC;const svg=$("#svgCost"),p=plot(svg,10,60,"Q","비용");
 const VC=q=>20*q-4*q*q+0.4*q*q*q,MC=q=>20-8*q+1.2*q*q,AVC=q=>VC(q)/q,AC=q=>(FC+VC(q))/q,AFC=q=>FC/q;
 const path=(fn,cls,dash)=>{let d="";for(let q=0.3;q<=10.001;q+=0.1){const y=fn(q);d+=(d?"L":"M")+p.X(q).toFixed(1)+" "+p.Y(Math.min(y,80)).toFixed(1)}el(p.g,"path",{d,class:cls,style:dash||""})};
 path(MC,"d");path(AC,"s");path(AVC,"g");if(FC>0)path(AFC,"guide");
 let qa=0.3,ma=1e9;for(let q=0.3;q<=10;q+=0.01){if(AC(q)<ma){ma=AC(q);qa=q}}
 el(p.g,"circle",{cx:p.X(qa),cy:p.Y(ma),r:4,fill:"var(--supply)"});el(p.g,"circle",{cx:p.X(5),cy:p.Y(AVC(5)),r:4,fill:"var(--gov)"});
 $("#csOut").innerHTML=`AVC 최저점: Q = 5, ${f(AVC(5),1)} (FC와 무관) · AC 최저점: Q = ${f(qa,1)}, ${f(ma,1)} — 이 점에서 MC = ${f(MC(qa),1)} ≈ AC`}
$("#cs1").addEventListener("input",drawCost);drawCost();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
import json
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=23
for x in u['units']:
    if x['u']=='U11': x['note']='cost'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
