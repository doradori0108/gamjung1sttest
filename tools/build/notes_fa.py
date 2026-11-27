P='/home/claude/gamjung1sttest/notes/acct.html'; h=open(P).read()
assert 'id="fa"' not in h
sec='''<!-- 12. 금융자산 -->
<section id="fa" class="sec" aria-labelledby="h-fa">
  <div class="shead"><h2 id="h-fa">금융자산</h2><span class="badge hi">비중 상 · 12문항</span><span class="lec">12단원</span></div>
  <div class="key">금융자산은 세 칸(AC · FVOCI · FVPL) 중 어디에 넣느냐가 전부다. 칸이 정해지면 거래원가 · 이자 · 평가 · 처분 처리가 자동으로 정해진다.<small>AC(상각후원가) = 공정가치 무시, 유효이자만. FVOCI(기타포괄손익-공정가치) = 이자는 AC처럼, 공정가치 변동은 OCI. FVPL(당기손익-공정가치) = 변동 전부 당기손익.</small></div>
  <p class="ask"><b>시험에서 묻는 방식</b> · 매년 1~2문항. ① 같은 채권을 세 칸으로 나눠 당기순이익 비교(31회 70번) ② FVPL 주식 처분·평가 손익(35회 54번 · 37회 50번) ③ FVOCI 처분손익(36회 54번) ④ 손상·재분류(35회 58번 · 36회 55번) ⑤ 이론 '옳지 않은 것'(30·33·34회)</p>

  <h3>① 어느 칸? 두 질문으로 정한다</h3>
  <div class="tw c1"><table>
    <thead><tr><th>현금흐름이 원금 + 이자뿐?</th><th>사업모형(왜 들고 있나)</th><th>분류</th></tr></thead>
    <tbody>
      <tr><td rowspan="3">예 (채권 · 대여금 · 매출채권)</td><td>만기까지 이자·원금 받기</td><td><b>AC</b></td></tr>
      <tr><td>받으면서 팔기도</td><td><b>FVOCI</b>(채무상품)</td></tr>
      <tr><td>그 밖(매매)</td><td><b>FVPL</b></td></tr>
      <tr><td>아니오 (주식 · 파생상품)</td><td>—</td><td><b>FVPL</b> 원칙 · 단기매매 아닌 주식은 최초에 <b>FVOCI 선택</b> 가능(취소 불가)</td></tr>
    </tbody>
  </table></div>
  <p class="foot">예외: 회계불일치를 없애려면 무엇이든 FVPL로 '지정' 가능(취소 불가). 도로사업에 비유하면 같은 장비라도 '직접 운용(AC) · 운용하다 팔 수도(FVOCI) · 되팔 목적(FVPL)'에 따라 장부가 달라지는 것.</p>

  <h3>② 칸별 처리표 (이 표 하나로 계산 문제 대부분이 풀린다)</h3>
  <div class="tw c1"><table>
    <thead><tr><th></th><th>AC</th><th>FVOCI 채무상품</th><th>FVOCI 지분(선택)</th><th>FVPL</th></tr></thead>
    <tbody>
      <tr><td>거래원가</td><td>원가 가산</td><td>원가 가산</td><td>원가 가산</td><td><b>당기비용</b></td></tr>
      <tr><td>이자 · 배당</td><td>유효이자</td><td>유효이자</td><td>배당 = 당기손익</td><td>받은 이자·배당</td></tr>
      <tr><td>공정가치 변동</td><td>무시</td><td>OCI</td><td>OCI</td><td><b>당기손익</b></td></tr>
      <tr><td>손상(기대신용손실)</td><td>당기손익 · 손실충당금</td><td>당기손익 · 상대는 OCI</td><td>손상 없음</td><td>없음</td></tr>
      <tr><td>처분 시 OCI 누계</td><td>—</td><td><b>당기손익으로 재분류</b></td><td><b>재분류 금지</b>(이익잉여금 대체만)</td><td>—</td></tr>
    </tbody>
  </table></div>
  <p class="ask">한 줄 요약: <b>FVOCI 채무상품의 당기순이익은 언제나 AC와 같다.</b> 차이는 재무상태표 금액과 OCI뿐.</p>

  <div class="lab">
    <h3>같은 채권, 세 칸 비교 · 31회 70번 숫자</h3>
    <p class="foot">액면 1,000,000 · 표시 4% · 취득 896,884 · 유효 8% · 20×2년 초 처분</p>
    <div class="slider"><label for="fa1">20×1년 말 공정가치</label><input type="range" id="fa1" min="880000" max="980000" step="5000" value="925000"><output id="fa1Out">925000</output></div>
    <div class="slider"><label for="fa2">20×2년 초 처분가</label><input type="range" id="fa2" min="880000" max="1000000" step="5000" value="940000"><output id="fa2Out">940000</output></div>
    <div class="tw c1"><table><thead><tr><th>분류</th><th class="n">20×1 당기순이익</th><th class="n">20×1 OCI</th><th class="n">20×2 당기순이익</th></tr></thead><tbody id="faBody"></tbody></table></div>
  </div>

  <h3>③ 손상(기대신용손실)과 재분류</h3>
  <div class="grid2">
    <div class="mini"><h3>신용손상 발생(35회 58번)</h3><p>손상차손 = 장부금액 − 추정 현금흐름의 현재가치. 할인율은 <b>최초 유효이자율</b>(시장이자율 X). 이후 이자수익 = 상각후원가 × 유효이자율.</p></div>
    <div class="mini"><h3>재분류(채무상품만, 사업모형 변경 시)</h3><p>AC → FVPL: 차이 당기손익(36회 55번: 8,800 − (9,200 − 600) = 200 이익) · AC → FVOCI: 차이 OCI · 지분상품은 재분류 불가.</p></div>
  </div>

  <div class="trap"><b>자주 틀리는 지점</b>
    <span>AC인데 공정가치를 쓴다. 문제에 공정가치가 나와도 AC는 무시(29회 51번).</span>
    <span>FVOCI 채무상품 처분손익을 '처분가 − 직전 공정가치'로 계산한다. 상각후원가 기준이다(31회 70번 ⑤ · 36회 54번).</span>
    <span>FVPL 거래원가를 원가에 넣는다. 즉시 비용(35회 54번 · 37회 50번). 반대로 FVOCI는 원가 가산(32회 65번).</span>
    <span>무상주 수령을 수익으로 잡는다. 주식 수만 늘고 단가가 내려간다(37회 50번).</span>
    <span>기말 FVPL 평가에서 예상 처분수수료를 뺀다. 빼지 않는다(37회 50번 ①).</span>
    <span>"상계하면 손익 발생" · "FVOCI 손상환입은 OCI" · "제각 불가" → 모두 X(30회 62번 · 34회 57번).</span>
  </div>
  <div class="drop"><b>우선순위 · 버려도 되는 주제</b><span>칸별 처리표와 FVPL·FVOCI 계산은 반드시. 신용손상 3단계 이자 계산(처음부터 손상 · 신용조정 유효이자율), 금융자산 양도 · 지속적 관여, 계약 변경손익 계산은 과락 회피 목표라면 이론 한 줄만 외우고 계산은 넘긴다.</span></div>
  <p class="mine"></p>
</section>

'''
h=h.replace('<!-- 암기카드 -->',sec+'<!-- 암기카드 -->',1)
h=h.replace('<a href="#cr">현금·수취채권</a>','<a href="#cr">현금·수취채권</a><a href="#fa">금융자산</a>',1)
h=h.replace('["투자부동산·생물자산","#ip","10단원",17,"hi"],','["투자부동산·생물자산","#ip","10단원",17,"hi"],["금융자산","#fa","12단원",12,"hi"],',1)
card='''      <tr data-sec="fa"><td>금융자산 분류</td><td>원리금만 + 수취 = AC · 수취·매도 = FVOCI · 나머지 = FVPL · 주식은 FVOCI 선택 가능</td></tr>
      <tr data-sec="fa"><td>FVOCI 채무상품</td><td>당기순이익 = AC와 동일 · 처분 시 OCI 재분류 / 지분상품은 재분류 금지</td></tr>
      <tr data-sec="fa"><td>거래원가</td><td>FVPL만 당기비용, 나머지 원가 가산</td></tr>
'''
a='      <tr data-sec="cr"><td>어음할인</td>'
i=h.index(a); j=h.index('\n',i)+1; h=h[:j]+card+h[j:]
js='''
/* 12. 금융자산 세 칸 비교 */
function faCalc(){const F1=+$("#fa1").value,F2=+$("#fa2").value;$("#fa1Out").textContent=F1;$("#fa2Out").textContent=F2;
 const c0=896884,int1=Math.round(c0*.08),ac1=c0+int1-40000;
 const rows=[["AC",int1,0,F2-ac1],["FVOCI 채무상품",int1,F1-ac1,F2-ac1],["FVPL",40000+F1-c0,0,F2-F1]];
 const s=v=>(v<0?"(":"")+w(Math.abs(v))+(v<0?")":"");
 $("#faBody").innerHTML=rows.map(r=>`<tr><td>${r[0]}</td><td class="n">${s(r[1])}</td><td class="n">${r[2]?s(r[2]):"—"}</td><td class="n">${s(r[3])}</td></tr>`).join("")}
["fa1","fa2"].forEach(i=>$("#"+i).addEventListener("input",faCalc));faCalc();
'''
i=h.rindex('</script>'); h=h[:i]+js+h[i:]
open(P,'w').write(h); print('ok')
