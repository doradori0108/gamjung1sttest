import json
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="mono"' not in h
sec='''<!-- 독점 -->
<section id="mono" class="sec" data-lec="26" aria-labelledby="h-mono">
  <div class="shead"><h2 id="h-mono">독점 · 가격차별 · 독점적 경쟁</h2><span class="badge hi">비중 상 · 21문항</span><span class="lec">26~27강</span></div>
  <div class="key">독점은 MR = MC에서 생산량을 정하고, 그 양을 수요곡선에 넣어 가격을 받는다. 그래서 P &gt; MC → 과소생산 · 자중손실.<small>직선 수요 P = a − bQ면 MR = a − 2bQ(기울기 2배). 가격차별은 손님별 가격을 달리해 소비자잉여를 더 가져가는 것.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 2문항 이상. ① 독점 생산량·가격·이윤 계산(29·34회) ② 가격차별 이론 O·X(30·34회) ③ 3급 가격차별 계산(36회 50번) ④ 독점적 경쟁 장기균형(34회 48번 · 37회 48번) ⑤ 자연독점 가격규제(35회 50·56번) ⑥ 탄력성과 MR(37회 49번)</p>

  <div class="lab">
    <h3>독점 vs 완전경쟁 · 수요 P = 100 − Q</h3>
    <div class="slider"><label for="mo1">한계비용 MC(일정)</label><input type="range" id="mo1" min="0" max="80" step="5" value="20"><output id="mo1Out">20</output></div>
    <svg id="svgMono" viewBox="0 0 340 250" role="img" aria-label="수요곡선, 한계수입곡선, 한계비용선과 독점가격, 자중손실 삼각형"></svg>
    <div class="readout" id="moOut" aria-live="polite"></div>
  </div>

  <h3>독점 계산 4단계</h3>
  <ol class="steps">
    <li>역수요로 바꾸기: Q = 100 − 2P → P = 50 − Q/2 (34회 47번)</li>
    <li>MR = 기울기 2배: MR = 50 − Q</li>
    <li>MR = MC: 50 − Q = 2Q + 20 → Q = 10 → 수요곡선에 넣어 P = 45</li>
    <li>이윤 = PQ − TC(고정비 포함) = 450 − 300 = <b>150</b></li>
  </ol>

  <h3>가격차별 3종</h3>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>방법</th><th>결과</th><th>예 · 기출</th></tr></thead>
    <tbody>
      <tr><td>1급(완전)</td><td>손님마다 최대 지불의사</td><td>생산량 = 완전경쟁 · 소비자잉여 0 · 자중손실 0</td><td>33-50 · 30-58 ①②</td></tr>
      <tr><td>2급</td><td>구매량별 단가(대량 할인)</td><td>이부가격(가입비 + 사용료)도 여기</td><td>32-56 이부가격</td></tr>
      <tr><td>3급</td><td>집단별 가격(나이·시간·지역)</td><td>MR<sub>A</sub> = MR<sub>B</sub> = MC · <b>비탄력 시장 고가</b> · 전매 불가</td><td>조조할인 · 30-58 ⑤ · 34-57 ④</td></tr>
    </tbody>
  </table></div>
  <p class="foot">가격차별이 아닌 것: 야간 근무 수당(임금 격차, 29회 47번). 러너지수 = (P − MC)/P = 1/|탄력성|.</p>

  <div class="grid2">
    <div class="mini"><h3>독점적 경쟁(음식점·미용실)</h3><p>차별화 상품 · 진입 자유 · 비가격경쟁. 단기는 독점처럼, 장기는 <b>P = AC 접점 → 이윤 0</b>, P &gt; MC(초과설비). 37회 48번: MR = MC와 P = AC를 동시에 풀기.</p></div>
    <div class="mini"><h3>자연독점 규제</h3><p>MC 가격 = 효율적이나 <b>손실(= 고정비용)</b>(35-56: −750) · AC 가격 = 손실 없음 · 이부/이중가격 = 손실 보전(32-56 ㄹ: 'AC 가격 손실 보전' X).</p></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>탄력성 |ε|</th><th>MR</th><th>가격 인하 시 총수입</th></tr></thead>
    <tbody>
      <tr><td>&gt; 1 (탄력)</td><td>+</td><td>증가</td></tr>
      <tr><td>= 1</td><td>0 (총수입 최대)</td><td>불변</td></tr>
      <tr><td>&lt; 1 (비탄력)</td><td>−</td><td>감소 (37-49 ③)</td></tr>
    </tbody>
  </table></div>
  <p class="foot">독점은 MR &gt; 0인 탄력적 구간에서만 생산한다. 도로공사 비유: 유일한 레미콘 공급업체가 있으면 물량을 줄이고 값을 올리는 것.</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>MR을 수요곡선 기울기 그대로 쓴다. 2배(30회 46번: ΔMC = 4 × 20 = 80).</span>
    <span>MR &gt; MC면 '가격 인상' → X. 생산 늘리고 가격 인하(28회 54번).</span>
    <span>3급에서 탄력적 시장을 비싸게 → X(34회 57번).</span>
    <span>조조할인 = 2급 → X. 3급(30회 58번).</span>
    <span>독점적 경쟁 P = MC → X. P &gt; MC(33회 48번).</span>
    <span>독점 이전 소비자잉여 = 자중손실과 혼동. 이전 = 직사각형 30 × 50 = 1,500(31회 51번).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>다공장 독점의 세부 계산, 독점의 장기 공장규모, 수요독점(→ 요소시장 단원)은 이 단원에선 넘긴다. 4단계 계산과 가격차별 표만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#pc">완전경쟁</a>','<a href="#pc">완전경쟁</a><a href="#mono">독점·가격차별</a>',1)
h=h.replace('["완전경쟁시장","#pc","24~25강",14,"hi","앱에서 표시"]','["완전경쟁시장","#pc","24~25강",14,"hi","앱에서 표시"],["독점·가격차별·독점적 경쟁","#mono","26~27강",21,"hi","앱에서 표시"]',1)
a='      <tr data-sec="pc"><th>완전경쟁 장기</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="mono"><th>독점</th><td>MR = MC → 수요곡선에서 P · MR 기울기 = 수요의 2배 · P &gt; MC(자중손실)</td></tr>
      <tr data-sec="mono"><th>가격차별</th><td>1급 CS 0·DWL 0 · 2급 수량별 · 3급 MR 일치, 비탄력 고가</td></tr>
'''+h[j:]
js='''
/* 독점 vs 완전경쟁 */
function drawMono(){const c=+$("#mo1").value;$("#mo1Out").textContent=c;const svg=$("#svgMono"),p=plot(svg,100,100,"Q","P");
 const qm=(100-c)/2,pm=100-qm,qc=100-c;
 el(p.g,"polygon",{points:`${p.X(qm)},${p.Y(pm)} ${p.X(qc)},${p.Y(c)} ${p.X(qm)},${p.Y(c)}`,fill:"var(--dwl)"});
 el(p.g,"rect",{x:p.X(0),y:p.Y(pm),width:p.X(qm)-p.X(0),height:p.Y(c)-p.Y(pm),fill:"var(--area1)"});
 line(p,p.g,"d",0,100,100,0);line(p,p.g,"s",0,100,50,0);line(p,p.g,"g",0,c,100,c);
 line(p,p.g,"guide",qm,0,qm,pm);line(p,p.g,"guide",0,pm,qm,pm);
 el(p.t,"text",{x:p.X(88),y:p.Y(14)},"D");el(p.t,"text",{x:p.X(42),y:p.Y(18)},"MR");el(p.t,"text",{x:p.X(92),y:p.Y(c)-5},"MC");
 $("#moOut").innerHTML=`독점: Q = ${f(qm,1)}, P = ${f(pm,1)}, 이윤(파란 사각형) ${f((pm-c)*qm,0)} · 완전경쟁: Q = ${f(qc,1)}, P = ${c} · 자중손실(빨간 삼각형) <b>${f((pm-c)*(qc-qm)/2,0)}</b>`}
$("#mo1").addEventListener("input",drawMono);drawMono();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=27
for x in u['units']:
    if x['u']=='U13': x['note']='mono'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
