import json,re
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
def sl(i,lab,mn,mx,st,v): return f'    <div class="slider"><label for="{i}">{lab}</label><input type="range" id="{i}" min="{mn}" max="{mx}" step="{st}" value="{v}"><output id="{i}Out">{v}</output></div>\n'
sec='''<!-- 32. 결합원가 -->
<section id="jc" class="sec" aria-labelledby="h-jc">
  <div class="shead"><h2 id="h-jc">결합원가</h2><span class="badge mid">비중 중 · 7문항</span><span class="lec">32단원</span></div>
  <div class="key">한 공정에서 여러 제품이 같이 나올 때 공통원가(결합원가)를 나누는 법 3가지 + 추가가공 의사결정. 추가가공은 <b>증분수익 vs 추가가공원가</b>만 비교하고 결합원가는 무시(매몰원가).<small>분리점 = 제품이 각각 구분되는 시점. 순실현가치(NRV) = 최종 판매가 − 추가가공원가.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 7문항. ① 배분 계산(분리점 판매가치·NRV·균등이익률, 28·33·34·35·36회) ② 추가가공 의사결정(30·31회)</p>
  <div class="lab">
    <h3>추가가공 판단 · 31회 74번 A 기본값</h3>
''' + sl('jc1','생산량',0,1000,10,400) + sl('jc2','분리점 단위당 가격',0,600,10,120) + sl('jc3','가공 후 단위당 가격',0,800,10,450) + sl('jc4','추가가공원가',0,300000,5000,150000) + '''    <div class="readout" id="jcOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>배분법</th><th>기준</th><th>예</th></tr></thead>
    <tbody>
      <tr><td>분리점 판매가치법</td><td>분리점 판매가치 비율</td><td>36-74, 30-73</td></tr>
      <tr><td>순실현가치법</td><td>(최종 판매가 − 추가가공원가) 비율</td><td>33-71, 35-76</td></tr>
      <tr><td>균등이익률법</td><td>전체 매출총이익률을 모든 제품에 동일하게 → 제품 원가 = 매출 × (1 − 이익률) − 추가가공원가 = 결합원가 몫</td><td>28-71, 34-76</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>부산물</h3><p>생산기준법: 부산물 NRV만큼 결합원가에서 먼저 빼고 주산물에 배분(35-76). 판매기준법: 배분에서 제외하고 팔 때 잡이익(28-71).</p></div>
    <div class="mini"><h3>역산 문제</h3><p>한 제품의 결합원가 몫을 알면 '그 제품 비율 = 몫 ÷ 결합원가'로 전체 판매가치나 NRV를 거꾸로 구한다(33-71: 30 ÷ 120 = 25%).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>추가가공 판단에 결합원가를 넣음(31-74 ㅁ).</span>
    <span>가격만 오르면 가공한다(30-73 X: 증분 3,000 &lt; 3,500).</span>
    <span>순실현가치법인데 최종 판매가 비율로 나눔.</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>결합원가 배분의 개념 비판, 연산품 재고 평가 세부는 넘긴다.</span></div>
  <p class="mine"></p>
</section>

<!-- 33. 표준원가 · 차이분석 -->
<section id="sv" class="sec" aria-labelledby="h-sv">
  <div class="shead"><h2 id="h-sv">표준원가 · 차이분석</h2><span class="badge hi">비중 상 · 9문항</span><span class="lec">33단원</span></div>
  <div class="key">거의 매년 1문항, 대부분 <b>역산</b>(실제시간·생산량·실제원가를 거꾸로). 3단 막대 하나로 다 풀린다: <b>AQ × AP | AQ × SP | SQ × SP</b>, 앞 칸 차이 = 가격(임률), 뒤 칸 차이 = 능률(수량).<small>SQ(SH) = 실제생산량 × 단위당 표준수량(시간). 실제가 더 크면 불리.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 9문항. ① 노무 차이 역산(28·31·33회) ② 재료 차이·재고(35·36회) ③ 제조간접 배부·조업도차이(32·34·37회) ④ O·X(30회)</p>
  <div class="lab">
    <h3>3단 차이 계산기 · 31회 75번 기본값(직접노무)</h3>
''' + sl('sv1','실제시간 AQ',0,80000,500,55000) + sl('sv2','실제임률 AP',0,20,0.5,10) + sl('sv3','표준임률 SP',0,20,0.5,12) + sl('sv4','표준시간 SQ(생산량 × 단위당)',0,80000,500,50000) + '''    <div class="readout" id="svOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>제조간접원가</th><th>차이</th><th>계산</th></tr></thead>
    <tbody>
      <tr><td>변동</td><td>소비 · 능률</td><td>실제 − AH × SR / (AH − SH) × SR</td></tr>
      <tr><td>고정</td><td>예산 · 조업도</td><td>실제 − 고정예산 / (기준조업도 − SH) × 고정배부율</td></tr>
      <tr><td>배부액</td><td colspan="2">표준배부율 × <b>SH</b>(실제시간 아님, 34-73)</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>재료 구입 vs 사용</h3><p>가격차이를 구입시점에 떼면 '구입량' 기준, 능률차이는 언제나 '사용량' 기준(30-76 ㄷ). 구입량 − 사용량 = 재고 증가(35-74).</p></div>
    <div class="mini"><h3>역산 순서</h3><p>주어진 차이 하나로 모르는 값 하나: 임률차이 → AH(31-75 · 33-80), AH·SR → 능률차이로 SH → 생산량(28-72 · 32-74), 총차이 → 표준원가 → SQ(36-75).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>배부·조업도차이에 실제시간을 씀(34-73 · 37-75 ④).</span>
    <span>구입가격차이를 사용량으로(35-74).</span>
    <span>유리·불리 방향을 반대로(임률 유리 = 실제임률이 낮다).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>배합차이·수율차이, 차이의 회계처리(비례배분)는 넘긴다. 3단 막대와 고정제조간접 조업도차이만.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#pr">종합원가</a>','<a href="#pr">종합원가</a><a href="#jc">결합원가</a><a href="#sv">표준원가</a>',1)
h=h.replace('["종합원가·공손","#pr","31단원",9,"hi"],','["종합원가·공손","#pr","31단원",9,"hi"],["결합원가","#jc","32단원",7,"mid"],["표준원가·차이분석","#sv","33단원",9,"hi"],',1)
a='      <tr data-sec="pr"><td>종합원가</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="jc"><td>결합원가</td><td>분리점 판매가치 · NRV(최종가 − 추가원가) · 균등이익률 · 추가가공 = 증분수익 vs 추가원가(결합원가 무시) · 부산물 생산기준 = NRV 먼저 차감</td></tr>
      <tr data-sec="sv"><td>표준원가</td><td>AQ×AP | AQ×SP | SQ×SP · 앞 = 가격(임률), 뒤 = 능률 · 배부 = SR × SH · 조업도차이 = (기준 − SH) × 고정배부율 · 구입가격차이 = 구입량 기준</td></tr>
'''+h[j:]
js='''
/* 32. 추가가공 */
function jcCalc(){const v=["jc1","jc2","jc3","jc4"].map(i=>{$("#"+i+"Out").textContent=(+$("#"+i).value).toLocaleString();return +$("#"+i).value});
 const inc=v[0]*(v[2]-v[1]),g=inc-v[3];
 $("#jcOut").innerHTML=`증분수익 ${v[0].toLocaleString()} × (${v[2]} − ${v[1]}) = ${inc.toLocaleString()} − 추가가공원가 ${v[3].toLocaleString()} = <b>${g.toLocaleString()}</b> → ${g>0?"추가가공":g<0?"분리점에서 판매":"무차별"} (결합원가는 판단에 쓰지 않음)`}
["jc1","jc2","jc3","jc4"].forEach(i=>$("#"+i).addEventListener("input",jcCalc));jcCalc();
/* 33. 3단 차이 */
function svCalc(){const v=["sv1","sv2","sv3","sv4"].map(i=>{$("#"+i+"Out").textContent=(+$("#"+i).value).toLocaleString();return +$("#"+i).value});
 const a=v[0]*v[1],b=v[0]*v[2],c=v[3]*v[2],t=x=>x===0?"0":`${Math.abs(x).toLocaleString()}(${x>0?"불리":"유리"})`;
 $("#svOut").innerHTML=`${a.toLocaleString()} | ${b.toLocaleString()} | ${c.toLocaleString()} → 가격(임률)차이 <b>${t(a-b)}</b> · 능률차이 <b>${t(b-c)}</b> · 총차이 ${t(a-c)}`}
["sv1","sv2","sv3","sv4"].forEach(i=>$("#"+i).addEventListener("input",svCalc));svCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='K6': x['note']='jc'
    if x['u']=='K7': x['note']='sv'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
