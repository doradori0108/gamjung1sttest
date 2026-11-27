import json
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="pc"' not in h
sec='''<!-- 완전경쟁 -->
<section id="pc" class="sec" data-lec="24" aria-labelledby="h-pc">
  <div class="shead"><h2 id="h-pc">완전경쟁시장</h2><span class="badge hi">비중 상 · 14문항</span><span class="lec">24~25강</span></div>
  <div class="key">완전경쟁 기업은 가격을 받아들이고(P = MR) P = MC가 되는 양을 만든다. 단기엔 손실이어도 P ≥ AVC면 생산, 장기엔 진입·퇴출로 P = LAC 최저점이 되어 초과이윤 0.<small>MR(한계수입) = 1개 더 팔 때 느는 수입. 완전경쟁에선 몇 개를 팔든 가격이 같아 MR = P.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1~2문항. ① 가격 위치별 이윤·조업 판정(30·31·33회) ② 장기균형 기업 수 계산(28회 44번 · 29회 49번 · 31회 56번) ③ 공급곡선·공급량(28회 59번 · 31회 49번 · 35회 46번) ④ 장기균형 특징 O·X(29회 50번 · 34회 52번)</p>

  <div class="lab">
    <h3>가격을 움직여 보세요 · 비용곡선은 위 비용이론 실습과 같음(FC 40)</h3>
    <div class="slider"><label for="pc1">시장가격 P</label><input type="range" id="pc1" min="4" max="30" step="0.5" value="14"><output id="pc1Out">14</output></div>
    <svg id="svgPc" viewBox="0 0 340 250" role="img" aria-label="MC, AC, AVC 곡선과 가격선, 이윤 또는 손실 사각형"></svg>
    <div class="readout" id="pcOut" aria-live="polite"></div>
  </div>

  <div class="tw c1"><table>
    <thead><tr><th>가격 위치</th><th>이윤</th><th>생산?</th><th>기출</th></tr></thead>
    <tbody>
      <tr><td>P &gt; AC 최저점</td><td>+</td><td>생산</td><td>33-46 P<sub>1</sub></td></tr>
      <tr><td>P = AC 최저점(<b>손익분기점</b>)</td><td>0</td><td>생산</td><td>33-46 P<sub>2</sub></td></tr>
      <tr><td>AVC 최저점 &lt; P &lt; AC 최저점</td><td>− (고정비 일부 회수)</td><td><b>생산</b></td><td>30-53 · 31-61 · 33-46 P<sub>3</sub>·P<sub>4</sub></td></tr>
      <tr><td>P = AVC 최저점(<b>조업중단점</b>)</td><td>− 고정비 전액</td><td>무차별</td><td></td></tr>
      <tr><td>P &lt; AVC 최저점</td><td>− 고정비 전액</td><td>중단</td><td>33-46 P<sub>5</sub></td></tr>
    </tbody>
  </table></div>

  <h3>장기균형 기업 수: 3단계</h3>
  <ol class="steps">
    <li>LAC 최저점 찾기(미분 = 0, 또는 LMC = LAC): C = 0.5q² + 8 → LAC = 0.5q + 8/q → q* = 4, P* = 4</li>
    <li>시장수요에 P* 대입: Q = 1,000 − 40 = 960</li>
    <li>기업 수 = Q ÷ q* = <b>240</b> (28회 44번). 29회 49번 70개, 31회 56번 100개도 같은 틀</li>
  </ol>
  <div class="grid2">
    <div class="mini"><h3>공급곡선 = P = MC</h3><p>STC = a + q²/100 → MC = q/50 → q = 50p(28회 59번). 시장공급 = 수평합(35회 46번 100P + 300P).</p></div>
    <div class="mini"><h3>공급곡선 → 가변비용</h3><p>Q = P/2 → MC = 2Q → VC = MC 아래 넓이 = Q² → Q = 5면 25(35회 59번).</p></div>
  </div>
  <p class="foot">장기균형 등식: P = MR = SMC = LMC = SAC = LAC(최저점). 초과이윤 0, 정상이윤은 있음. 도로공사 입찰로 비유하면, 이익이 나는 공종엔 업체가 몰려 단가가 원가 수준까지 내려가는 것.</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>"초과이윤 0 = 정상이윤 0" → X(28회 43번 · 34회 52번).</span>
    <span>손실이면 바로 조업중단 → X. 기준은 AVC(30회 53번 · 31회 61번).</span>
    <span>"P<sub>4</sub>에서 고정비용 모두 충당" → X. 일부만(33회 46번).</span>
    <span>"독점의 공급곡선은 AC에서 도출" → X. 독점은 공급곡선이 없다(28회 43번).</span>
    <span>이윤 계산에서 고정비용을 빼먹는다(35회 47번).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>비용불변·체증·체감 산업의 장기공급곡선 모양, 지대(이윤이 요소가격으로 흡수) 논의는 10년간 단독 출제 없음. 위 표와 3단계 계산만.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#cost">비용이론</a>','<a href="#cost">비용이론</a><a href="#pc">완전경쟁</a>',1)
h=h.replace('["비용이론·비용극소화","#cost","22~23강",14,"hi","앱에서 표시"]','["비용이론·비용극소화","#cost","22~23강",14,"hi","앱에서 표시"],["완전경쟁시장","#pc","24~25강",14,"hi","앱에서 표시"]',1)
a='      <tr data-sec="cost"><th>비용극소화</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="pc"><th>완전경쟁 단기</th><td>P = MC · P &lt; AC 손실 · P &lt; AVC 최저점이면 중단</td></tr>
      <tr data-sec="pc"><th>완전경쟁 장기</th><td>P = LAC 최저점 · 초과이윤 0(정상이윤 O) · 기업 수 = Q(P*) ÷ q*</td></tr>
'''+h[j:]
js='''
/* 완전경쟁: 가격에 따른 단기 판단 */
function drawPc(){const P=+$("#pc1").value;$("#pc1Out").textContent=P;const FC=40,svg=$("#svgPc"),p=plot(svg,10,60,"Q","가격·비용");
 const VC=q=>20*q-4*q*q+0.4*q*q*q,MC=q=>20-8*q+1.2*q*q,AVC=q=>VC(q)/q,AC=q=>(FC+VC(q))/q;
 const path=(fn,cls)=>{let d="";for(let q=0.3;q<=10.001;q+=0.1){d+=(d?"L":"M")+p.X(q).toFixed(1)+" "+p.Y(Math.min(fn(q),80)).toFixed(1)}el(p.g,"path",{d,class:cls})};
 const minAVC=AVC(5);let q=(8+Math.sqrt(64-4*1.2*(20-P)))/(2*1.2);const shut=P<minAVC;if(shut)q=0;
 if(!shut){const a=AC(q);el(p.g,"rect",{x:p.X(0),y:p.Y(Math.max(P,a)),width:p.X(q)-p.X(0),height:Math.abs(p.Y(P)-p.Y(a)),fill:P>=a?"var(--area1)":"var(--dwl)",opacity:.6})}
 path(MC,"d");path(AC,"s");path(AVC,"g");line(p,p.g,"guide",0,P,10,P);
 [["MC",MC,9.3],["AC",AC,9.6],["AVC",AVC,9.6]].forEach(([n,fn,x])=>el(p.t,"text",{x:p.X(x)-4,y:p.Y(Math.min(fn(x),58))-6},n));
 if(!shut)el(p.g,"circle",{cx:p.X(q),cy:p.Y(P),r:4,fill:"var(--demand)"});
 const pi=shut?-FC:P*q-FC-VC(q);
 $("#pcOut").innerHTML=shut?`P ${P} &lt; AVC 최저점 ${f(minAVC,1)} → <b>조업중단</b>. 손실 = 고정비용 ${FC}`:`P = MC → q = ${f(q,1)} · AC ${f(AC(q),1)} · AVC ${f(AVC(q),1)} → 이윤 <b>${f(pi,1)}</b>${pi<0?(pi>-FC?" (손실이지만 멈추면 −40이라 생산이 낫다)":""):""}`}
$("#pc1").addEventListener("input",drawPc);drawPc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=25
for x in u['units']:
    if x['u']=='U12': x['note']='pc'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
