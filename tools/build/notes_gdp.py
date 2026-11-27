import json,re
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="gdp"' not in h and not re.search(r'id="gd\d|gdOut|function gdCalc',h)
sec='''<!-- 거시: 국민소득 -->
<section id="gdp" class="sec" data-lec="39" aria-labelledby="h-gdp">
  <div class="shead"><h2 id="h-gdp">국민소득 · 물가지수(거시 시작)</h2><span class="badge hi">비중 상 · 23문항</span><span class="lec">39강</span></div>
  <div class="key">GDP = 일정 기간 <b>국내</b>에서 <b>새로</b> 생산된 <b>최종</b> 재화·서비스의 <b>시장가치</b>. 시험은 ① 포함·제외 판단 ② 항등식 NX = (S<sub>P</sub> − I) + (T − G) ③ 물가지수 3종 비교 세 가지로 끝난다.<small>거시경제 = 나라 전체의 생산·물가·고용을 보는 분야. 도로공사 비유: 올해 새로 깐 도로(생산)는 GDP, 기존 도로 부지 매매(자산 거래)는 GDP가 아니다.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 23문항, 매년 2~3문항. ① GDP 포함 O·X(29·30·34·35·36·37회) ② 항등식 계산(28·29·30·31·33·35회) ③ 물가지수 비교·계산(28·29·32·33·34·35회) ④ GDI·GNI·NI 사다리(30·36회)</p>

  <h3>포함 · 제외</h3>
  <div class="tw c1"><table>
    <thead><tr><th>GDP에 포함</th><th>GDP에서 제외</th></tr></thead>
    <tbody>
      <tr><td>신축 주택(투자) · 재고 증가(재고투자) · 중개수수료</td><td>기존 주택·중고품·주식 거래, 주가·집값 상승</td></tr>
      <tr><td>귀속임대료 · 농가 자가소비 · 정부 서비스(비시장이지만 포함)</td><td>가사노동 · 지하경제</td></tr>
      <tr><td>외국인의 국내 생산(GDP 기준 = 장소)</td><td>이전지출(연금·출산장려금·실업수당)</td></tr>
      <tr><td>간접세 · 감가상각(GDP는 '총'생산)</td><td>중간재(최종재에 이미 포함) · 수입품(C에 더해지고 M으로 빠짐)</td></tr>
    </tbody>
  </table></div>

  <div class="lab">
    <h3>항등식 · 33회 61번 기본값</h3>
    <div class="slider"><label for="gd1">민간저축 S<sub>P</sub></label><input type="range" id="gd1" min="0" max="300" step="10" value="150"><output id="gd1Out">150</output></div>
    <div class="slider"><label for="gd2">투자 I</label><input type="range" id="gd2" min="0" max="300" step="10" value="50"><output id="gd2Out">50</output></div>
    <div class="slider"><label for="gd3">조세 T</label><input type="range" id="gd3" min="0" max="200" step="10" value="50"><output id="gd3Out">50</output></div>
    <div class="slider"><label for="gd4">정부지출 G</label><input type="range" id="gd4" min="0" max="200" step="10" value="70"><output id="gd4Out">70</output></div>
    <div class="readout" id="gdOut" aria-live="polite"></div>
  </div>
  <ol class="steps">
    <li>Y = C + I + G + NX 와 Y = C + S<sub>P</sub> + T 를 빼면 → <b>NX = (S<sub>P</sub> − I) + (T − G)</b></li>
    <li>모르는 값은 정의로 역산: S<sub>P</sub> = Y − T − C(31-72에서 T = 50), G = 정부소비 + 정부투자(35-63)</li>
    <li>균형예산(G = T)이면 S<sub>P</sub> = I + NX(30-65: 200 + 50 = 250, Y 계산 불필요)</li>
    <li>유량 ≠ 저량: 적자가 '줄어도' 적자면 채무는 늘고, 흑자면 순대외채권은 늘어난다(29-71)</li>
  </ol>

  <h3>소득 지표 사다리</h3>
  <p class="foot">GDP → (+ 교역조건 변화 손익) <b>GDI</b> → (+ 국외 순수취 요소소득) <b>GNI</b> → (− 고정자본소모) NNI → (− 순간접세) <b>NI</b> = 임금 + 지대 + 이자 + 이윤. 처분가능소득 = GNI − 감가상각 − 사내유보 − 세금 + 이전지출(30-64: 1,000 → 1,050 → 1,070 → 1,050). GNP = GDP + 순수취 요소소득(37-61 ㄷ X).</p>

  <h3>물가지수 3종</h3>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>CPI</th><th>GDP 디플레이터</th><th>PPI</th></tr></thead>
    <tbody>
      <tr><td>방식</td><td>라스파이레스(기준연도 수량 고정)</td><td>파셰(비교연도 수량, 가중치 매년 변함)</td><td>라스파이레스</td></tr>
      <tr><td>대상</td><td>소비자 장바구니(<b>수입 소비재 O</b>)</td><td>국내 생산 최종재 전부(투자재 O, <b>수입품 X</b>)</td><td>기업 간 거래(<b>수입품 O</b>, 원자재 O)</td></tr>
      <tr><td>특징</td><td>대체효과·신상품·품질개선 무시 → 생계비 과대평가. 그래도 생계비 지표로는 디플레이터보다 적합(32-67 ④)</td><td>명목GDP ÷ 실질GDP × 100</td><td>CPI의 선행지표</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>계산 3종</h3><p>가중평균 상승률(28-74: 0.4×10 + 0.2×10 + 0.2×5 = 7%) · 파셰(34-64: 1,800 ÷ 1,000 → 80%) · 실질GDP = 기준연도 가격 × 당해 수량(35-61: 20%).</p></div>
    <div class="mini"><h3>증가율 근사</h3><p>실질 성장률 ≈ 명목 − 물가, 1인당 ≈ 실질 − 인구(30-76: 5 − 3 − 1 = 1%). 다른 해 금액 환산 = 금액 × 지수비(30-68: 1,000 × 120/40).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>'시장 거래 최종생산물만' → X(귀속임대료 등 예외, 34-62 ① · 36-73 ①).</span>
    <span>GNP = GDP − 순수취 → X. 더한다.</span>
    <span>수입 부품을 쓴 완제품 전액을 GDP로(35-62 ②). 부가가치 = 생산액 − 중간투입.</span>
    <span>소비 증가 → 경상수지 개선 → X(저축 감소, 28-73 ㄱ).</span>
    <span>PPI는 수입품 제외 → X(33-62 ㄷ).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>국민계정 세부 항목(통계상 불일치, 해외 부문 계정 표), 연쇄가중 GDP는 출제 거의 없음. 포함·제외 표와 항등식만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#fail">시장실패</a>','<a href="#fail">시장실패</a><a href="#gdp">국민소득</a>',1)
h=h.replace('["시장실패","#fail","35강",28,"hi","앱에서 표시"],','["시장실패","#fail","35강",28,"hi","앱에서 표시"],["국민소득·물가지수","#gdp","39강",23,"hi","앱에서 표시"],',1)
a='      <tr data-sec="fail"><th>공공재 · 정보</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="gdp"><th>GDP 포함</th><td>신축·재고증가·귀속임대료 O / 기존자산·주가·이전지출·가사노동 X · GNP = GDP + 순수취 · GDI = GDP + 교역조건 손익</td></tr>
      <tr data-sec="gdp"><th>항등식 · 물가</th><td>NX = (S<sub>P</sub> − I) + (T − G) · CPI 라스파이레스(수입 소비재 O) · 디플레이터 파셰(수입품 X) · PPI 수입품 O</td></tr>
'''+h[j:]
js='''
/* 국민소득 항등식 */
function gdCalc(){const s=+$("#gd1").value,i=+$("#gd2").value,t=+$("#gd3").value,g=+$("#gd4").value;["gd1","gd2","gd3","gd4"].forEach(k=>$("#"+k+"Out").textContent=$("#"+k).value);
 const nx=(s-i)+(t-g);
 $("#gdOut").innerHTML=`민간 (S<sub>P</sub> − I) = ${s-i} · 정부 (T − G) = ${t-g} → 경상수지 NX = <b>${nx}</b> ${nx>0?"흑자":nx<0?"적자":"균형"}`}
["gd1","gd2","gd3","gd4"].forEach(k=>$("#"+k).addEventListener("input",gdCalc));gdCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=40
for x in u['units']:
    if x['u']=='U18': x['note']='gdp'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
