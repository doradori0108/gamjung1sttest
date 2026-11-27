import json,re
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="ad"' not in h and not re.search(r'id="gw\d|gwOut|function gwCalc',h)
sec='''<!-- 26. 기타 기준 -->
<section id="ad" class="sec" aria-labelledby="h-ad">
  <div class="shead"><h2 id="h-ad">기타 기준: 사업결합 · 관계기업 · 환율 · 매각예정 · 공정가치</h2><span class="badge mid">비중 중 · 16문항</span><span class="lec">26단원</span></div>
  <div class="key">네 덩어리가 각자 1~2문항씩 나온다. <b>영업권</b> = 이전대가 − 순자산 공정가치, <b>지분법</b> = 순자산 변동 × 지분율, <b>외화</b> = 화폐성은 기말환율·비화폐성은 거래일 환율, <b>매각예정</b> = 작은 금액 + 상각 중단.<small>이전대가 = 합병하려고 넘긴 것(현금·주식·자산)의 공정가치. 순자산 = 자산 − 부채.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 16문항, 매년 1~3문항. ① 영업권 계산(28·29·30·36·37회) ② 지분법 장부금액(34·37회) ③ 외화 환산 계산·O·X(31·33·35·36·37회) ④ 매각예정 O·X·계산(33·35·36회) ⑤ 공정가치 측정 O·X(32회)</p>
  <div class="lab">
    <h3>영업권 계산기 · 37회 70번 기본값</h3>
    <div class="slider"><label for="gw1">이전대가(기존지분 공정가치 + 주식 + 조건부대가)</label><input type="range" id="gw1" min="500000" max="1200000" step="2000" value="974000"><output id="gw1Out">974000</output></div>
    <div class="slider"><label for="gw2">피취득자 순자산 공정가치</label><input type="range" id="gw2" min="300000" max="1000000" step="10000" value="800000"><output id="gw2Out">800000</output></div>
    <div class="slider"><label for="gw3">새로 인식하는 무형자산</label><input type="range" id="gw3" min="0" max="100000" step="2000" value="20000"><output id="gw3Out">20000</output></div>
    <div class="slider"><label for="gw4">우발부채(현재의무 · 신뢰성 있게 측정)</label><input type="range" id="gw4" min="0" max="100000" step="2000" value="6000"><output id="gw4Out">6000</output></div>
    <div class="readout" id="gwOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>사업결합 항목</th><th>영업권 계산에서</th></tr></thead>
    <tbody>
      <tr><td>주식 발행</td><td>액면 X, <b>공정가치</b>로 이전대가</td></tr>
      <tr><td>토지 등 자산 지급</td><td>장부 X, 공정가치로 이전대가</td></tr>
      <tr><td>조건부대가</td><td>공정가치로 이전대가에 포함</td></tr>
      <tr><td>단계적 취득 시 기존 보유 지분</td><td>취득일 공정가치로 재측정해 포함</td></tr>
      <tr><td>새로 식별한 무형자산(개발프로젝트 등)</td><td>순자산에 더함</td></tr>
      <tr><td>우발부채(현재의무 + 측정 가능)</td><td>순자산에서 뺌(일반 충당부채보다 넓게 인식)</td></tr>
      <tr><td>취득 관련 원가(수수료·취득세)</td><td>무시(비용 또는 자산 원가)</td></tr>
    </tbody>
  </table></div>
  <div class="tw c1"><table>
    <thead><tr><th>외화 환산</th><th>적용 환율</th><th>환산 차이</th><th>예</th></tr></thead>
    <tbody>
      <tr><td>화폐성(현금·채권·사채·충당부채·현금배당 부채)</td><td>마감(기말)환율</td><td>당기손익</td><td>35-61</td></tr>
      <tr><td>비화폐성 · 역사적원가(원가모형 토지)</td><td>거래일 환율 고정</td><td>없음</td><td>33-67</td></tr>
      <tr><td>비화폐성 · 공정가치(재평가모형)</td><td>공정가치 측정일 환율</td><td>평가손익 따라감(재평가 → OCI)</td><td>31-43</td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>지분법 장부금액</h3><p>취득원가 + (순이익 − 공정가치 차액 상각 − 미실현이익) × 지분율 + OCI × 지분율 − 받은 배당. 34-68: 300,000 + 16,000 + 6,000 − 3,000 = 319,000. 토지 차액은 상각 안 함.</p></div>
    <div class="mini"><h3>매각예정</h3><p>min(장부금액, 순공정가치), 사용가치는 안 봄. 분류 후 감가상각 중단, 부채 이자는 계속. 재측정 손익은 중단영업이 아니면 계속영업손익. 36-53: 250,000 → 200,000 → 190,000.</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>주식 이전대가를 액면으로(28-65).</span>
    <span>합병하는 회사 자료로 계산(28-65 표에 (주)감평 자료가 같이 있음).</span>
    <span>받은 배당을 수익으로, 미실현이익을 전액 제거(34-68 · 37-69).</span>
    <span>원가모형 외화 토지를 기말환율로 다시 환산(33-67).</span>
    <span>매각예정 '큰 금액'·'상각 계속'(33-70 · 35-68).</span>
    <span>공정가치 투입변수: 관측 가능 최대 ↔ 관측 불가 최소 뒤집기(32-43).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>연결재무제표 작성(비지배지분 세부), 해외사업장 환산(표시통화 환산 절차), 지분법 손실 누적·중단은 넘긴다. 영업권·지분법 기본 계산과 환율 3분법만 확실히. 35-61(외화사채)은 전항 정답이라 흐름만 보면 된다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#ra">재무비율</a>','<a href="#ra">재무비율</a><a href="#ad">사업결합·환율</a>',1)
h=h.replace('["재무비율 분석","#ra","25단원",6,"mid"],','["재무비율 분석","#ra","25단원",6,"mid"],["사업결합·관계기업·환율·매각예정","#ad","26단원",16,"mid"],',1)
a='      <tr data-sec="ra"><td>재무비율</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="ad"><td>영업권 · 지분법</td><td>영업권 = 이전대가(공정가치, 기존지분·조건부대가 포함) − 순자산 공정가치(+ 무형자산 − 우발부채) · 지분법 = (NI − 차액상각 − 미실현) × % + OCI × % − 배당</td></tr>
      <tr data-sec="ad"><td>환율 · 매각예정</td><td>화폐성 = 기말 / 원가 비화폐성 = 거래일 / 공정가치 비화폐성 = 측정일 · 매각예정 = min(장부, 순공정가치), 상각 중단</td></tr>
'''+h[j:]
js='''
/* 26. 영업권 */
function gwCalc(){const v=["gw1","gw2","gw3","gw4"].map(i=>{$("#"+i+"Out").textContent=(+$("#"+i).value).toLocaleString();return +$("#"+i).value});
 const na=v[1]+v[2]-v[3],g=v[0]-na;
 $("#gwOut").innerHTML=`식별가능 순자산 ${na.toLocaleString()} → ${g>=0?`영업권 <b>₩${g.toLocaleString()}</b>`:`염가매수차익 <b>₩${(-g).toLocaleString()}</b>(당기이익)`}`}
["gw1","gw2","gw3","gw4"].forEach(i=>$("#"+i).addEventListener("input",gwCalc));gwCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    if x['u']=='AD': x['note']='ad'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
