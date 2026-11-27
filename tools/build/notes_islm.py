import json,re
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="islm"' not in h and not re.search(r'id="il\d|ilOut|svgIl|function ilDraw',h)
sec='''<!-- 거시: IS-LM -->
<section id="islm" class="sec" data-lec="47" aria-labelledby="h-islm">
  <div class="shead"><h2 id="h-islm">IS-LM · 재정정책 · 통화정책</h2><span class="badge hi">비중 상 · 28문항</span><span class="lec">47강</span></div>
  <div class="key">IS = 물건 시장이 맞는 (소득, 이자율), LM = 돈 시장이 맞는 (소득, 이자율). 재정정책은 IS를, 통화정책은 LM을 옮기고, 두 선이 <b>가파르냐 완만하냐</b>가 정책 효과를 정한다.<small>구축효과 = 정부가 돈을 써서 이자율이 오르면 민간투자가 줄어드는 것. 도로공사 비유: 정부 발주가 몰려 자재·자금 값이 오르면 민간 공사가 밀려나는 것.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 28문항, 매년 2~5문항. ① 연립·목표 이자율용 통화량 계산(28·30·33·35·36회) ② 곡선 모양별 정책 효과(31·33·34·35·37회) ③ 리카도 등가(28·30·31·36회) ④ 구축효과·정책 조합(29·30·32회)</p>
  <div class="lab">
    <h3>IS-LM · 36회 63번 기본값 (IS: r = A − Y, LM: M = Y − r)</h3>
    <svg id="svgIl" viewBox="0 0 340 250" role="img" aria-label="IS곡선과 LM곡선, 균형점"></svg>
    <div class="slider"><label for="il1">재정 A(정부지출 ↑ → IS 오른쪽)</label><input type="range" id="il1" min="4" max="9" step="0.5" value="6"><output id="il1Out">6</output></div>
    <div class="slider"><label for="il2">명목화폐공급 M(P = 1)</label><input type="range" id="il2" min="1" max="7" step="0.5" value="4"><output id="il2Out">4</output></div>
    <div class="readout" id="ilOut" aria-live="polite"></div>
  </div>
  <ol class="steps">
    <li>연립: IS와 LM을 같이 풀면 (Y, r). 30-72: r = 2, Y = 300</li>
    <li>목표 이자율 문제: 목표 r을 <b>IS</b>에 넣어 Y → 그 (Y, r)을 LM에 넣어 필요한 M(28-71 · 35-76 · 36-63)</li>
    <li>균형재정승수: LM에서 r을 IS에 대입해 Y식으로 → ΔG = ΔT일 때 ΔY(32-61: 0.5, 구축 때문에 1보다 작음)</li>
  </ol>
  <div class="tw c1"><table>
    <thead><tr><th>모양</th><th>원인</th><th>재정정책</th><th>통화정책</th></tr></thead>
    <tbody>
      <tr><td>LM 수평(유동성함정)</td><td>화폐수요 이자 탄력성 ∞</td><td><b>최대</b>(구축 0)</td><td>무력</td></tr>
      <tr><td>LM 수직(고전학파)</td><td>화폐수요 이자 탄력성 0</td><td>무력(완전 구축)</td><td><b>최대</b></td></tr>
      <tr><td>IS 수직</td><td>투자의 이자 탄력성 0</td><td><b>최대</b></td><td>무력</td></tr>
      <tr><td>IS 수평</td><td>투자의 이자 탄력성 ∞</td><td>무력</td><td><b>최대</b>(34-68)</td></tr>
    </tbody>
  </table></div>
  <p class="foot">IS 기울기 절댓값 = (1 − MPC) ÷ 투자의 이자 민감도 → MPC ↑·투자 민감 ↑이면 완만(34-69). 완만한 IS = 통화정책 강함, 완만한 LM = 재정정책 강함(33-69). 물가 ↓ = 실질통화량 ↑ → LM 오른쪽(명목 M은 그대로, 31-79).</p>
  <div class="grid2">
    <div class="mini"><h3>리카도 등가</h3><p>국채로 감세해도 미래 증세를 예상해 저축 → 소비 불변. 성립: 합리적·미래지향, 차입제약 없음, 정액세, 정부지출 경로 불변. 불성립: 유동성 제약·근시안·왜곡적 조세·인구 증가. 미래 지출을 줄이며 감세하면 소비 증가(31-80 ⑤).</p></div>
    <div class="mini"><h3>재정정책 효과 키우는 것</h3><p>MPC ↑ · 한계수입성향 ↓ · 정액세(비례세 X) · 투자의 이자 탄력성 ↓ · 화폐수요의 이자 탄력성 ↑ · 중앙은행의 이자율 유지(통화량 ↑, LM 오른쪽, 32-76).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>유동성함정 = 재정정책 무력 → X(통화정책이 무력, 31-67 ㄷ · 37-68 ②).</span>
    <span>화폐수요 탄력성 0 = 유동성함정 → X(∞, 35-75 ①).</span>
    <span>목표 이자율 문제에서 LM에 먼저 대입(IS에 먼저).</span>
    <span>IS 위쪽 = 초과수요 → X(초과공급, 35-75 ⑤).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>IS-LM의 수식 일반해(편미분 승수), 먼델-토빈 효과·피구효과 세부는 출제가 드물다. 계산 3유형과 위 표만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#money">승수·화폐</a>','<a href="#money">승수·화폐</a><a href="#islm">IS-LM</a>',1)
h=h.replace('["승수·대부자금·화폐","#money","44강",28,"hi","앱에서 표시"],','["승수·대부자금·화폐","#money","44강",28,"hi","앱에서 표시"],["IS-LM·재정·통화정책","#islm","47강",28,"hi","앱에서 표시"],',1)
a='      <tr data-sec="money"><th>통화승수</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="islm"><th>IS-LM 모양</th><td>LM 수평(함정) = 재정 최대·통화 무력 · LM 수직 = 반대 · IS 완만 → 통화 강함 · LM 완만 → 재정 강함</td></tr>
      <tr data-sec="islm"><th>리카도 등가</th><td>국채 감세 → 소비 불변 · 조건: 합리적·차입제약 없음·정액세·지출 경로 불변</td></tr>
'''+h[j:]
js='''
/* IS-LM */
function ilDraw(){const A=+$("#il1").value,M=+$("#il2").value;$("#il1Out").textContent=A;$("#il2Out").textContent=M;
 const p=plot($("#svgIl"),10,8,"Y","r");const Y=(A+M)/2,r=(A-M)/2;
 line(p,p.g,"d",Math.max(0,A-8),Math.min(8,A),Math.min(10,A),Math.max(0,A-10));
 line(p,p.g,"s",M,0,Math.min(10,M+8),Math.min(8,10-M));
 line(p,p.g,"guide",Y,0,Y,Math.max(r,0));line(p,p.g,"guide",0,Math.max(r,0),Y,Math.max(r,0));
 el(p.t,"text",{x:p.X(Math.min(9.3,A-0.3)),y:p.Y(Math.max(0.3,0.3))-4},"IS");el(p.t,"text",{x:p.X(Math.min(9.3,M+6.5)),y:p.Y(Math.min(7.6,6.5))-4},"LM");
 $("#ilOut").innerHTML=r<0?"이자율이 음수가 되는 조합이에요. A를 키우거나 M을 줄여 보세요.":`균형 Y = <b>${f(Y)}</b>, r = <b>${f(r)}</b> · 재정 A +1 → Y +0.5, r +0.5(구축) · 통화 M +1 → Y +0.5, r −0.5`}
["il1","il2"].forEach(k=>$("#"+k).addEventListener("input",ilDraw));ilDraw();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=50
for x in u['units']:
    if x['u']=='U21': x['note']='islm'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
