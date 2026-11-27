import json
P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
def sl(i,lab,mn,mx,st,v): return f'    <div class="slider"><label for="{i}">{lab}</label><input type="range" id="{i}" min="{mn}" max="{mx}" step="{st}" value="{v}"><output id="{i}Out">{v}</output></div>\n'
sec='''<!-- 36. 관련원가 의사결정 -->
<section id="dm" class="sec" aria-labelledby="h-dm">
  <div class="shead"><h2 id="h-dm">관련원가 의사결정</h2><span class="badge hi">비중 상 · 10문항</span><span class="lec">36단원</span></div>
  <div class="key">원칙 하나: <b>대안 사이에 달라지는 미래 금액만 본다</b>. 매몰원가 · 회피 못 하는 고정비 · 배부된 공통비는 무시, 놓치는 공헌이익(기회비용)과 회피 가능 고정비 · 대체 수익(임대료)은 넣는다.<small>관련원가 = 의사결정에 따라 달라지는 원가. 기회비용 = 다른 대안을 택해 포기하는 이익.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 10문항. ① 특별주문(28·30·34·37회) ② 제품·부문 중단(28·32회) ③ 자가제조 vs 구입(31·34회) ④ 제약자원(29회) ⑤ 광고 효과(33회)</p>
  <div class="lab">
    <h3>특별주문 최소가격 · 28회 79번 기본값</h3>
''' + sl('dm1','최대생산능력',0,20000,100,10000) + sl('dm2','기존 판매량',0,20000,100,9000) + sl('dm3','특별주문 수량',0,5000,100,2000) + sl('dm4','특별주문 단위당 변동비',0,3000,10,1000) + sl('dm5','기존 판매 단위당 공헌이익',0,2000,10,800) + '''    <div class="readout" id="dmOut" aria-live="polite"></div>
  </div>
  <div class="tw c1"><table>
    <thead><tr><th>유형</th><th>넣는 것</th><th>빼는 것</th></tr></thead>
    <tbody>
      <tr><td>특별주문</td><td>주문 공헌이익, 포기하는 기존 공헌이익(여유 부족 시)</td><td>고정제조원가</td></tr>
      <tr><td>제품·부문 중단</td><td>잃는 공헌이익, 회피 가능 고정비, 다른 제품 매출 영향, 임대수익</td><td>회피불능 고정비 · 배부 공통비</td></tr>
      <tr><td>자가제조 vs 구입</td><td>변동제조원가, 회피 가능 고정비, 설비 임대수익(기회비용)</td><td>회피불능 고정비</td></tr>
      <tr><td>제약자원</td><td colspan="2">제약자원 단위당 공헌이익이 큰 순서로 생산(29-78: 시간당 A 70 → C 50 → B 45)</td></tr>
    </tbody>
  </table></div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>영업손실 제품 = 중단(28-75 · 32-73).</span>
    <span>단위당 공헌이익 순서로 생산(29-78). 제약자원당.</span>
    <span>여유능력이 모자란데 기회비용을 빠뜨림(30-77 ⑤).</span>
    <span>'제조원가'를 묻는데 관련원가만 계산(34-74 ①).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>선형계획법(제약 2개 이상), 불확실성하 의사결정(완전정보 기대가치)은 넘긴다.</span></div>
  <p class="mine"></p>
</section>

<!-- 37. 예산 -->
<section id="bd" class="sec" aria-labelledby="h-bd">
  <div class="shead"><h2 id="h-bd">종합예산</h2><span class="badge mid">비중 중 · 6문항</span><span class="lec">37단원</span></div>
  <div class="key">순서만 지키면 계산 문제: <b>판매 → 생산(제품 재고) → 원재료 구입(재료 재고) → 현금(회수·지급 시차)</b>. 매번 '필요량 + 기말 목표재고 − 기초재고'.<small>목표재고 = 다음 달 판매(생산)량의 몇 %를 남겨 두라는 재고정책.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 6문항. ① 매입·원재료 구입 예산(28·30·33·37회) ② 현금예산(31·35회)</p>
  <div class="tw c1"><table>
    <thead><tr><th>단계</th><th>식</th></tr></thead>
    <tbody>
      <tr><td>생산량</td><td>판매량 + 기말 제품 − 기초 제품</td></tr>
      <tr><td>원재료 구입량</td><td>생산 소요량 + 기말 재료 − 기초 재료 (투입 시점에 주의, 37-80)</td></tr>
      <tr><td>상품 매입액</td><td>매출원가 + 기말 상품 − 기초 상품, 매출원가 = 매출 ÷ (1 + 이익가산율)</td></tr>
      <tr><td>현금 유출 · 유입</td><td>이번 달 몫 + 지난달·지지난달 이월 몫. 감가상각비 제외</td></tr>
    </tbody>
  </table></div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>감가상각비를 현금유출로(31-78 ②).</span>
    <span>개업 첫 달 기초재고가 0인 것을 잊음(30-80).</span>
    <span>판매월 회수 할인(5%)을 빠뜨림(35-79).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>변동예산 차이 분석 세부(매출가격차이·매출수량차이·시장점유율차이)는 넘긴다.</span></div>
  <p class="mine"></p>
</section>

<!-- 38. 성과평가 · 대체가격 · 최신 관리회계 -->
<section id="pe" class="sec" aria-labelledby="h-pe">
  <div class="shead"><h2 id="h-pe">성과평가 · 대체가격 · 최신 관리회계</h2><span class="badge mid">비중 중 · 9문항</span><span class="lec">38단원</span></div>
  <div class="key">세 덩어리: <b>ROI · RI · EVA</b> 공식, <b>최소대체가격 = 증분원가 + 기회비용</b>, 최신 기법 O·X(카이젠 · 원가기획 · 수명주기 · 균형성과표 · 품질원가 · 제약이론 · JIT).<small>투자수익률(ROI) = 영업이익 ÷ 영업자산. 잔여이익(RI) = 영업이익 − 영업자산 × 최저필수수익률.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 10년 9문항. ① ROI · RI · EVA 계산(32·35·36회) ② 최소대체가격(28·34회) ③ 최신 기법 O·X(32·35·36·37회)</p>
  <div class="tw c1"><table>
    <thead><tr><th>지표</th><th>이익</th><th>차감 기준</th></tr></thead>
    <tbody>
      <tr><td>잔여이익(RI)</td><td>세전 영업이익</td><td>영업자산 × 최저필수수익률</td></tr>
      <tr><td>경제적 부가가치(EVA)</td><td>세후 영업이익</td><td>투하자본 × 가중평균자본비용</td></tr>
      <tr><td>RI 변형</td><td colspan="2">RI = 영업자산 × (ROI − 최저필수수익률)(32-80 · 35-78)</td></tr>
    </tbody>
  </table></div>
  <div class="tw c1"><table>
    <thead><tr><th>최신 기법</th><th>핵심</th></tr></thead>
    <tbody>
      <tr><td>원가기획(목표원가)</td><td>목표가격 − 목표이익. 기획·설계 단계</td></tr>
      <tr><td>수명주기원가</td><td>연구개발~폐기 전 단계, 제조 이전 단계 통제가 핵심, 장기 의사결정</td></tr>
      <tr><td>카이젠</td><td>제조 단계의 지속적 개선(절감 여지는 작음)</td></tr>
      <tr><td>균형성과표</td><td>재무 · 고객 · 내부프로세스 · 학습과 성장, 전략 연계</td></tr>
      <tr><td>품질원가</td><td>통제원가(예방 · 평가) ↑ → 실패원가(내부 · 외부) ↓. 설계품질 ≠ 적합품질</td></tr>
      <tr><td>제약이론 · JIT</td><td>병목 관리, 재료처리량공헌이익 = 매출 − 직접재료 · JIT = 재고 최소화</td></tr>
    </tbody>
  </table></div>
  <div class="trap"><b>자주 틀리는 지점</b>
    <span>EVA를 세전이익 · 최저필수수익률로(36-79).</span>
    <span>카이젠을 설계 단계로(35-80 ②), 수명주기원가를 제조 단계로(36-80 ㅁ).</span>
    <span>설계품질 = 설계대로 생산(37-71 ①). 그건 적합품질.</span>
    <span>대체가격에 고정원가를 넣음(28-74 · 34-77).</span>
  </div>
  <div class="drop"><b>버려도 되는 주제</b><span>분권화 이론, 성과평가 보상 설계, 균형성과표 인과지도 세부는 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#cvp">CVP</a>','<a href="#cvp">CVP</a><a href="#dm">의사결정</a><a href="#bd">예산</a><a href="#pe">성과평가</a>',1)
h=h.replace('["CVP 분석","#cvp","35단원",13,"hi"],','["CVP 분석","#cvp","35단원",13,"hi"],["관련원가 의사결정","#dm","36단원",10,"hi"],["종합예산","#bd","37단원",6,"mid"],["성과평가·대체가격·최신기법","#pe","38단원",9,"mid"],',1)
a='      <tr data-sec="cvp"><td>CVP</td>'
i=h.index(a); j=h.index('\n',i)+1
h=h[:j]+'''      <tr data-sec="dm"><td>의사결정</td><td>관련원가만(매몰 · 회피불능 고정비 X, 기회비용 O) · 특별주문 최소가 = 변동비 + 포기 공헌이익 ÷ 주문량 · 제약자원당 공헌이익 순</td></tr>
      <tr data-sec="bd"><td>예산</td><td>판매 → 생산 → 재료 → 현금 · 필요량 + 기말 목표 − 기초 · 감가상각비는 현금 아님</td></tr>
      <tr data-sec="pe"><td>성과평가</td><td>RI = 이익 − 자산 × 최저필수 · EVA = 세후이익 − 투하자본 × WACC · 최소대체가 = 증분원가 + 기회비용 · 카이젠 = 제조단계, 원가기획 = 설계단계</td></tr>
