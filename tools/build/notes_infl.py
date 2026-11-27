import json,re
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="infl"' not in h and not re.search(r'id="ph\d|phOut|svgPh|function phDraw',h)
sec='''<!-- 거시: 실업 · 인플레이션 · 필립스곡선 -->
<section id="infl" class="sec" data-lec="53" aria-labelledby="h-infl">
  <div class="shead"><h2 id="h-infl">실업 · 인플레이션 · 필립스곡선</h2><span class="badge hi">비중 상 · 26문항</span><span class="lec">53강</span></div>
  <div class="key">세 덩어리: <b>고용지표 계산</b>(분모가 무엇인지), <b>인플레이션</b>(피셔 · 수량방정식 · 비용), <b>필립스곡선</b>(단기 우하향, 장기 수직). 매년 2~4문항, 계산이 절반.<small>경제활동인구 = 취업자 + 실업자. 구직단념자는 비경제활동인구. 필립스곡선 = 인플레이션율과 실업률의 관계.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 26문항. ① 고용지표 계산(29·30·32·33회) ② 균제상태 실업률(30·33·35·37회) ③ 필립스곡선 O·X(28·32·34·36회)와 식 해석(33·37회) ④ 피셔·수량방정식 계산(28·29·30회) ⑤ 인플레이션 비용·용어(28·32·34·36회) ⑥ 효율임금(28·31회)</p>
  <div class="lab">
    <h3>단기 필립스곡선 π = π<sup>e</sup> − b(u − u<sub>n</sub>), u<sub>n</sub> = 5%</h3>
    <svg id="svgPh" viewBox="0 0 340 250" role="img" aria-label="단기 필립스곡선과 장기 필립스곡선"></svg>
    <div class="slider"><label for="ph1">기대 인플레이션 π<sup>e</sup>(%)</label><input type="range" id="ph1" min="0" max="8" step="0.5" value="2"><output id="ph1Out">2</output></div>
    <div class="slider"><label for="ph2">기울기 b(37-71은 2, 33-64는 0.5)</label><input type="range" id="ph2" min="0.5" max="3" step="0.5" value="2"><output id="ph2Out">2</output></div>
    <div class="slider"><label for="ph3">실업률 u(%)</label><input type="range" id="ph3" min="2" max="9" step="0.5" value="4"><output id="ph3Out">4</output></div>
    <div class="readout" id="phOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>지표</th><th>분자</th><th>분모</th></tr></thead>
    <tbody>
      <tr><td>경제활동참가율</td><td>경제활동인구</td><td>생산가능인구(15세 이상)</td></tr>
      <tr><td>실업률</td><td>실업자</td><td><b>경제활동인구</b></td></tr>
      <tr><td>고용률</td><td>취업자</td><td><b>생산가능인구</b></td></tr>
      <tr><td>균제상태 실업률</td><td>실직률 s</td><td>s + 구직률 f</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>피셔 · 수량방정식</h3><p>명목이자율 = 실질이자율 + 인플레이션율. MV = PY → 통화증가율 + V증가율 = 물가상승률 + 실질성장률. 28-80: π 2% + g 2% = 통화증가율 4%. 세금은 명목이자에 매기고 물가를 뺀다(30-69).</p></div>
    <div class="mini"><h3>인플레이션 비용</h3><p>예상된: 메뉴비용 · 구두창비용(현금 관리). 예상 못 한: 채권자 → 채무자, 고정소득자 손해, 누진세 수입 ↑. 주조차익 = 통화증가율 × 실질화폐, 인플레이션 조세 = π × 실질화폐(장기 균형에서 같음).</p></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>필립스곡선</th><th>단기</th><th>장기</th></tr></thead>
    <tbody>
      <tr><td>원조 필립스(1958)</td><td colspan="2">임금상승률-실업률의 우하향 '경험적' 관계(기대 개념 없음)</td></tr>
      <tr><td>적응적 기대(프리드먼·펠프스)</td><td>우하향(AS 우상향과 거울)</td><td>자연실업률에서 수직</td></tr>
      <tr><td>합리적 기대(새고전학파)</td><td>예상된 정책이면 수직 → 실업 증가 없이 물가 안정</td><td>수직</td></tr>
      <tr><td>이동</td><td colspan="2">기대 인플레이션 ↑, 음의 공급충격 → 위(오른쪽)로. AS 가파를수록 필립스곡선도 가파름</td></tr>
    </tbody>
  </table></div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>자연실업률 = 구조적 실업'만'(28-61 ③). 마찰적 포함.</span>
    <span>고용률 분모를 경제활동인구로(30-71 · 33-63).</span>
    <span>AI·로봇 실업을 경기적으로(29-64 ④). 구조적.</span>
    <span>효율임금 인하 시 유능한 노동자가 남는다(31-62 ⑤). 반대.</span>
    <span>기대 인플레이션 ↑ → 필립스곡선 왼쪽(36-72 ⑤). 오른쪽.</span>
    <span>π &lt; π<sup>e</sup>면 고용이 완전고용보다 높다(37-71 ④). 낮다.</span>
    <span>디플레이션 ↔ 스태그플레이션 ↔ 디스인플레이션 혼동(34-73).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>테일러 준칙 세부, 실업 이력현상(hysteresis), 초인플레이션 사례사는 넘긴다. 고용지표 표 · 균제상태 공식 · 필립스곡선 표만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#adas">AD-AS</a>','<a href="#adas">AD-AS</a><a href="#infl">실업·필립스</a>',1)
h=h.replace('["AD-AS·경기변동","#adas","51강",26,"hi","앱에서 표시"],','["AD-AS·경기변동","#adas","51강",26,"hi","앱에서 표시"],["실업·인플레이션·필립스곡선","#infl","53강",26,"hi","앱에서 표시"],',1)
a='      <tr data-sec="adas"><th>학파</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="infl"><th>고용지표</th><td>실업률 = 실업자 ÷ 경활 · 고용률 = 취업자 ÷ 생산가능 · 균제 실업률 = s ÷ (s + f) · 자연실업률 = 마찰 + 구조</td></tr>
      <tr data-sec="infl"><th>필립스곡선</th><td>π − π<sup>e</sup> = −b(u − u<sub>n</sub>) · 단기 우하향, 장기 수직 · π<sup>e</sup> ↑ → 위로 · 피셔 i = r + π · 통화증가율 = π + g</td></tr>
'''+h[j:]
js='''
/* 필립스곡선 */
function phDraw(){const E=+$("#ph1").value,b=+$("#ph2").value,u=+$("#ph3").value;["ph1","ph2","ph3"].forEach(k=>$("#"+k+"Out").textContent=$("#"+k).value);
 const p=plot($("#svgPh"),10,16,"u(%)","π(%)"),pi=x=>E-b*(x-5);
 const xa=Math.max(0,5-(16-E)/b),xb=Math.min(10,5+E/b);
 line(p,p.g,"d",xa,pi(xa),xb,pi(xb));line(p,p.g,"s",5,0,5,16);
 const P=pi(u);if(P>=0&&P<=16){line(p,p.g,"guide",u,0,u,P);line(p,p.g,"guide",0,P,u,P)}
 el(p.t,"text",{x:p.X(5)+4,y:p.Y(15.2)},"장기(수직)");el(p.t,"text",{x:p.X(Math.min(9.2,xb))-30,y:p.Y(Math.max(0.6,pi(Math.min(9.2,xb))))-6},"단기");
 $("#phOut").innerHTML=`u = ${f(u)}% → π = <b>${f(P)}%</b> · ${u<5?"자연실업률보다 낮은 실업 → π &gt; π<sup>e</sup>(고용 &gt; 완전고용)":u>5?"자연실업률보다 높은 실업 → π &lt; π<sup>e</sup>(고용 &lt; 완전고용)":"자연실업률 → π = π<sup>e</sup>"} · 실업률 1%p ↓ = 인플레이션 ${f(b)}%p ↑`}
["ph1","ph2","ph3"].forEach(k=>$("#"+k).addEventListener("input",phDraw));phDraw();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=53
for x in u['units']:
    if x['u']=='U23': x['note']='infl'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
