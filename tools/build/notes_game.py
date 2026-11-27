import json
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="game"' not in h
sec='''<!-- 과점 · 게임이론 -->
<section id="game" class="sec" data-lec="28" aria-labelledby="h-game">
  <div class="shead"><h2 id="h-game">과점 · 게임이론</h2><span class="badge hi">비중 상 · 17문항</span><span class="lec">28~29강</span></div>
  <div class="key">과점 문제는 두 갈래다. 보수표가 나오면 '서로 최선인 칸(내쉬균형)' 찾기, 수요·비용함수가 나오면 꾸르노·슈타켈버그 반응함수 계산.<small>과점 = 소수 기업이 서로의 행동을 의식하는 시장. 내쉬균형 = 상대 전략이 주어졌을 때 아무도 혼자 바꿀 이유가 없는 상태.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 2문항. ① 보수행렬 내쉬균형·우월전략(28·29·31·34·36·37회) ② 꾸르노 균형(33회 57번 · 34회 49번) ③ 슈타켈버그(36회 49번) ④ 담합 배신(36회 51번) ⑤ 굴절수요·베르뜨랑·순차게임 이론</p>

  <div class="lab">
    <h3>보수행렬 실습 · 31회 52번 게임에서 a를 바꿔 보세요</h3>
    <div class="slider"><label for="gm1">a (둘 다 인상할 때 보수)</label><input type="range" id="gm1" min="-8" max="10" step="1" value="3"><output id="gm1Out">3</output></div>
    <div class="tw c1"><table><thead><tr><th>甲＼乙</th><th>인상</th><th>인하</th></tr></thead><tbody id="gmBody"></tbody></table></div>
    <div class="readout" id="gmOut" aria-live="polite"></div>
  </div>
  <p class="foot">밑줄 = 상대 전략에 대한 최선. 두 숫자 모두 밑줄인 칸이 내쉬균형. a &lt; 5면 용의자의 딜레마(둘 다 인하), a &gt; 5면 균형 2개.</p>

  <h3>내쉬균형 찾는 법 (밑줄 긋기)</h3>
  <ol class="steps">
    <li>상대의 각 전략(열)마다 내 보수 중 큰 것에 밑줄 → 행 기업 차례</li>
    <li>상대(열 기업)도 내 각 전략(행)마다 자기 보수 큰 것에 밑줄</li>
    <li>두 숫자 모두 밑줄 = 내쉬균형. 0개·1개·여러 개 모두 가능(28회 53번 3개)</li>
    <li>한 기업의 밑줄이 한 줄에 몰려 있으면 그게 <b>우월전략</b>(37회 46번 T사 광고)</li>
  </ol>

  <h3>수량경쟁 공식 (P = a − bQ, MC = c 동일)</h3>
  <div class="tw c1"><table>
    <thead><tr><th>모형</th><th>총생산량</th><th>특징 · 기출</th></tr></thead>
    <tbody>
      <tr><td>완전경쟁</td><td>(a − c)/b</td><td>P = MC</td></tr>
      <tr><td>꾸르노(n개)</td><td>완전경쟁 × <b>n/(n + 1)</b></td><td>상대 생산량 고정 추측 · 복점 2/3(34-49: 10 × 2/3)</td></tr>
      <tr><td>슈타켈버그</td><td>완전경쟁 × 3/4 (선도자 1/2)</td><td>추종자 반응함수를 대입(36-49: 50)</td></tr>
      <tr><td>담합(독점)</td><td>완전경쟁 × 1/2</td><td>배신 유인 → 불안정(36-51: 800 → 900)</td></tr>
      <tr><td>베르뜨랑(동질)</td><td>완전경쟁과 같음</td><td>가격경쟁 → P = MC. 차별화면 반응함수(28-49: P = 30)</td></tr>
    </tbody>
  </table></div>
  <ol class="steps">
    <li>MC가 다른 꾸르노(33회 57번): P = 120 − 2Q → A: 120 − 4q<sub>A</sub> − 2q<sub>B</sub> = 40, B: 120 − 2q<sub>A</sub> − 4q<sub>B</sub> = 20</li>
    <li>연립 → q<sub>A</sub> = 10, q<sub>B</sub> = 20 → Q = 30, P = 60 (MC가 낮은 기업이 더 많이)</li>
  </ol>
  <div class="grid2">
    <div class="mini"><h3>굴절수요(스위지)</h3><p>인상엔 안 따라오고 인하엔 따라옴(비대칭) → 꺾인 수요, MR 끊김 → 비용이 변해도 가격 경직(32-52).</p></div>
    <div class="mini"><h3>순차게임</h3><p>뒤에서부터(역진귀납). 먼저 움직이는 쪽이 '확약'으로 유리해질 수 있다(33-49). 완전균형 = 신빙성 없는 위협 제거.</p></div>
  </div>
  <p class="foot">도로공사 비유: 입찰 업체 둘이 서로 높게 쓰자 짜도(담합), 각자는 살짝 낮게 써서 낙찰받고 싶어 배신하는 구조가 용의자의 딜레마.</p>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>내쉬균형 = '상대와 관계없이 최선' → X. 그건 우월전략(34회 50번 ①).</span>
    <span>내쉬균형은 하나뿐 → X(34회 50번 ② · 34회 51번).</span>
    <span>꾸르노 = 담합 결과 → X. 꾸르노가 더 많이 생산(32회 53번).</span>
    <span>굴절수요가 '대칭적 반응' 때문 → X. 비대칭(32회 52번).</span>
    <span>문자 보수(α, a)를 구간별로 확인하지 않는다. 숫자를 하나 넣어 보기(30회 56번 · 31회 52번).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>혼합전략 내쉬균형 계산, 반복게임의 방아쇠 전략 세부, 경매 이론(승자의 불행 정도만)은 출제 빈도가 낮다. 밑줄 긋기와 꾸르노 공식만 확실히.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#mono">독점·가격차별</a>','<a href="#mono">독점·가격차별</a><a href="#game">과점·게임이론</a>',1)
h=h.replace('["독점·가격차별·독점적 경쟁","#mono","26~27강",21,"hi","앱에서 표시"]','["독점·가격차별·독점적 경쟁","#mono","26~27강",21,"hi","앱에서 표시"],["과점·게임이론","#game","28~29강",17,"hi","앱에서 표시"]',1)
a='      <tr data-sec="mono"><th>가격차별</th>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="game"><th>내쉬균형</th><td>상대 전략별 내 최선에 밑줄 → 둘 다 밑줄인 칸 · 우월전략균형 ⊂ 내쉬균형</td></tr>
      <tr data-sec="game"><th>과점 생산량</th><td>완전경쟁 대비: 꾸르노 n/(n + 1) · 슈타켈버그 3/4 · 담합 1/2</td></tr>
'''+h[j:]
js='''
/* 과점: 보수행렬 */
function drawGame(){const a=+$("#gm1").value;$("#gm1Out").textContent=a;
 const M=[[[a,a],[-5,5]],[[5,-5],[-1,-1]]],R=["인상","인하"];
 const b1=j=>M[0][j][0]>=M[1][j][0]?[0]:[]; const best1=j=>{const v=[M[0][j][0],M[1][j][0]],m=Math.max(...v);return [0,1].filter(i=>v[i]===m)};
 const best2=i=>{const v=[M[i][0][1],M[i][1][1]],m=Math.max(...v);return [0,1].filter(j=>v[j]===m)};
 const ne=[];let rows="";
 for(let i=0;i<2;i++){rows+=`<tr><td>${R[i]}</td>`;for(let j=0;j<2;j++){const u1=best1(j).includes(i),u2=best2(i).includes(j);if(u1&&u2)ne.push(`(${R[i]}, ${R[j]})`);
  rows+=`<td class="n" style="${u1&&u2?"background:var(--area1);font-weight:700":""}">(${u1?"<u>":""}${M[i][j][0]}${u1?"</u>":""}, ${u2?"<u>":""}${M[i][j][1]}${u2?"</u>":""})</td>`}rows+="</tr>"}
 $("#gmBody").innerHTML=rows;
 $("#gmOut").innerHTML=`내쉬균형: <b>${ne.join(" · ")||"없음"}</b> (${ne.length}개)${a<5?" · 인하가 두 사람의 우월전략(용의자의 딜레마)":""}`}
$("#gm1").addEventListener("input",drawGame);drawGame();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=29
for x in u['units']:
    if x['u']=='U14': x['note']='game'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