'''+h[j:]
js='''
/* 36. 특별주문 */
function dmCalc(){const v=["dm1","dm2","dm3","dm4","dm5"].map(i=>{$("#"+i+"Out").textContent=(+$("#"+i).value).toLocaleString();return +$("#"+i).value});
 const idle=Math.max(0,v[0]-v[1]),give=Math.max(0,v[2]-idle),opp=give*v[4],p=v[2]?v[3]+opp/v[2]:0;
 $("#dmOut").innerHTML=`여유능력 ${idle.toLocaleString()} → 포기하는 기존 판매 ${give.toLocaleString()}단위 × ${v[4].toLocaleString()} = 기회비용 ${opp.toLocaleString()} → 최소가격 <b>₩${(Math.round(p*100)/100).toLocaleString()}</b>`}
["dm1","dm2","dm3","dm4","dm5"].forEach(i=>$("#"+i).addEventListener("input",dmCalc));dmCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h)
U='/home/claude/gamjung1sttest/data/acct/units.json'; u=json.load(open(U))
for x in u['units']:
    x['note']={'KA':'dm','KB':'bd','KC':'pe'}.get(x['u'],x.get('note'))
    if x.get('note') is None: x.pop('note',None)
u['mapNote']='단원 구분과 문항 분류는 표준 중급회계·원가관리회계 순서로 나눈 것이라 신은미 교수 교재의 장 순서와 다를 수 있습니다. 10년치 기출 전 단원이 들어 있고, 진도로 설정한 단원까지만 출제됩니다.'
json.dump(u,open(U,'w'),ensure_ascii=False,indent=1); print('ok',[x['u'] for x in u['units'] if not x.get('note')])
