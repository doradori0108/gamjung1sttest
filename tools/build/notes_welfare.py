import json
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="welfare"' not in h
sec='''<!-- 일반균형 · 후생경제 -->
<section id="welfare" class="sec" data-lec="32" aria-labelledby="h-welfare">
  <div class="shead"><h2 id="h-welfare">일반균형 · 후생경제</h2><span class="badge hi">비중 상 · 12문항</span><span class="lec">32~34강</span></div>
  <div class="key">효율 3단계: 교환(MRS 일치) · 생산(MRTS 일치) · 종합(MRS = MRT). 후생경제학 제1정리 = 완전경쟁이면 효율, 제2정리 = 효율적 배분은 초기부존 재분배로 달성 가능.<small>에지워스 상자 = 두 사람(또는 두 재화 생산)의 배분을 한 상자에 그린 그림. 계약곡선 = 효율적 배분 점들.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1~2문항. ① 순수교환 일반균형 가격(29·31·33회) ② 계약곡선·파레토 개선(28·31회) ③ 후생정리 O·X(32·34회) ④ 사회후생함수·애로우·차선(32·35·37회) ⑤ MRS = MRT 계산(37회 55번)</p>

  <h3>효율성 3단계</h3>
  <div class="tw c1"><table>
    <thead><tr><th>효율</th><th>조건</th><th>그림</th><th>옮기면</th></tr></thead>
    <tbody>
      <tr><td>교환(소비)</td><td>MRS<sub>A</sub> = MRS<sub>B</sub></td><td>소비자 상자의 계약곡선</td><td>효용가능곡선(U<sub>A</sub>–U<sub>B</sub>)</td></tr>
      <tr><td>생산</td><td>MRTS<sub>X</sub> = MRTS<sub>Y</sub></td><td>생산요소(L–K) 상자의 계약곡선</td><td><b>생산가능곡선(X–Y)</b> (37-54 ③)</td></tr>
      <tr><td>종합</td><td>MRS = MRT</td><td>생산가능곡선과 무차별곡선 접점</td><td>37-55: 2Y/X = X/Y → Y = 3</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>제1정리</h3><p>조건: 완전경쟁 · 단조성 · <b>외부성·공공재 없음</b> → 경쟁균형은 파레토 효율. '보이지 않는 손'의 근거(사익 = 공익).</p></div>
    <div class="mini"><h3>제2정리</h3><p>추가 조건: 선호·기술의 <b>볼록성</b>. 형평은 초기부존 재분배(정액 이전)로, 가격은 시장에. "가격 개입 정당화" X(34-55).</p></div>
  </div>

  <h3>순수교환 일반균형 가격 찾기</h3>
  <ol class="steps">
    <li>보기 가격을 넣어 각자 소득(= 부존 가치)과 수요를 구한다</li>
    <li>한 재화 시장만 청산되면 끝(왈라스 법칙). 33-56: P<sub>Y</sub> = 1 → X 45 + 45 = 90 ✓</li>
    <li>완전대체 소비자가 있으면 가격비 = 그 사람의 MRS(29-58: 1)</li>
  </ol>

  <div class="lab">
    <h3>사회후생함수 비교 · 효용 100을 A·B에 나누기</h3>
    <div class="slider"><label for="wf1">A의 효용</label><input type="range" id="wf1" min="0" max="100" step="5" value="70"><output id="wf1Out">70</output></div>
    <div class="readout" id="wfOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>가치판단</th><th>사회후생함수</th><th>사회무차별곡선</th></tr></thead>
    <tbody>
      <tr><td>공리주의</td><td>W = U<sub>A</sub> + U<sub>B</sub></td><td><b>직선</b>(37-56 ㄷ)</td></tr>
      <tr><td>평등주의</td><td>효용 차이를 반영</td><td>원점에 <b>볼록</b>(평등 강할수록 더, 35-55 ①)</td></tr>
      <tr><td>롤즈</td><td>W = min{U<sub>A</sub>, U<sub>B</sub>}</td><td><b>L자</b>(최소극대화)</td></tr>
    </tbody>
  </table></div>
  <p class="foot">애로우 불가능성 정리: 완비·이행성, 파레토원칙(만장일치 선호 존중, 과반수제 X), 무관한 대안 독립, 비독재성을 모두 만족하는 규칙은 없다. 차선의 이론: 하나가 깨져 있으면 나머지를 고치는 게 더 나쁠 수도 있다(도로 정비 순서를 바꾸면 오히려 정체가 커지는 것과 비슷).</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>파레토 효율 = '개선 가능한 상태' → X. 불가능한 상태(32-49 ①).</span>
    <span>제1정리에 '외부성 존재' → X(32-49 ③).</span>
    <span>평등주의 → 오목 → X. 볼록(35-55).</span>
    <span>생산가능곡선을 L–K 평면 → X(37-54).</span>
    <span>파레토 개선 판단 시 한 사람만 본다. 두 사람 효용을 모두 계산(31-58 ㄴ).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>왈라스 법칙의 증명, 코어(core) 개념, 일반균형 존재 정리는 출제가 드물다. 효율 3단계 표와 사회후생 표만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#factor">요소시장·분배</a>','<a href="#factor">요소시장·분배</a><a href="#welfare">일반균형·후생</a>',1)
h=h.replace('["요소시장·소득분배","#factor","30~31강",15,"hi","앱에서 표시"]','["요소시장·소득분배","#factor","30~31강",15,"hi","앱에서 표시"],["일반균형·후생경제","#welfare","32~34강",12,"hi","앱에서 표시"]',1)
a='      <tr data-sec="factor"><th>지대 · 분배</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="welfare"><th>효율 3단계</th><td>교환 MRS 일치 · 생산 MRTS 일치 · 종합 MRS = MRT / 1정리 경쟁 → 효율, 2정리 재분배는 초기부존으로</td></tr>
      <tr data-sec="welfare"><th>사회후생</th><td>공리주의 직선 · 평등주의 볼록 · 롤즈 L자 · 애로우 파레토원칙 = 만장일치</td></tr>
'''+h[j:]
js='''
/* 후생: 사회후생함수 비교 */
function wfCalc(){const a=+$("#wf1").value,b=100-a;$("#wf1Out").textContent=a;
 $("#wfOut").innerHTML=`U<sub>A</sub> = ${a}, U<sub>B</sub> = ${b} → 공리주의 W = <b>${a+b}</b>(어떻게 나눠도 같음) · 롤즈 W = <b>${Math.min(a,b)}</b>(50 : 50일 때 최대) · 곱(평등주의 예) W = <b>${a*b}</b>`}
$("#wf1").addEventListener("input",wfCalc);wfCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=34
for x in u['units']:
    if x['u']=='U16': x['note']='welfare'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
