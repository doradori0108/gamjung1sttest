import json,re
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="rule"' not in h and not re.search(r'id="rl\d|rlOut|function rlCalc',h)
sec='''<!-- 거시: 준칙 vs 재량 · 정책시차 · 테일러 준칙 -->
<section id="rule" class="sec" data-lec="54" aria-labelledby="h-rule">
  <div class="shead"><h2 id="h-rule">준칙 vs 재량 · 정책시차 · 테일러 준칙</h2><span class="badge mid">비중 중 · 11문항</span><span class="lec">54강</span></div>
  <div class="key">결론 하나: <b>합리적 기대 아래서 재량 정책은 실업을 못 줄이고 인플레이션만 높인다</b>(시간 불일치 → 준칙이 낫다). 계산은 손실함수를 π로 미분하는 한 가지 유형.<small>준칙 = 미리 정해 약속한 규칙대로. 재량 = 그때그때 최선을 고름. 시간 불일치 = 약속해 놓고 나중에 어기고 싶어지는 문제.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 11문항. ① 손실함수 최소화 계산(29·32·35·37회) ② 정책시차 O·X(29·37회) ③ 테일러 준칙 대입(31·33·34·35회) ④ 한국은행 제도(32회)</p>
  <div class="lab">
    <h3>재량 vs 준칙 · u = u<sub>n</sub> − b(π − π<sup>e</sup>), L = u + (a/2)π², u<sub>n</sub> = 5 (37회 73번 기본값)</h3>
    <div class="slider"><label for="rl1">b(필립스 기울기)</label><input type="range" id="rl1" min="0.5" max="3" step="0.5" value="2"><output id="rl1Out">2</output></div>
    <div class="slider"><label for="rl2">a(인플레이션 싫어하는 정도)</label><input type="range" id="rl2" min="0.5" max="3" step="0.5" value="1"><output id="rl2Out">1</output></div>
    <div class="readout" id="rlOut" aria-live="polite"></div>
  </div>
  <div class="steps"><b>손실함수 풀이 3단계</b>
    <span>① 필립스곡선을 u에 대해 풀어 손실함수에 대입한다.</span>
    <span>② π<sup>e</sup>는 상수로 두고 L을 π로 미분해 0 → 재량 π.</span>
    <span>③ 합리적 기대면 π<sup>e</sup> = π → u = u<sub>n</sub>. 손실 = u<sub>n</sub> + 인플레이션 부분. 준칙(π = 0)이면 손실 = u<sub>n</sub>.</span>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>내부시차(결정까지)</th><th>외부시차(효과까지)</th></tr></thead>
    <tbody>
      <tr><td>통화정책</td><td>짧다(금통위 결정)</td><td>길다(금리 → 투자·소비 전달)</td></tr>
      <tr><td>재정정책</td><td>길다(예산 · 국회)</td><td>짧다(직접 지출)</td></tr>
      <tr><td>자동안정화장치</td><td colspan="2">누진세·실업급여 → 결정이 필요 없어 내부시차를 줄인다</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>테일러 준칙</h3><p>금리 = π + 중립 실질금리 + a(π − 목표) + b(산출량 갭). 인플레이션 ↑·경기 과열 → 금리 ↑. 목표치를 낮추면 금리 ↑(33-65 ②). 숫자 대입 문제는 식에 그대로 넣는다(34-75: r = 9%).</p></div>
    <div class="mini"><h3>디스인플레이션</h3><p>긴축 → 실질이자율 ↑ → 단기 생산 ↓(경기침체). 기대가 빨리 조정될수록 빨리 장기균형으로(35-64). 루카스 비판: 정책이 바뀌면 기대·행동도 바뀐다.</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>내부시차 ↔ 외부시차 정의 뒤집기(29-67 ㄱ · 37-74 ㄷ).</span>
    <span>시간 불일치면 재량이 낫다(29-67 ㄹ). 준칙.</span>
    <span>재량이면 실업률이 낮아진다(32-68). 합리적 기대면 u = u<sub>n</sub> 그대로.</span>
    <span>디스인플레이션 때 실질이자율 하락(35-64 ㄴ).</span>
    <span>물가안정목표제를 고용 목적으로(32-62 ⑤).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>바로-고든 모형의 평판·게임 확장, 통화정책 전달경로 세부(신용경로 등)는 넘긴다. 손실함수 3단계와 시차 표만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#infl">실업·필립스</a>','<a href="#infl">실업·필립스</a><a href="#rule">준칙·재량</a>',1)
h=h.replace('["실업·인플레이션·필립스곡선","#infl","53강",26,"hi","앱에서 표시"],','["실업·인플레이션·필립스곡선","#infl","53강",26,"hi","앱에서 표시"],["준칙·재량·테일러 준칙","#rule","54강",11,"mid","앱에서 표시"],',1)
a='      <tr data-sec="infl"><th>필립스곡선</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="rule"><th>준칙 · 재량</th><td>손실함수 π로 미분 → 재량 π · 합리적 기대면 u = u<sub>n</sub>, 재량은 인플레이션만 ↑ → 준칙 · 내부시차 통화 짧음 / 재정 김 · 테일러: π·갭 ↑ → 금리 ↑</td></tr>
'''+h[j:]
js='''
/* 준칙 vs 재량 */
function rlCalc(){const b=+$("#rl1").value,a=+$("#rl2").value;$("#rl1Out").textContent=b;$("#rl2Out").textContent=a;
 const p=b/a,L=5+a/2*p*p;
 $("#rlOut").innerHTML=`준칙(π = 0): u = 5, 손실 <b>5</b> · 재량: π = b ÷ a = <b>${f(p)}</b>, 민간이 예상해 u = 5 그대로, 손실 <b>${f(L)}</b> → 재량은 손실만 ${f(L-5)} 더 큼`}
["rl1","rl2"].forEach(k=>$("#"+k).addEventListener("input",rlCalc));rlCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=55
for x in u['units']:
    if x['u']=='U24': x['note']='rule'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
