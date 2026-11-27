import json,re
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="money"' not in h and not re.search(r'id="mm\d|mmOut|function mmCalc|id="ml\d|mlOut|function mlCalc',h)
sec='''<!-- 거시: 승수·대부자금·화폐 -->
<section id="money" class="sec" data-lec="44" aria-labelledby="h-money">
  <div class="shead"><h2 id="h-money">승수 · 대부자금 · 화폐</h2><span class="badge hi">비중 상 · 28문항</span><span class="lec">44강</span></div>
  <div class="key">거시 최다 출제 단원. 계산은 두 공식으로 끝난다: <b>지출승수</b> = 1 ÷ (1 − 한계소비성향 + 한계수입성향), <b>통화승수</b> = (현금비율 + 1) ÷ (현금비율 + 지급준비율).<small>승수 = 처음 1원 쓴 돈이 돌고 돌아 소득을 몇 원 늘리는지. 도로공사 비유: 공사비 1억이 인부 임금 → 식당 매출 → 식당 직원 소비로 이어지는 연쇄.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 28문항, 매년 2~4문항. ① 정부지출·조세·균형재정승수(29·31·34·35·36·37회) ② 개방경제 승수와 경상수지(31·32·33·37회) ③ 통화승수·본원통화(30·31·34·35·37회) ④ 화폐수요·유통속도(28·30·32·36·37회) ⑤ 대부자금(32·35회)</p>

  <div class="lab">
    <h3>지출승수 계산기 · 37회 78번 기본값</h3>
    <div class="slider"><label for="mm1">한계소비성향 c</label><input type="range" id="mm1" min="0.5" max="0.95" step="0.05" value="0.8"><output id="mm1Out">0.8</output></div>
    <div class="slider"><label for="mm2">한계수입성향 m(처분가능소득 기준)</label><input type="range" id="mm2" min="0" max="0.4" step="0.05" value="0.1"><output id="mm2Out">0.1</output></div>
    <div class="slider"><label for="mm3">정부지출 증가</label><input type="range" id="mm3" min="0" max="100" step="10" value="50"><output id="mm3Out">50</output></div>
    <div class="slider"><label for="mm4">조세 증가</label><input type="range" id="mm4" min="0" max="100" step="10" value="50"><output id="mm4Out">50</output></div>
    <div class="readout" id="mmOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>승수</th><th>폐쇄경제</th><th>개방경제(수입 = m(Y − T))</th></tr></thead>
    <tbody>
      <tr><td>정부지출·투자·수출</td><td>1 ÷ (1 − c)</td><td>1 ÷ (1 − c + m)</td></tr>
      <tr><td>조세</td><td>−c ÷ (1 − c)</td><td>−(c − m) ÷ (1 − c + m)</td></tr>
      <tr><td>균형재정(ΔG = ΔT)</td><td><b>1</b></td><td>1 (수입이 Y − T의 함수일 때, 경상수지 불변)</td></tr>
      <tr><td>비례세 T = tY</td><td colspan="2">1 ÷ [1 − c(1 − t)] → 승수 작아짐(자동안정장치, 35-69: 5/3)</td></tr>
    </tbody>
  </table></div>

  <div class="lab">
    <h3>통화승수 계산기 · 37회 66번 기본값</h3>
    <div class="slider"><label for="ml1">현금/예금 비율</label><input type="range" id="ml1" min="0" max="2" step="0.1" value="0.6"><output id="ml1Out">0.6</output></div>
    <div class="slider"><label for="ml2">지급준비율(법정 + 초과, %)</label><input type="range" id="ml2" min="5" max="100" step="5" value="20"><output id="ml2Out">20</output></div>
    <div class="slider"><label for="ml3">본원통화 증가(조 원)</label><input type="range" id="ml3" min="1" max="10" step="1" value="3"><output id="ml3Out">3</output></div>
    <div class="readout" id="mlOut" aria-live="polite"></div>
  </div>
  <div class="grid2">
    <div class="mini"><h3>본원통화를 바꾸는 것</h3><p>공개시장 매입(↑) · 재할인 대출(↑, 재할인율 인상 ↓) · 정부의 중앙은행 차입(↑) · 외환 매입(↑). 본원통화 = 현금 + 지급준비금(시재금 포함, 34-66 ⑤).</p></div>
    <div class="mini"><h3>승수를 바꾸는 것</h3><p>현금비율 ↑ → 승수 ↓, 지급준비율(초과 포함) ↑ → 승수 ↓. 국채 매입은 승수 불변(30-77 ㄷ). 100% 지급준비면 승수 1.</p></div>
  </div>

  <h3>화폐수요 · 유통속도</h3>
  <p class="foot">화폐수량설 MV = PY → V = Y ÷ (M/P). 화폐수요함수가 주어지면 V를 바로 계산(28-70: M/P = Y/5i → V = 5i, 36-62: V = i/0.2 = 0.2). 화폐수요 = f(소득 +, 물가 +, 이자율 −). 케인즈 3동기: 거래적·예비적 = 소득, 투기적 = 이자율. 유동성 함정 = 이자율 탄력성 <b>무한대</b>(37-65 ①).</p>
  <h3>대부자금시장(고전학파)</h3>
  <p class="foot">공급 = 총저축(민간 + 정부 T − G), 수요 = 투자 I(r). 정부지출 ↑ → 정부저축 ↓ → 이자율 ↑ → 투자 ↓(구축효과, 35-67). 정부저축은 이자율과 무관(32-64 ④).</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>개방경제 균형재정승수를 0이나 그대로 1로 외워 적용(29-68: 100, 수입 함수 형태 확인).</span>
    <span>수출 증가분 = 경상수지 개선분으로 착각(33-66: 100 − 수입 40 = 60).</span>
    <span>법정지급준비율만 쓰고 초과지급준비율을 빼먹음(37-66).</span>
    <span>중앙은행이 '사면' 통화량 감소로 착각(28-66 ③, 37-67 ㄱ).</span>
    <span>환율경로: 금리 ↑ → 통화가치 '상승' → 순수출 감소(35-66 ⑤).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>M1·M2·Lf 세부 구성, 화폐 기능의 역사, 보몰-토빈 재고모형 계산은 출제가 드물다. 두 승수 공식과 본원통화 표만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#cons">소비·투자</a>','<a href="#cons">소비·투자</a><a href="#money">승수·화폐</a>',1)
h=h.replace('["국민소득·물가지수","#gdp","39강",23,"hi","앱에서 표시"],','["승수·대부자금·화폐","#money","44강",28,"hi","앱에서 표시"],["국민소득·물가지수","#gdp","39강",23,"hi","앱에서 표시"],',1)
a='      <tr data-sec="cons"><th>투자이론</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="money"><th>지출승수</th><td>1/(1 − c + m) · 조세 −(c − m)/(1 − c + m) · 균형재정 1 · 비례세 1/[1 − c(1 − t)]</td></tr>
      <tr data-sec="money"><th>통화승수</th><td>(k + 1)/(k + r), k = 현금/예금 · 국채·외환 매입 = 본원통화 ↑ · V = Y ÷ (M/P) · 유동성함정 = 탄력성 ∞</td></tr>
'''+h[j:]
js='''
/* 지출승수 · 통화승수 */
function mmCalc(){const c=+$("#mm1").value,m=+$("#mm2").value,g=+$("#mm3").value,t=+$("#mm4").value;["mm1","mm2","mm3","mm4"].forEach(k=>$("#"+k+"Out").textContent=$("#"+k).value);
 const k=1/(1-c+m),dy=k*(g-(c-m)*t),dm=m*(dy-t);
 $("#mmOut").innerHTML=`승수 ${f(k)} · ΔY = ${f(k)} × (${g} − ${f(c-m)} × ${t}) = <b>${f(dy)}</b> · 수입 변화 ${f(dm)} → 경상수지 ${f(-dm)}`}
["mm1","mm2","mm3","mm4"].forEach(k=>$("#"+k).addEventListener("input",mmCalc));mmCalc();
function mlCalc(){const k=+$("#ml1").value,r=+$("#ml2").value/100,b=+$("#ml3").value;["ml1","ml2","ml3"].forEach(i=>$("#"+i+"Out").textContent=$("#"+i).value);
 const m=(k+1)/(k+r);
 $("#mlOut").innerHTML=`통화승수 (${k} + 1) ÷ (${k} + ${f(r)}) = <b>${f(m)}</b> → 통화량 증가 ${f(m*b)}조 원`}
["ml1","ml2","ml3"].forEach(i=>$("#"+i).addEventListener("input",mlCalc));mlCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=46
for x in u['units']:
    if x['u']=='U20': x['note']='money'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
