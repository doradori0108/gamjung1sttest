import json
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="factor"' not in h
sec='''<!-- 요소시장 · 소득분배 -->
<section id="factor" class="sec" data-lec="30" aria-labelledby="h-factor">
  <div class="shead"><h2 id="h-factor">요소시장 · 소득분배</h2><span class="badge hi">비중 상 · 15문항</span><span class="lec">30~31강</span></div>
  <div class="key">요소시장은 생산물시장을 뒤집어 본 것이다. 기업이 노동을 '사는' 쪽이라 고용 조건은 VMP(= P × MP<sub>L</sub>) = 임금, 수요독점이면 VMP = MFC.<small>VMP = 노동자 1명이 더 만든 양의 판매가치. MFC = 1명 더 쓸 때 늘어나는 총인건비. 경제적 지대 = 최소 보수(전용수입)를 넘어 더 받는 몫.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1~2문항. ① 고용량 계산 VMP = w(32·33회) ② 수요독점(30·33·35·37회) ③ 지대·전용수입(28·30·34·36회) ④ 소득분배 지표(34회 54번 · 37회 51·52번) ⑤ 보상격차(30회 54번)</p>

  <div class="lab">
    <h3>지대 vs 전용수입 · 공급곡선 기울기를 바꿔 보세요 (균형 w = 7, L = 10)</h3>
    <div class="slider"><label for="fc1">공급곡선 세로절편</label><input type="range" id="fc1" min="0" max="7" step="0.5" value="2"><output id="fc1Out">2</output></div>
    <svg id="svgFc" viewBox="0 0 340 250" role="img" aria-label="노동 공급곡선 아래 전용수입, 위 경제적 지대 면적"></svg>
    <div class="readout" id="fcOut" aria-live="polite"></div>
  </div>
  <p class="foot">절편 2 = 28회 51번(지대 25, 전용수입 45). 절편 0에 가까울수록(가파를수록, 비탄력적) 지대↑. 절편 7 = 수평(완전탄력) → 지대 0.</p>

  <h3>요소시장 구조별 비교</h3>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>완전경쟁 노동시장</th><th>수요독점</th></tr></thead>
    <tbody>
      <tr><td>고용량</td><td>VMP = w</td><td>VMP(MRP) = <b>MFC</b></td></tr>
      <tr><td>임금</td><td>시장임금</td><td>그 고용량을 <b>공급곡선</b>에 넣어</td></tr>
      <tr><td>MFC 위치</td><td>MFC = w(수평)</td><td>공급곡선 <b>위</b>(기울기 2배)</td></tr>
      <tr><td>결과</td><td></td><td>고용↓ 임금↓ · 노동수요곡선 없음</td></tr>
    </tbody>
  </table></div>
  <ol class="steps">
    <li>30회 59번: 공급 w = L + 40 → MFC = 2L + 40</li>
    <li>MFC = VMP: 2L + 40 = 60 − 3L → L = 4</li>
    <li>임금 = 공급곡선에서 w = 44 (VMP 48에서 읽으면 오답)</li>
  </ol>

  <h3>소득분배 지표</h3>
  <div class="tw c1"><table>
    <thead><tr><th>지표</th><th>계산</th><th>완전 평등</th><th>완전 불평등</th></tr></thead>
    <tbody>
      <tr><td>로렌츠곡선</td><td>인구 누적 vs 소득 누적</td><td>대각선</td><td>ㄴ자</td></tr>
      <tr><td>지니계수</td><td>불평등 면적 ÷ 삼각형</td><td>0</td><td>1</td></tr>
      <tr><td>십분위분배율</td><td>하위 40% ÷ 상위 20%</td><td><b>2</b></td><td>0</td></tr>
      <tr><td>오분위분배율</td><td>상위 20% ÷ 하위 20%</td><td>1</td><td>∞</td></tr>
    </tbody>
  </table></div>
  <p class="foot">기능별 분배 = 임금·이자·이윤·지대(요소별) / 계층별 분배 = 소득 크기별. 로렌츠곡선이 교차하면 비교 불가. 도로사업 비유: 보상금 총액이 같아도 소수 대토지주에게 몰리면 지니계수가 크다.</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>수요독점 임금을 VMP나 MFC에서 읽는다. 공급곡선(30회 59번).</span>
    <span>MFC가 공급곡선 아래 → X(33회 59번 ㄴ · 37회 50번 ④).</span>
    <span>공급 수직 → 지대 없음 → X. 전부 지대(34회 53번 ㄷ).</span>
    <span>'최소한 받아야 할 금액' = 지대 → X. 전용수입(30회 50번 ㄷ).</span>
    <span>십분위분배율은 클수록 평등(다른 지표와 반대 방향, 37회 51·52번).</span>
    <span>성별 임금 격차 = 보상격차 → X(30회 54번).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>쌍방독점, 노동조합의 임금 결정 모형, 앳킨슨지수 계산은 출제가 드물다. 위 세 표와 VMP 계산만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#game">과점·게임이론</a>','<a href="#game">과점·게임이론</a><a href="#factor">요소시장·분배</a>',1)
h=h.replace('["과점·게임이론","#game","28~29강",17,"hi","앱에서 표시"]','["과점·게임이론","#game","28~29강",17,"hi","앱에서 표시"],["요소시장·소득분배","#factor","30~31강",15,"hi","앱에서 표시"]',1)
a='      <tr data-sec="game"><th>과점 생산량</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="factor"><th>요소시장</th><td>고용: VMP = w · 수요독점: VMP = MFC, 임금은 공급곡선 · MFC는 공급곡선 위</td></tr>
      <tr data-sec="factor"><th>지대 · 분배</th><td>공급 수직 = 전부 지대 · 수평 = 지대 0 / 십분위 2 = 평등, 지니·오분위는 클수록 불평등</td></tr>
'''+h[j:]
js='''
/* 요소시장: 지대와 전용수입 */
function drawFc(){const s=+$("#fc1").value;$("#fc1Out").textContent=s;const svg=$("#svgFc"),p=plot(svg,20,14,"L","w");
 const b=(7-s)/10;
 el(p.g,"polygon",{points:`${p.X(0)},${p.Y(0)} ${p.X(0)},${p.Y(s)} ${p.X(10)},${p.Y(7)} ${p.X(10)},${p.Y(0)}`,fill:"var(--area1)"});
 el(p.g,"polygon",{points:`${p.X(0)},${p.Y(s)} ${p.X(0)},${p.Y(7)} ${p.X(10)},${p.Y(7)}`,fill:"var(--area2)"});
 line(p,p.g,"d",0,12,20,2);line(p,p.g,"s",0,s,20,s+b*20);line(p,p.g,"guide",0,7,10,7);line(p,p.g,"guide",10,0,10,7);
 el(p.t,"text",{x:p.X(17),y:p.Y(3.6)},"D");el(p.t,"text",{x:p.X(17),y:p.Y(Math.min(13,s+b*17))-6},"S");
 const rent=(7-s)*10/2;
 $("#fcOut").innerHTML=`요소소득 70 = 전용수입(공급곡선 아래) <b>${f(70-rent,1)}</b> + 경제적 지대(위) <b>${f(rent,1)}</b>`}
$("#fc1").addEventListener("input",drawFc);drawFc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=31
for x in u['units']:
    if x['u']=='U15': x['note']='factor'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
