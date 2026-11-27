import json
P='/home/claude/gamjung1sttest/notes/econ.html'; h=open(P).read()
assert 'id="trade"' not in h
sec='''<!-- 국제무역 -->
<section id="trade" class="sec" data-lec="60" aria-labelledby="h-trade">
  <div class="shead"><h2 id="h-trade">국제무역: 비교우위 · 관세 · 보호무역</h2><span class="badge lo">비중 하 · 4문항</span><span class="lec">60강</span></div>
  <div class="key">10년 4문항. <b>비교우위 = 기회비용이 작은 쪽</b>, 교역조건은 두 기회비용 사이. 관세는 <b>정부·국내 생산자 이득, 소비자 손해, 순손실 발생</b>.<small>기회비용 = 하나를 만들려고 포기하는 다른 것의 양. 소국 = 국제가격에 영향을 못 주는 나라.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · ① 교역조건 계산(37회) ② 관세의 이해관계(37회) ③ 교역 후 잉여 변화(33회) ④ 보호무역 논거(34회)</p>
  <div class="tw c1"><table>
    <thead><tr><th>37회 47번</th><th>쌀 1kg의 기회비용</th><th>특화</th></tr></thead>
    <tbody>
      <tr><td>A(쌀 60분, 밀 30분)</td><td>밀 2kg</td><td>쌀</td></tr>
      <tr><td>B(쌀 30분, 밀 10분)</td><td>밀 3kg</td><td>밀(쌀·밀 모두 절대우위지만 비교우위는 밀)</td></tr>
      <tr><td colspan="3">교환비율: 쌀 1kg = 밀 2~3kg 사이(2.5)</td></tr>
    </tbody>
  </table></div>
  <div class="tw c1"><table>
    <thead><tr><th>소국 관세</th><th>변화</th></tr></thead>
    <tbody>
      <tr><td>국내가격</td><td>국제가격 + 관세로 상승</td></tr>
      <tr><td>소비자 잉여</td><td>감소</td></tr>
      <tr><td>생산자 잉여 · 정부 관세수입</td><td>증가</td></tr>
      <tr><td>총잉여</td><td>감소(순손실 = 과잉생산 + 과소소비 삼각형)</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>교역 후 잉여</h3><p>수입국: 가격 ↓ → 소비자 ↑, 생산자 ↓, 총잉여 ↑. 수출국: 가격 ↑ → 생산자 ↑, 소비자 ↓, 총잉여 ↑.</p></div>
    <div class="mini"><h3>보호무역 논거</h3><p>국가안보, 유치산업 보호, 환경(오염도피처), 미숙련 노동자 임금. 관세의 순손실은 반대로 '자유무역' 논거(34-79 ②).</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>절대우위로 특화를 판단.</span>
    <span>관세로 소비자도 이득(37-77 ㄷ).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>헥셔-올린 · 립진스키 · 스톨퍼-사무엘슨 정리, 대국 관세의 교역조건 효과, 수입할당은 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 11. 암기카드 -->',sec+'<!-- 11. 암기카드 -->',1)
h=h.replace('<a href="#fx">환율·먼델플레밍</a>','<a href="#fx">환율·먼델플레밍</a><a href="#trade">국제무역</a>',1)
h=h.replace('["환율·국제수지·먼델-플레밍","#fx","59강",20,"hi","앱에서 표시"],','["환율·국제수지·먼델-플레밍","#fx","59강",20,"hi","앱에서 표시"],["국제무역","#trade","60강",4,"lo","앱에서 표시"],',1)
a='      <tr data-sec="fx"><th>먼델-플레밍</th>'
i=h.index(a); j=h.index('\\n',i)+1 if False else h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="trade"><th>국제무역</th><td>비교우위 = 기회비용 작은 쪽 · 교역조건은 두 기회비용 사이 · 소국 관세: 정부·생산자 ↑, 소비자 ↓, 순손실</td></tr>
'''+h[j:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/econ/units.json'; u=json.load(open(U)); u['dataThrough']=60
u['mapNote']='단원은 손병익 기본이론 강의 순서에 맞춰 나눴습니다. 10년치 기출 전 단원이 들어 있고, 진도로 설정한 강까지만 출제됩니다.'
for x in u['units']:
    if x['u']=='U27': x['note']='trade'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
