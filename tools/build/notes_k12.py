import json,re
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="kf"' not in h and 'id="jo"' not in h and not re.search(r'id="(kf|jo)\d|kfOut|joOut|function (kfCalc|joCalc)',h)
def sl(i,lab,mn,mx,st,v): return f'    <div class="slider"><label for="{i}">{lab}</label><input type="range" id="{i}" min="{mn}" max="{mx}" step="{st}" value="{v}"><output id="{i}Out">{v}</output></div>\n'
sec='''<!-- 27. 원가 개념 · 원가흐름 -->
<section id="kf" class="sec" aria-labelledby="h-kf">
  <div class="shead"><h2 id="h-kf">원가 개념 · 원가흐름</h2><span class="badge hi">비중 상 · 10문항</span><span class="lec">27단원</span></div>
  <div class="key">원가관리회계(71~80번)의 첫 관문. <b>재료 → 재공품 → 제품 → 매출원가</b> 세 번의 '기초 + 투입 − 기말'만 할 줄 알면 매년 1문항이 거의 공짜. 거꾸로 묻는 문제(매출액 → 매출원가 → … → 재료 매입)가 절반.<small>재공품 = 만들다 만 것. 당기제품제조원가 = 이번에 완성된 제품의 원가. 매출총이익률 30% = 매출원가는 매출의 70%.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 10문항, 거의 매년 1문항. ① 원가흐름 계산(29·30·31·36·37회) ② 원가행태 표 채우기·고저점법(28·32회) ③ 원가 용어 O·X(33회) ④ 원가가산 가격(29회) ⑤ 학습곡선(31회)</p>
  <div class="lab">
    <h3>원가흐름 계산기 · 29회 80번 기본값</h3>
''' + sl('kf1','당기총제조원가(재료 사용 + 노무 + 간접)',0,200000,1000,106000) + sl('kf2','기초재공품',0,100000,1000,60000) + sl('kf3','기말재공품',0,100000,1000,30000) + sl('kf4','기초제품',0,100000,1000,45000) + sl('kf5','기말제품',0,100000,1000,60000) + '''    <div class="readout" id="kfOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>T계정</th><th>차변(들어온 것)</th><th>대변(나간 것)</th></tr></thead>
    <tbody>
      <tr><td>원재료</td><td>기초 + 매입</td><td>사용액(→ 재공품) + 기말</td></tr>
      <tr><td>재공품</td><td>기초 + 재료 사용 + 노무 + 제조간접</td><td>당기제품제조원가(→ 제품) + 기말</td></tr>
      <tr><td>제품</td><td>기초 + 당기제품제조원가</td><td>매출원가 + 기말</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>원가 분류</h3><p>기초(기본)원가 = 재료 + 노무, 가공(전환)원가 = 노무 + 간접(노무는 양쪽). 제조원가 + 판관비 = 총원가, + 영업이익 = 판매가격(29-72). 노무원가는 지급액 X, 발생액 O(31-71).</p></div>
    <div class="mini"><h3>원가행태(관련범위 안)</h3><p>변동원가: 총액 ∝ 조업도, 단위당 일정. 고정원가: 총액 일정, 단위당 ↓. 고저점법은 '조업도' 최고·최저 두 점(28-76). 누적평균 학습곡선: 누적량 2배 → 누적 평균시간 × 학습률, 추가분 = 새 총시간 − 기존 총시간(31-79).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>재료 '사용액'을 '매입액'으로 답함(30-71).</span>
    <span>제품제조원가에서 멈추고 매출원가로 안 감(29-80 ④).</span>
    <span>총변동원가가 일정하다(33-72 ②). 일정한 건 단위당.</span>
    <span>고저점법을 원가 최고·최저로(28-76).</span>
    <span>학습곡선 추가분인데 누적 총시간 전체를 곱함(31-79 ⑤).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>원가 용어의 세부 분류(기회원가·매몰원가는 관련원가 단원에서), 학습곡선의 증분단위시간 모형, 회귀분석 원가추정은 넘긴다. 원가흐름 T계정 세 개만 손에 익히면 된다.</span></div>
  <p class="mine"></p>
</section>

<!-- 28. 개별원가 · 정상원가 -->
<section id="jo" class="sec" aria-labelledby="h-jo">
  <div class="shead"><h2 id="h-jo">개별원가 · 정상원가</h2><span class="badge mid">비중 중 · 7문항</span><span class="lec">28단원</span></div>
  <div class="key">제조간접원가는 작업마다 직접 못 붙이니 <b>배부율 × 배부기준</b>으로 나눠 준다. 정상원가는 연초에 정한 <b>예정배부율</b>을 쓰고, 연말에 실제와의 차이(배부차이)를 조정한다.<small>예정배부율 = 제조간접원가 예산 ÷ 예정조업도. 배부액 = 예정배부율 × 실제조업도. 과소배부 = 실제 &gt; 배부액(원가를 덜 잡음).</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 7문항. ① 배부차이와 매출총이익(30·34·36회) ② 예정배부율·실제조업도 역산(32·35회) ③ 실제배부율 배부(29회) ④ 기말재공품 원가 구성(37회)</p>
  <div class="lab">
    <h3>예정배부 · 배부차이 · 30회 72번 기본값</h3>
''' + sl('jo1','제조간접원가 예산',100000,1000000,10000,600000) + sl('jo2','예정조업도(시간)',5000,40000,1000,20000) + sl('jo3','실제조업도(시간)',5000,40000,1000,18000) + sl('jo4','실제 제조간접원가',100000,1000000,10000,650000) + '''    <div class="readout" id="joOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>실제원가</th><th>정상원가</th><th>표준원가(33단원)</th></tr></thead>
    <tbody>
      <tr><td>직접재료 · 노무</td><td>실제</td><td>실제</td><td>표준</td></tr>
      <tr><td>제조간접</td><td>실제배부율 × 실제조업도</td><td><b>예정배부율 × 실제조업도</b></td><td>표준배부율 × 표준조업도</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>배부차이 조정</h3><p>제조간접원가 T계정: 차변 실제, 대변 배부. 차변이 크면 과소배부 → 매출원가 ↑(이익 ↓). ① 매출원가조정법: 전액 매출원가 ② 총원가비례법: 재공품·제품·매출원가 잔액 비율(원재료 제외, 36-72) ③ 원가요소법: 각 계정 속 배부액 비율.</p></div>
    <div class="mini"><h3>거꾸로 풀기</h3><p>매출원가 → 제품제조원가 → 총제조원가 → 재료·노무 빼면 간접 배부액(35-71). 조정 후 매출원가 − 조정 전 = 배부차이 → 실제 = 배부액 ± 차이(34-78).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>배부액을 예정조업도로 계산(배부는 '실제'조업도).</span>
    <span>과소배부를 이익 증가로(30-72).</span>
    <span>총원가비례법에 원재료를 넣음(36-72).</span>
    <span>실제조업도 역산에 실제 간접원가를 씀(32-76).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>원가요소별 비례배분법의 세부 계산, 부문별 예정배부율은 넘긴다. 예정배부율 공식과 '과소배부 = 매출원가 ↑'만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#ad">사업결합·환율</a>','<a href="#ad">사업결합·환율</a><a href="#kf">원가흐름</a><a href="#jo">정상원가</a>',1)
h=h.replace('["사업결합·관계기업·환율·매각예정","#ad","26단원",16,"mid"],','["사업결합·관계기업·환율·매각예정","#ad","26단원",16,"mid"],["원가 개념·원가흐름","#kf","27단원",10,"hi"],["개별원가·정상원가","#jo","28단원",7,"mid"],',1)
a='      <tr data-sec="ad"><td>환율 · 매각예정</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="kf"><td>원가흐름</td><td>재료 사용 = 기초 + 매입 − 기말 → 제품제조원가 = 기초재공 + 총제조 − 기말재공 → 매출원가 = 기초제품 + 제품제조 − 기말제품 · 기초원가 = 재료 + 노무, 가공원가 = 노무 + 간접</td></tr>
      <tr data-sec="jo"><td>정상원가</td><td>예정배부율 = 예산 ÷ 예정조업도 · 배부액 = 배부율 × 실제조업도 · 과소배부(실제 &gt; 배부) → 매출원가 ↑ · 총원가비례 = 재공·제품·매출원가(원재료 X)</td></tr>
'''+h[j:]
js='''
/* 27. 원가흐름 */
function kfCalc(){const v=["kf1","kf2","kf3","kf4","kf5"].map(i=>{$("#"+i+"Out").textContent=(+$("#"+i).value).toLocaleString();return +$("#"+i).value});
 const m=v[1]+v[0]-v[2],c=v[3]+m-v[4];
 $("#kfOut").innerHTML=`당기제품제조원가 = ${v[1].toLocaleString()} + ${v[0].toLocaleString()} − ${v[2].toLocaleString()} = <b>${m.toLocaleString()}</b> → 매출원가 = ${v[3].toLocaleString()} + ${m.toLocaleString()} − ${v[4].toLocaleString()} = <b>${c.toLocaleString()}</b>`}
["kf1","kf2","kf3","kf4","kf5"].forEach(i=>$("#"+i).addEventListener("input",kfCalc));kfCalc();
/* 28. 정상원가 */
function joCalc(){const v=["jo1","jo2","jo3","jo4"].map(i=>{$("#"+i+"Out").textContent=(+$("#"+i).value).toLocaleString();return +$("#"+i).value});
 const r=v[0]/v[1],ap=r*v[2],d=v[3]-ap;
 $("#joOut").innerHTML=`예정배부율 ${(Math.round(r*100)/100).toLocaleString()} · 배부액 ${Math.round(ap).toLocaleString()} · ${Math.abs(d)<0.5?"배부차이 없음":d>0?`<b>과소배부 ${Math.round(d).toLocaleString()}</b> → 매출원가 ↑, 이익 ↓`:`<b>과대배부 ${Math.round(-d).toLocaleString()}</b> → 매출원가 ↓, 이익 ↑`}`}
["jo1","jo2","jo3","jo4"].forEach(i=>$("#"+i).addEventListener("input",joCalc));joCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='K1': x['note']='kf'
    if x['u']=='K2': x['note']='jo'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
