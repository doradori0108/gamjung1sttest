import json,re
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
h=h.replace('<section id="pf" class="sec" aria-labelledby="h-pf">','<section id="pf" class="sec" data-lec="20" aria-labelledby="h-pf">',1)
h=h.replace('<span class="lec">20강~ (수강 중)</span>','<span class="lec">20~21강</span>',1)
old_foot='  <p class="foot">20강(장기생산함수)까지 들은 내용만 넣었습니다. 이 단원 기출 9문항은 규모에 대한 수익(21강)까지 들으면 문제풀이에 열립니다.</p>\n'
assert old_foot in h
add='''  <h3>규모에 대한 수익 (21강) · "모든 투입을 t배 하면?"</h3>
  <div class="tw c1"><table>
    <thead><tr><th>t배 투입 → 산출</th><th>이름</th><th>동차 차수 k</th><th>예</th></tr></thead>
    <tbody>
      <tr><td>t배보다 많이</td><td><b>규모수익 체증</b></td><td>k &gt; 1</td><td>Q = 2L² + 2K² (k = 2, 29회 59번)</td></tr>
      <tr><td>딱 t배</td><td><b>불변</b></td><td>k = 1</td><td>Q = L<sup>1/3</sup>K<sup>2/3</sup> · min{L, K} · L + 3K</td></tr>
      <tr><td>t배보다 적게</td><td><b>체감</b></td><td>k &lt; 1 (0차 포함)</td><td>Q = L<sup>0.3</sup>K<sup>0.3</sup> · 0차 동차(34회 46번)</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>한계생산 체감(단기)</h3><p>자본은 그대로, <b>노동만</b> 늘릴 때 노동 1단위가 더하는 생산량이 줄어든다. 도로 현장에 장비는 그대로인데 인부만 계속 투입하는 상황.</p></div>
    <div class="mini"><h3>규모수익(장기)</h3><p>장비와 인부를 <b>함께</b> 같은 비율로 늘릴 때 이야기. 한계생산이 체감해도 규모수익은 불변·체증일 수 있다(콥-더글러스 L<sup>1/3</sup>K<sup>2/3</sup>).</p></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>콥-더글러스 Q = AL<sup>α</sup>K<sup>β</sup> 4종 세트</th><th>37회 45번 L<sup>1/3</sup>K<sup>2/3</sup></th></tr></thead>
    <tbody>
      <tr><td>규모수익 = α + β와 1 비교</td><td>1 → 불변 · 1차 동차</td></tr>
      <tr><td>MP<sub>L</sub> 체감 ⇔ α &lt; 1</td><td>1/3 &lt; 1 → 체감</td></tr>
      <tr><td>노동소득분배율 = α</td><td>1/3</td></tr>
      <tr><td>MRTS = (α/β)(K/L)</td><td><b>K/(2L)</b> (보기의 2K/L은 X)</td></tr>
      <tr><td>대체탄력성</td><td>항상 1 (완전대체 ∞ · 완전보완 0)</td></tr>
    </tbody>
  </table></div>
'''
h=h.replace(old_foot,add,1)
h=h.replace('<span>선형 생산함수에서 "노동이 늘면 MRTS가 감소한다" → X. 직선이므로 일정(30회 52번).</span></div>',
 '<span>선형 생산함수에서 "노동이 늘면 MRTS가 감소한다" → X. 직선이므로 일정(30회 52번).</span><span>0차 동차를 규모수익 불변으로 고른다. 불변은 1차 동차(34회 46번).</span><span>콥-더글러스 MRTS를 (β/α)(K/L)로 뒤집는다. 분자는 노동 지수(37회 45번).</span><span>"비용극소화 = 이윤극대화의 필요충분조건" → X. 필요조건(32회 48번).</span><span>기술진보는 종류와 무관하게 등량곡선을 원점 쪽으로 옮긴다(30회 45번).</span></div>\n  <div class="drop"><b>버려도 되는 주제</b><span>기술진보의 종류별 MRTS 변화(힉스 중립 · 노동절약적 정의 세부)는 10년간 1문항. 동차성 판정과 콥-더글러스 4종 세트만 확실히.</span></div>',1)
h=h.replace('["생산함수·등량곡선","#pf","20~21강",9,"mid","21강 후 열림"]','["생산함수·규모수익","#pf","20~21강",9,"mid","앱에서 표시"]',1)
h=h.replace('<tr><th>MRTS</th><td>MP<sub>L</sub>/MP<sub>K</sub> · 선형 = 일정 · min형 = 남는 요소 MP 0</td></tr>',
 '<tr><th>MRTS</th><td>MP<sub>L</sub>/MP<sub>K</sub> · 선형 = 일정 · min형 = 남는 요소 MP 0</td></tr>\n      <tr data-sec="pf"><th>규모수익</th><td>k차 동차: k &gt; 1 체증 · = 1 불변 · &lt; 1 체감(0차 포함) · 콥-더글러스는 α + β</td></tr>\n      <tr data-sec="pf"><th>콥-더글러스</th><td>MRTS = (α/β)(K/L) · 노동분배율 = α · σ = 1</td></tr>',1)
# generic header
h=re.sub(r'<div class="eyebrow">.*?</div>','<div class="eyebrow">감정평가사 1차 · 경제학원론 · 손병익 기본이론 · 수강한 강의까지 열림</div>',h,count=1)
h=re.sub(r'<p class="lede">.*?</p>','<p class="lede">제28~37회 경제학 400문항을 손병익 기본이론 강의 순서로 정리합니다. 자주 나온 순서대로 ‘결론 한 줄 → 그래프 → 함정 → 기출’이고, 그래프는 버튼과 슬라이더로 직접 움직여 볼 수 있습니다. 아직 수강 전인 주제는 앱의 🗺️ 진도를 올리면 열립니다.</p>',h,count=1,flags=re.S)
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=21
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
