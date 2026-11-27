import json,re
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert not re.search(r'id="(sp|abc|pr)"|id="(sp|pr)\d|spOut|prOut|function (spCalc|prCalc)',h)
def sl(i,lab,mn,mx,st,v): return f'    <div class="slider"><label for="{i}">{lab}</label><input type="range" id="{i}" min="{mn}" max="{mx}" step="{st}" value="{v}"><output id="{i}Out">{v}</output></div>\n'
sec='''<!-- 29. 보조부문 원가배분 -->
<section id="sp" class="sec" aria-labelledby="h-sp">
  <div class="shead"><h2 id="h-sp">보조부문 원가배분</h2><span class="badge mid">비중 중 · 5문항</span><span class="lec">29단원</span></div>
  <div class="key">수선·동력 같은 보조부문의 원가를 제조부문으로 넘기는 방법 3가지. 시험은 거의 <b>상호배분법 연립방정식</b>이고, 답을 거꾸로(배부 전 원가 · 용역비율) 묻는다.<small>보조부문 = 직접 제품을 만들지 않고 제조부문을 돕는 부문. 용역제공비율 = 그 부문 서비스를 누가 몇 % 썼나.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 5문항(29·31·33·35·37회). ① 상호배분법 역산(배부 전 원가 · 용역비율) ② 직접배분법 배분액</p>
  <div class="lab">
    <h3>상호배분법 계산기 · 33회 74번 기본값</h3>
''' + sl('sp1','S1 배부 전 원가',0,500,10,90) + sl('sp2','S2 배부 전 원가',0,500,10,180) + sl('sp3','S1 → S2 비율(%)',0,80,5,50) + sl('sp4','S2 → S1 비율(%)',0,80,5,20) + '''    <div class="readout" id="spOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>방법</th><th>보조부문 간 용역</th><th>계산</th></tr></thead>
    <tbody>
      <tr><td>직접배분법</td><td>무시</td><td>제조부문 사용량 비율로만(분모에 보조부문 사용량 넣지 않기, 35-72)</td></tr>
      <tr><td>단계배분법</td><td>일부 반영(순서대로 한 방향)</td><td>먼저 배분한 부문은 다시 받지 않음</td></tr>
      <tr><td>상호배분법</td><td>전부 반영</td><td>S1 = 원가 + b·S2, S2 = 원가 + a·S1 연립</td></tr>
    </tbody>
  </table></div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>방정식 해(배분할 총원가)를 배부 전 원가로 답함(29-74 ⑤ · 37-78 ⑤).</span>
    <span>자기부문 소비(S2 → S2)를 빼지 않고 계산(37-78).</span>
    <span>보조부문이 제조부문에 준 총액 = 보조부문 배부 전 원가 합계(29-74 출발점).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>단계배분법 순서 결정 기준, 이중배분율법(변동·고정 나눠 배분)은 넘긴다. 상호배분법 방정식 하나면 된다.</span></div>
  <p class="mine"></p>
</section>

<!-- 30. 활동기준원가 -->
<section id="abc" class="sec" aria-labelledby="h-abc">
  <div class="shead"><h2 id="h-abc">활동기준원가(ABC)</h2><span class="badge lo">비중 하 · 3문항</span><span class="lec">30단원</span></div>
  <div class="key">계산은 하나뿐: <b>활동별 배부율 = 활동원가 ÷ 원가동인 총수량</b>, 제품 배부액 = Σ 배부율 × 제품이 쓴 원가동인. 거꾸로 '나머지 시간'·'기본원가'를 묻는다.<small>원가동인 = 그 활동 원가를 일으키는 요인(이동 횟수, 기계시간, 검사 횟수 등).</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 3문항(29·30·33회), 모두 계산.</p>
  <div class="tw c1"><table>
    <thead><tr><th>33회 76번</th><th>배부율</th><th>제품 A</th><th>제품 B</th></tr></thead>
    <tbody>
      <tr><td>자재주문 ₩55 / 55회</td><td>1</td><td>20</td><td>35</td></tr>
      <tr><td>품질검사 ₩84 / 28회</td><td>3</td><td>30</td><td>54</td></tr>
      <tr><td>기계수리 ₩180 / 180시간</td><td>1</td><td>80</td><td>100</td></tr>
      <tr><td>합계</td><td></td><td><b>130</b></td><td><b>189</b></td></tr>
    </tbody>
  </table></div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>제조원가 = 기본원가 + 제조간접원가. 기본원가를 묻는데 간접원가를 답함(30-74).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>활동 계층(단위·묶음·제품·설비 수준) 분류, ABC 도입 장단점 서술은 넘긴다.</span></div>
  <p class="mine"></p>
</section>

<!-- 31. 종합원가 -->
<section id="pr" class="sec" aria-labelledby="h-pr">
  <div class="shead"><h2 id="h-pr">종합원가 · 공손</h2><span class="badge hi">비중 상 · 9문항</span><span class="lec">31단원</span></div>
  <div class="key">거의 매년 1문항. 5단계(물량 → 환산량 → 단위원가 → 완성품·기말 배분)를 손에 익히고, 가중평균과 선입선출의 차이 <b>= 기초재공품 × 기초 완성도</b> 하나만 기억. 공손은 '<b>누가 검사를 통과했나</b>'.<small>완성품환산량 = 물량 × 완성도. 재료는 보통 공정 초 전량 투입(완성도 100%), 가공원가는 진행률만큼.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 9문항. ① 기말재공품 원가(28·31·33·34회) ② 두 방법 환산량 차이 역산(29·34회) ③ 정상·비정상 공손(32·35·36회) ④ 개념 O·X(37회)</p>
  <div class="lab">
    <h3>가공원가 완성품환산량 · 28회 77번 기본값</h3>
''' + sl('pr1','기초재공품 수량',0,3000,100,1000) + sl('pr2','기초 완성도(%)',0,100,5,40) + sl('pr3','당기 완성 수량',0,8000,100,4000) + sl('pr4','기말재공품 수량',0,3000,100,1000) + sl('pr5','기말 완성도(%)',0,100,5,40) + '''    <div class="readout" id="prOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>가중평균법</th><th>선입선출법</th></tr></thead>
    <tbody>
      <tr><td>환산량</td><td>완성품 + 기말 × 완성도</td><td>기초 × (1 − 기초 완성도) + 당기착수완성 + 기말 × 완성도</td></tr>
      <tr><td>단위원가 분자</td><td>기초재공품원가 + 당기투입원가</td><td><b>당기투입원가만</b></td></tr>
    </tbody>
  </table></div>
  <div class="grid2">
    <div class="mini"><h3>공손 3단계</h3><p>① 공손 수량 = 기초 + 착수 − 완성 − 기말 ② 당기 합격품 = 당기에 검사시점을 지난 것(기초가 이미 지났으면 제외, 기말이 아직이면 제외) ③ 정상공손 = 합격품 × %, 나머지는 비정상.</p></div>
    <div class="mini"><h3>공손 원가</h3><p>공손품 단위원가 = 재료 단위원가 + 가공 단위원가 × 검사시점. 정상공손원가는 합격품(완성품 · 검사 지난 기말)에, 비정상은 기간비용. 처분가치가 있으면 순정상공손원가만 배분.</p></div>
  </div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>선입선출 단위원가에 기초재공품원가를 섞음(31-73).</span>
    <span>전기에 검사를 지난 기초재공품을 당기 합격품에 넣음(32-72 ④ 57,200).</span>
    <span>정상·비정상 구분 이유를 '단위원가가 달라서'(37-76 ⑤). 피할 수 있느냐의 차이.</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>연속공정(전공정원가), 감손, 공손 재작업은 넘긴다. 5단계와 공손 3단계만.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#jo">정상원가</a>','<a href="#jo">정상원가</a><a href="#sp">보조부문</a><a href="#abc">ABC</a><a href="#pr">종합원가</a>',1)
h=h.replace('["개별원가·정상원가","#jo","28단원",7,"mid"],','["개별원가·정상원가","#jo","28단원",7,"mid"],["보조부문 원가배분","#sp","29단원",5,"mid"],["활동기준원가","#abc","30단원",3,"lo"],["종합원가·공손","#pr","31단원",9,"hi"],',1)
a='      <tr data-sec="jo"><td>정상원가</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="sp"><td>보조부문</td><td>직접(무시) · 단계(일부) · 상호(전부, 연립) · 방정식 해 = 배분할 총원가 ≠ 배부 전 원가 · 자기부문 소비는 빼고 비율 재계산</td></tr>
      <tr data-sec="abc"><td>ABC</td><td>배부율 = 활동원가 ÷ 원가동인 총수량 · 제조원가 = 기본원가 + 간접원가</td></tr>
      <tr data-sec="pr"><td>종합원가</td><td>평균 − 선입 환산량 = 기초 × 기초 완성도 · 선입선출 단위원가 = 당기원가만 · 정상공손 = 당기 합격품 × % · 공손 단위원가 = 재료 + 가공 × 검사시점</td></tr>
'''+h[j:]
js='''
/* 29. 상호배분 */
function spCalc(){const v=["sp1","sp2","sp3","sp4"].map(i=>{$("#"+i+"Out").textContent=$("#"+i).value;return +$("#"+i).value});
 const a=v[2]/100,b=v[3]/100,d=1-a*b;
 if(d<=0){$("#spOut").textContent="비율을 줄여 주세요";return}
 const S1=(v[0]+b*v[1])/d,S2=v[1]+a*S1,r=x=>Math.round(x*100)/100;
 $("#spOut").innerHTML=`S1 = ${v[0]} + ${b}·S2, S2 = ${v[1]} + ${a}·S1 → 배분할 총원가 S1 <b>${r(S1)}</b>, S2 <b>${r(S2)}</b> · 제조부문으로 가는 합계 = ${v[0]+v[1]}(배부 전 원가 합계와 같음)`}
["sp1","sp2","sp3","sp4"].forEach(i=>$("#"+i).addEventListener("input",spCalc));spCalc();
/* 31. 종합원가 환산량 */
function prCalc(){const v=["pr1","pr2","pr3","pr4","pr5"].map(i=>{$("#"+i+"Out").textContent=$("#"+i).value;return +$("#"+i).value});
 const wa=v[2]+v[3]*v[4]/100,fi=wa-v[0]*v[1]/100;
 $("#prOut").innerHTML=`가중평균 환산량 = ${v[2]} + ${v[3]} × ${v[4]}% = <b>${wa}</b> · 선입선출 = ${wa} − ${v[0]} × ${v[1]}% = <b>${fi}</b> (차이 = 기초재공품이 전기에 해 둔 작업량)`}
["pr1","pr2","pr3","pr4","pr5"].forEach(i=>$("#"+i).addEventListener("input",prCalc));prCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    x['note']={'K3':'sp','K4':'abc','K5':'pr'}.get(x['u'],x.get('note'))
    if x.get('note') is None: x.pop('note',None)
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok')
